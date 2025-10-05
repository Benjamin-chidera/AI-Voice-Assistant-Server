import os
# langchain - llm
from langchain.text_splitter import RecursiveCharacterTextSplitter
from pinecone import Pinecone, ServerlessSpec
from langchain_core.output_parsers import StrOutputParser
from langchain_ollama import ChatOllama, OllamaEmbeddings
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from openai import OpenAI
from langchain_pinecone import PineconeVectorStore

index_name = os.getenv("PINECONE_INDEX_NAME")

print("Pinecone Index Name:", index_name)

api_key = os.getenv("PINECONE_API_KEY")

pc = Pinecone(api_key=api_key)
 
client = OpenAI()

llm = ChatOllama(model="llama3.1")
# llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0.7)

# emben=dding
embedding = OllamaEmbeddings(model="llama3.1")
# embedding = OpenAIEmbeddings(model="text-embedding-3-small")
 
if not pc.has_index(index_name): # type: ignore
    pc.create_index(
        name=index_name, # type: ignore
        # dimension=1536, # this is for openai
        dimension=4096, # this is for ollama
        metric="cosine",
        spec=ServerlessSpec(cloud="aws", region="us-east-1"),
    )

index = pc.Index(index_name) # type: ignore


async def speak_to_llm(text, voice, language, user_name):
    # Split text (optional)
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    splitted_text = text_splitter.split_text(text)

    print("echo language:", language)

   
    vector_store = PineconeVectorStore(index=index, embedding=embedding)

    previous_chat = vector_store.similarity_search(text, k=5, filter={"user": user_name})

    chat_history = "\n\n".join([doc.page_content for doc in previous_chat]) if previous_chat else "No prior context."

    message = [
        ("system", f"""You are Echo, a professional AI voice assistant. You can answer questions asked by the user in a friendly and professional manner.
        The user's name is {user_name}.
        You must ALWAYS respond in {language}, regardless of the input language.
        Here is the recent chat history:
        {chat_history}
        Now continue the conversation naturally, keeping context and tone consistent."""),
        ("human", "{query}")
    ]

    chat = ChatPromptTemplate.from_messages(message)
    chain = chat | llm | StrOutputParser()

    ai_response = chain.invoke({"query": text})
    print("Response from LLM:", ai_response)

    doc = f"User: {splitted_text}\nAI: {ai_response}"

    vector_store.add_texts(
        [doc],
        metadatas=[{"role": "conversation", "user": user_name}]
    )

    return ai_response



async def chat_llm(message: str, language: str, user_name: str):
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    splitted_text = text_splitter.split_text(message)
    
    print("echo language:", language)

    
  
    vector_store = PineconeVectorStore(index=index, embedding=embedding)
    
    # get the most similar conversation turn
    previous_chat = vector_store.similarity_search(message, k=5)

    chat_history = "\n\n".join([doc.page_content for doc in previous_chat])

    
    messages = [
    ("system", f"""You are Echo, a professional AI voice assistant. You can answer questions asked by the user in a friendly and professional manner.
    You must ALWAYS respond in {language}, regardless of input language. 
    The user name is {user_name}.

    Here is the conversation so far:
    {chat_history}

    Now continue the conversation naturally, staying in context.
    """),
    ("human", "{message}")
]
    
    chat = ChatPromptTemplate.from_messages(messages) 
    chain = chat | llm | StrOutputParser()

    ai_response = chain.invoke({"message": message}) 
    print("Response from LLM:", ai_response)
    
    
    doc = f"""
            User: {splitted_text}
            AI: {ai_response}"""

    vector_store.add_texts([doc], metadatas=[{"role": "conversation"}])

    return ai_response
