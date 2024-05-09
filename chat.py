from unittest import result
import streamlit as st
from pymongo import MongoClient
from langchain_openai import OpenAIEmbeddings
import os
from langchain_openai import ChatOpenAI
 
# Set up OpenAI API key
os.environ["OPENAI_API_KEY"] = ""
 
# # Set up MongoDB connection
# MONGO_URL = "mongodb+srv://sriramg:Coc54694@cluster0.uwofdgc.mongodb.net/"
# MONGO_DBNAME = "vectorcollections"
# COLLECTION = "datatest"
 
# client = MongoClient(MONGO_URL)
# db = client[MONGO_DBNAME]
# vec_collection = db[COLLECTION]
 
# Initialize OpenAI embeddings
# embeddings = OpenAIEmbeddings()
chatgpt = ChatOpenAI()
 
# Define Streamlit app  
def main():
    st.title("Your Friendly Assistent")
 
    # User input for query
    query = st.text_input("Ask Your Question:")
    print("Query_vector----->", query)
 
    if st.button("Search"):
        # Embed the input text
        prompt = "can you give me detailed response for this:\n" + query
        response = chatgpt.predict(prompt)
        st.write("AI Response:", response)
        
if __name__ == "__main__":
    main()
