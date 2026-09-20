from click import prompt
from typer import prompt
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser

load_dotenv()

llm = ChatGroq(
    model = "llama-3.1-8b-instant",
    temperature = 0.7,
    groq_api_key = os.getenv("GROQ_API_KEY")
)
template = PromptTemplate.from_template("Why human exist, how god makes human, and what is the meaning of life? What should purpose be the human in the earth? We should go for money or peace if anyone thught about peace then meaing comes out that the person  is lazy and don't want to work hard for money. If anyone thught about money then meaning comes out that the person is hardworking and want to work hard for money. So, what is the meaning of life?")
chain = template | llm | StrOutputParser()

response = chain.invoke({})
print(response)