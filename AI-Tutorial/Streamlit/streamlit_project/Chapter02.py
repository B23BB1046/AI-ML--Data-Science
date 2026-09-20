import streamlit as st
import requests

st.title("Calculator")
st.subheader("This is a simple calculator app built with Streamlit.")
st.number_input1 = st.number_input('Enter the first number:')
st.number_input2 = st.number_input('Enter the second number:')
operation = st.selectbox('select an operation:', ['Addition', 'Subtraction', 'Multiplication', 'Division'])

if operation == 'Additionn':
    result = st.number_input1 + st.number_input2
elif operation == 'Subtraction':
    result = st.number_input1 - st.number_input2
elif operation == 'Multiplication':
    result = st.number_input1 * st.number_input2
elif operation == 'Division':       
    if st.number_input2 != 0:
        result = st.number_input1 / st.number_input2
else:
        result = 'Error: Division by zero is not allowed.'
st.write(f'Result: {result}')

col1, col2  = st.columns(2)
with col1:
    st.header('Masala Chai')
    vote1= st.button('Vote for Masala Chai')
    st.image('https://media.istockphoto.com/id/1297483389/photo/masala-tea-chai.jpg?s=612x612&w=0&k=20&c=Pv-QROSSywNh_qzHIIjHJeJB7OT0ujrKQsSiTgOmJAs=',width=300)
with col2:
    st.header('Adrak chai')
    vote2 = st.button('Vote for adrak chai')
    st.image('https://media.istockphoto.com/id/1336601313/photo/top-view-of-indian-herbal-masala-chai-or-traditional-beverage-tea-with-milk-and-spices-kerala.jpg?s=612x612&w=0&k=20&c=txjXqXtu3_PcA0ztNxyNVXJ-YziORr2XnuHWIriNEKk=',width=300)
if vote1:
    st.success('thank you for voting for masala chai')
if vote2:
    st.success('thank you for voting for adrak chai')
name = st.sidebar.text_input('Enter your name:')
tea = st.sidebar.selectbox('Select your favorite color:', ['Red', 'Green', 'Blue', 'Yellow'])

if st.sidebar.button('Submit'):
    st.sidebar.success(f'Thank you {name} for selecting {tea} as your favorite color!')

