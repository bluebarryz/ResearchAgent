# ResearchAgent

A research tool that utlizes a dual approach of RAG (providing grounded, factual responses) and agents (providing more reasoning and exploration) to generate grounded, insightful responses to research queries.

## Overview

When the user provides a query (e.g. "explain what the Pareto front is"), the app generates two types of responses:
1. A "RAG-based" response
    1. Searches for arxiv papers related to the query, does chunking then embedding on the returned papers, and stores the embeddings in a [VectorStore](https://python.langchain.com/v0.1/docs/modules/data_connection/vectorstores/) object.
    2. Embeds the user query and retrieves the embeddings in the VectorStore object most relevant to the user's query/
    3. Passes those most revelant embeddings to an LLM to generate a response, which will be based on the relevant retrievals from actual papers.

2. An "agent" response:
    1. Use a reasoning-capable LLM agent.
    2. Provide an extra response that utilizes the LLM (and web search, if needed).
    3. The agent reasons over the results before returning an answer.


## How to run
- Backend
    - `cd agent`
    - `pip install -r requirements.txt`
    - Create a `.env` file in the `agent` folder and set `OPENAI_API_KEY`
    - `python -m uvicorn main:app --reload`
- Frontend
    - `cd ui`
    - `npm install`
    - `npm run dev`
