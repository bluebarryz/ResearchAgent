from langchain.agents import initialize_agent, Tool
from langchain.agents.agent_types import AgentType
from langchain.chat_models import ChatOpenAI
from langchain.utilities import ArxivAPIWrapper
from langchain.tools import DuckDuckGoSearchRun
from langchain.chains import RetrievalQA
from langchain.vectorstores import FAISS
from langchain.document_loaders import ArxivLoader
from langchain.embeddings import OpenAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.memory import ConversationBufferMemory
from langchain.schema import HumanMessage
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uvicorn
import os
import tempfile

from dotenv import load_dotenv
load_dotenv()


# Arxiv search
arxiv_tool = Tool(
    name="ArxivSearch",
    func=ArxivAPIWrapper().run,
    description="Search for academic papers on arXiv related to a topic."
)

# web search for supplementary sources
web_search_tool = Tool(
    name="WebSearch",
    func=DuckDuckGoSearchRun().run,
    description="Search for relevant information online."
)


# Vector DB setup. Return the vector store object for arxiv text related to the query
def build_vectorstore_from_arxiv(query):
    # search arxiv for papers related to the query
    loader = ArxivLoader(query)
    docs = loader.load()

    # split text into chunks
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    chunks = text_splitter.split_documents(docs)
    embeddings = OpenAIEmbeddings()
    db = FAISS.from_documents(chunks, embeddings)
    return db

## Agent with memory
# store convo history
memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
llm = ChatOpenAI(temperature=0.3, model_name="gpt-4")
tools = [arxiv_tool, web_search_tool]
agent = initialize_agent(
    tools,
    llm,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True,
    memory=memory
)

## FastAPI web interface
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

## Query pipeline
class QueryRequest(BaseModel):
    query: str

@app.post("/query")
async def run_query(req: QueryRequest):
    # Build fresh vector db from arxiv content
    db = build_vectorstore_from_arxiv(req.query)
    retriever = db.as_retriever()
    rag_chain = RetrievalQA.from_chain_type(llm=llm, retriever=retriever)

    # Compose final response from RAG and agent
    rag_response = rag_chain.run(req.query)
    agent_response = agent.run(req.query)

    return {
        "rag": rag_response,
        "agent": agent_response
    }

# python -m uvicorn main:app --reload
