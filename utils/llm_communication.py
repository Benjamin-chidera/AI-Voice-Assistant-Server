import os

# langchain - llm
import langgraph
from langchain.text_splitter import RecursiveCharacterTextSplitter
from pinecone import Pinecone, ServerlessSpec
from langchain_core.output_parsers import StrOutputParser
from langchain_ollama import ChatOllama, OllamaEmbeddings
from langchain_core.prompts import ChatPromptTemplate

index_name = "echo-voice-assistant"

api_key = os.getenv("PINECONE_API_KEY")

pc = Pinecone(api_key=api_key)


if not pc.has_index(index_name):
    pc.create_index(
        name=index_name,
        dimension=4096,
        metric="cosine",
        spec=ServerlessSpec(cloud="aws", region="us-east-1"),
    )

index = pc.Index(index_name)


async def speak_to_llm(text):
    
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    
    text = text_splitter.split_text(text)
    
    message = [
        (
            "system", f"""You are a professional ai voice assistant.
            
            respond to the following query: {text}
            """
            
        ), 
        (
            "human", "{query}"
        )
    ]
    
    
    llm = ChatOllama(model="llama3.1")
    
    chat = ChatPromptTemplate.from_messages(message)
    
   
    
    chain = chat | llm | StrOutputParser()
    
    response = chain.invoke({"query": text})
    
    print("Response from LLM:", response)