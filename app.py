import streamlit as st
from groq import Groq
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Initialize the Groq client
client = Groq()

## Function To get response from Groq LLaMA 3.1-8b-instant model
def getLLamaresponse(input_text, no_words, blog_style):
    
    # Prepare the message for the Groq API
    messages = [
        {
            "role": "user",
            "content": f"Write a blog for {blog_style} job profile for a topic {input_text} within {no_words} words."
        }
    ]

    # Generate the response using Groq API
    completion = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=messages,
        temperature=1,
        max_tokens=1024,
        top_p=1,
        stream=True,
        stop=None,
    )

    response = ""
    for chunk in completion:
        response += chunk.choices[0].delta.content or ""

    return response


# Streamlit UI setup
st.set_page_config(page_title="Generate Blogs",
                   page_icon='🤖',
                   layout='centered',
                   initial_sidebar_state='collapsed')

st.header("🤖 Generate Blogs for Job Specification 🤖")

# Input fields for topic and additional blog options
input_text = st.text_input("Enter the Blog Topic")

# Creating two columns for additional fields
col1, col2 = st.columns([5, 5])

with col1:
    no_words = st.text_input('No of Words')

with col2:
    blog_style = st.selectbox('Writing the blog for',
                              ('Researchers', 'Data Scientist', 'Software Developer', 'Data Analytics'), index=0)

# Generate button
submit = st.button("Generate")

# Final response display
if submit:
    st.write(getLLamaresponse(input_text, no_words, blog_style))
