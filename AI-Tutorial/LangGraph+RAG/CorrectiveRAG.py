from langchain_groq import ChatGroq
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from typing import TypedDict, List
from dotenv import load_dotenv
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_core.documents import Document
import os
import regex as re
from pydantic import BaseModel
from langgraph.graph import StateGraph,START,END
from langchain_core.prompts import ChatPromptTemplate
from langchain_tavily import TavilySearch
import torch

load_dotenv()
# Define the LLM to be used for question answering
llm = ChatGroq(
    model = 'llama-3.1-8b-instant',
    api_key = os.getenv('GROQ_API_KEY'),
    temperature = 0.7
)


device = "cuda" if torch.cuda.is_available() else "cpu"


# Define the model for Embedding
model = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2",
    model_kwargs={"device": "cuda"}
)

# Load the External PDF document for RAG
docs  = (
        PyPDFLoader('/home/yogendra/Downloads/Machine Learning ( etc.) (z-lib.org).pdf').load() +
        PyPDFLoader('/home/yogendra/Downloads/Introduction to Machine Learning with Python ( PDFDrive.com )-min.pdf').load()
        )
print(len(docs))

# Divide into the chunks
chunks = RecursiveCharacterTextSplitter(chunk_size = 900,chunk_overlap = 100).split_documents(docs)

# Make the embedding and store them
vectorstore = FAISS.from_documents(
    chunks,
    model
    
)
retriever = vectorstore.as_retriever(search_type = 'similarity', search_kwargs = {"k": 4})
# Define Threshold
UPPER_TH = 0.5
LOWER_TH = 0.2

# Define the class State
class State(TypedDict):
    question: str
    context: List[str]
    docs: List[Document]
    
    good_docs: List[Document]
    verdict: str
    reason: str
    
    strips: List[str]
    kept_strips: List[str]
    refined_context: str
    web_docs: List[Document]
    web_query:str
    
    answer: str
def retrive_docs(state:State) ->State:
    q = state['question']
    return {'docs':retriever.invoke(q)}
class docEvalScore(BaseModel):
    relevance: float
    reason: str
doc_eval_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You are a strict retrieval evaluator for RAG.\n"
            "You will be given ONE retrieved chunk and a question.\n"
            "Return a relevance in [0.0, 1.0].\n"
            "- 1.0: chunk alone is sufficient to answer fully/mostly\n"
            "- 0.0: chunk is irrelevant\n"
            "Be conservative with high relevance.\n"
            "Also return a short reason.\n"
            "Output JSON only.",
        ),
        ("human", "Question: {question}\n\nChunk:\n{chunk}"),
    ]
)

doc_eval_chain = doc_eval_prompt | llm.with_structured_output(docEvalScore,method = 'json_mode')
def eval_each_node_doc(state:State)->State:
    q = state['question']
    relevance: List[float] = []
    reason: List[str] = []
    good: List[Document] = []
    
    for d in state['docs']:
        
        try:
            
            out = doc_eval_chain.invoke({'question': q, 'chunk': d.page_content})
        except Exception as e:
            print('parsing error:',e)
            out = docEvalScore(
                relevance=0.0,
                reason ='Evaluation_Failed'
            )
        relevance.append(out.relevance)
        reason.append(out.reason)
        if out.relevance>LOWER_TH:
            good.append(d)
    if any(s>UPPER_TH for s in relevance):
        return {
            'good_docs':good,
            'verdict':'correct',
            'reason': f'At leas one retrieve chunk store > {UPPER_TH}'
        }
    if len(relevance)>0 and all(s<LOWER_TH for s in relevance):
        why = "Because no chunk was important to give the answer"
        return {
            'good_docs': [],
            'verdict':'Incorrect',
            'reason': f'All retrieved chunk was relevance<{LOWER_TH}.{why}'
        }
        
    why = 'Mix relevance signal'
    return {
        'good_docs':good,
        'verdict': 'Ambigous',
        'reason': f'All retrieve chunk relevane<{UPPER_TH} and more than >{LOWER_TH}. {why}'
    }
def decompose_to_sentences(text: str) -> List[str]:
    text = re.sub(r"\s+", " ", text).strip()
    sentences = re.split(r"(?<=[.!?])\s+", text)
    return [s.strip() for s in sentences if len(s.strip()) > 20]

# Filter(LLM Judge)
class KeepOrDrop(BaseModel):
    keep:bool
filter_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You are a strict relevance filter.\n"
            "Return keep=true only if the sentence directly helps answer the question.\n"
            "Use ONLY the sentence. Output JSON only.",
        ),
        ("human", "Question: {question}\n\nSentence:\n{sentence}"),
    ]
)

filter_chain = filter_prompt|llm.with_structured_output(KeepOrDrop,method='json_mode')
def refine(state:State)->State:
    q = state['question']
    if state.get('verdict')=='correct':
        docs_to_use = state['good_docs']
    elif state.get('verdict')=='Incorrect':
        docs_to_use = state["web_docs"]
    else:
        docs_to_use = state.get('good_docs',[]) + state.get('web_docs',[])
    context = "\n\n".join(d.page_content for d in docs_to_use).strip()
    strips = decompose_to_sentences(context)
    
    # Filter keep only relevent strip
    kept: List[str] = []
    for s in strips:
        if filter_chain.invoke({'question':q, 'sentence': s}).keep:
            kept.append(s)
    refined_context = "\n".join(kept).strip()
    
    return {
        "strips": strips,
        "kept_strips": kept,
        "refined_context": refined_context,
    }
    
# For Web query so that user input can be minimize and rich input goes for the web searching
def rewrite_query_node(state: State) -> State:

    prompt = f"""
    Convert the following question into a short web search query.

    Question:
    {state['question']}

    Only return the search query.
    """

    out = llm.invoke(prompt)

    return {
        "web_query": out.content.strip()
    }

# Web Searching code using Tavily
# Web Searching code using Tavily
tavily = TavilySearch(max_results=5)

def web_search_node(state: State) -> State:

    q = state['web_query'] or state["question"]

    results = tavily.invoke({"query": q})

    # Tavily returns a dictionary
    search_results = results.get("results", [])

    web_docs = []

    for r in search_results:

        title = r.get("title", "")
        url = r.get("url", "")
        content = r.get("content", "") or r.get("snippet", "")

        text = f"""
TITLE: {title}

URL: {url}

CONTENT:
{content}
"""

        web_docs.append(
            Document(
                page_content=text,
                metadata={
                    "url": url,
                    "title": title
                }
            )
        )

    return {"web_docs": web_docs}

answer_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You are a helpful ML tutor. Answer ONLY using the provided context.\n"
            "If the context is empty or insufficient, say: 'I don't know.'",
        ),
        ("human", "Question: {question}\n\nRefined context:\n{refined_context}"),
    ]
)

def generate(state: State) -> State:
    out = (answer_prompt | llm).invoke(
        {"question": state["question"], "refined_context": state["refined_context"]}
    )
    return {"answer": out.content}
def fail_node(state:State)->State:
    return {'answer': f"FAIL:{state['reason']}"}
def ambiguous_node(state:State)->State:
    return {'answer': f"Ambiguous:{state['reason']}"}
def route_after_eval(state:State)->str:
    if state['verdict'] == 'correct':
        return 'refine'
    else:
        return 'rewrite_query'
    
g = StateGraph(State)
g.add_node("retrieve", retrive_docs)
g.add_node("eval_each_doc", eval_each_node_doc)
g.add_node('rewrite_query', rewrite_query_node)
g.add_node('web_search',web_search_node)
g.add_node("refine", refine)
g.add_node("generate", generate)


g.add_edge(START,'retrieve')
g.add_edge('retrieve','eval_each_doc')
g.add_conditional_edges(
    'eval_each_doc',
    route_after_eval,
    {'refine':'refine','rewrite_query':'rewrite_query'}
)
g.add_edge('rewrite_query','web_search')
g.add_edge('web_search','refine')
g.add_edge('refine','generate')
g.add_edge('generate',END)
app = g.compile()
app

while True:
    
    q= input("\nAsk any question (type 'exit' to quit): ")
    if q.lower()=='exit':
        
        print('Goodbye')
        break
    
    
    
    
    
        
    res = app.invoke(
        
        {
            "question": q,
            "docs": [],
            "good_docs": [],
            "verdict": "",
            "reason": "",
            "strips": [],
            "kept_strips": [],
            "refined_context": "",
            "web_docs":[],
            "web_query": "",
            "answer": "",
        }
    )

    print("VERDICT:", res["verdict"])
    print("REASON:", res["reason"])
    print("\nOUTPUT:\n", res["answer"])