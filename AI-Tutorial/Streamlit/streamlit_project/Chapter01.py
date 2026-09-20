import streamlit as st

st.title('Hello Sudha kaise ho tum')
st.subheader('me badhiya hu, tum kaise ho chandar')
st.text('bas kat rahi h zindagi, shukla ji kidhar h')
st.write('humko ka pta, kabhi hamare bare me bhi puch liya karo, hamari to fikar hi nhi h tumko ki hum kaise hai, bus pure din cycle par hi ghumte rehte ho')
option = st.selectbox(' tum sabse jyada kisko pasand krte ho:',['Pammi','Dr Shukla','Sudha','Binti'])
st.write(f'{option}, Accha ji hum kyu nhi aisa kya kr diya apki {option} ji ne ')



