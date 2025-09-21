import os
import base64

# langchain - llm
import langgraph
from langchain.text_splitter import RecursiveCharacterTextSplitter
from pinecone import Pinecone, ServerlessSpec
from langchain_core.output_parsers import StrOutputParser
from langchain_ollama import ChatOllama, OllamaEmbeddings
from langchain_core.prompts import ChatPromptTemplate
from openai import OpenAI
from langchain_pinecone import PineconeVectorStore

index_name = os.getenv("PINECONE_INDEX_NAME")

print("Pinecone Index Name:", index_name)

api_key = os.getenv("PINECONE_API_KEY")

pc = Pinecone(api_key=api_key)

client = OpenAI()

llm = ChatOllama(model="llama3.1")
 
if not pc.has_index(index_name): # type: ignore
    pc.create_index(
        name=index_name, # type: ignore
        dimension=4096,
        metric="cosine",
        spec=ServerlessSpec(cloud="aws", region="us-east-1"),
    )

index = pc.Index(index_name) # type: ignore


async def speak_to_llm(text, voice, language):
    # 1. Split text if long (optional for user query, but fine for docs)
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    splitted_text = text_splitter.split_text(text)
    
    print("echo language:", language)

    # 2. Build prompt for LLM
    message = [
        ("system", f"""You are Echo, a professional AI voice assistant.
                      You must ALWAYS respond in {language}, regardless of input language. """),
        ("human", "{query}")
    ]

    chat = ChatPromptTemplate.from_messages(message)
    chain = chat | llm | StrOutputParser()

    ai_response = chain.invoke({"query": text})
    print("Response from LLM:", ai_response)

    # 3. Convert response to speech (uncomment when ready)
    # with client.audio.speech.with_streaming_response.create(
    #     model="gpt-4o-mini-tts",
    #     voice=voice,
    #     input=ai_response,
    # ) as response:
    #     audio_bytes = response.read() 
    # speech_response = base64.b64encode(audio_bytes).decode("utf-8")
    speech_response = "dfff" # temporary placeholder

    # 4. Save both USER and AI response into Pinecone
    embedding = OllamaEmbeddings(model="llama3.1")
    vector_store = PineconeVectorStore(index=index, embedding=embedding)

    # create a "conversation turn" doc
    doc = f"""
            User: {splitted_text}
            AI: {ai_response}"""

    vector_store.add_texts([doc], metadatas=[{"role": "conversation"}])

    return ai_response, speech_response


async def chat_llm(message: str, language: str):
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    splitted_text = text_splitter.split_text(message)
    
    print("echo language:", language)

    
    embedding = OllamaEmbeddings(model="llama3.1")
    vector_store = PineconeVectorStore(index=index, embedding=embedding)
    
    # get the most similar conversation turn
    previous_chat = vector_store.similarity_search(message, k=5)
    
    messages = [
        ("system", f"""You are Echo, a professional AI voice assistant.
                        You must ALWAYS respond in {language}, regardless of input language. 
                        Here is the conversation so far (but translate your response into {language}):

                    
                    {[previous_chat.page_content for previous_chat in previous_chat]}
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