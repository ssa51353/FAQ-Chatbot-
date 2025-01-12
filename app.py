import streamlit as st
import openai
import pandas as pd
from fuzzywuzzy import fuzz

# Load FAQ dataset
def load_faq_data(file_path):
    return pd.read_csv(r"C:\Users\Shreya\OneDrive\Desktop\faq_chatbot\faq_dataset.csv")

# Get a response from OpenAI GPT
def get_response(question):
    try:
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=f"Answer this question: {question}",
            max_tokens=100,
            temperature=0.7
        )
        return response['choices'][0]['text'].strip()
    except Exception as e:
        return f"Error: {str(e)}"

# Match user query to the dataset
from fuzzywuzzy import fuzz

def search_dataset(question, dataset):
    for _, row in dataset.iterrows():
        score = fuzz.partial_ratio(question.lower(), row["Question"].lower())
        if score > 80:  # Match if score is greater than 80
            return row["Answer"]
    return None


# Streamlit App
st.title("FAQ Chatbot")
st.write("Ask me anything about our services!")

# Load dataset
faq_data = load_faq_data("faq_dataset.csv")

# User input
question = st.text_input("Enter your question:")
if st.button("Get Answer"):
    if question:
        # First, try to find the answer in the dataset
        answer = search_dataset(question, faq_data)
        if not answer:  # If no match is found, use OpenAI API
            answer = get_response(question)
        st.write(f"**Answer:** {answer}")
    else:
        st.write("Please enter a question.")
