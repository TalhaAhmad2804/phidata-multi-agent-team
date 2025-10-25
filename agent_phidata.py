import os
from typing import Iterator
from dotenv import load_dotenv
import datetime

from phi.agent import Agent, AgentMemory
from phi.model.azure import AzureOpenAIChat
from phi.tools.yfinance import YFinanceTools
from phi.knowledge.pdf import PDFKnowledgeBase, PDFReader
from phi.vectordb.lancedb import LanceDb
from phi.embedder.azure_openai import AzureOpenAIEmbedder
from phi.storage.agent.sqlite import SqlAgentStorage
from phi.memory.db.sqlite import SqliteMemoryDb


load_dotenv()
azure_model = AzureOpenAIChat(
    id=os.getenv("AZURE_OPENAI_MODEL_NAME"),
    api_key=os.getenv("AZURE_OPENAI_KEY"),
    azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
    azure_deployment=os.getenv("AZURE_OPENAI_DEPLOYMENT"),
)

pdf_knowledge_base = PDFKnowledgeBase(
    path="data/",
    vector_db=LanceDb(
        table_name="pdf_stocks",
        uri='./data/',
        embedder=AzureOpenAIEmbedder(
            model=os.getenv("AZURE_EMBEDDING_MODEL"),
            api_key=os.getenv("AZURE_EMBEDDING_KEY"),
            azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
            azure_deployment=os.getenv("AZURE_EMBEDDING_MODEL"),
        )
    ),
    reader=PDFReader(chunk=True),
)

def getCurrentDatetime() -> str:
    return datetime.datetime.now().isoformat()


pdf_knowledge_base.load(recreate=False, upsert=True)

stock_datetime_agent = Agent(
    name="stock datetime agent",
    model=azure_model,
    knowledge=pdf_knowledge_base,
    role="Handle queries about stock/crypto prices and date/time and knowledge base.",
    tools=[YFinanceTools(stock_price=True, historical_prices=True), getCurrentDatetime],
    description="You are a Stocks & Time Bot.",
    instructions=["You only answer three types of queries:",
        "1) Return the current date and time when asked.",
        "2) Return the latest stock (or crypto) price for a given ticker symbol.",
        "3) Retreive information from the knowledge base.",
        "If the user asks anything else, politely decline and say you can only provide date/time or stock prices."
    ],
    markdown=True,
    add_history_to_messages=True,
    num_history_responses=10,
    show_tool_calls=True,
)

general_query_agent = Agent(
    name="general query agent",
    model=azure_model,
    role="Handle all other user questions.",
    description="You are a general query bot.",
    instructions=["Following are the instructions to answer user queries:",
        "1) Return information in structured paragraphs.",
        "2) include details, analysis, and conclusion.",
        "3) Use tables where needed to be in a structured form."
    ],
    markdown=True,
    add_chat_history_to_messages=True,
    show_tool_calls=True,
)

agent_team = Agent(
    model=azure_model,
    name="Agent Team",
    team=[stock_datetime_agent, general_query_agent],
    system_prompt=(
        "You are a creation of Talha Ahmad. Be concise with your information.\n\n"
        "You are a two‑agent system: stock_datetime_agent and general_query_agent.\n"
        "- Route all stock, crypto, or date/time queries to stock_datetime_agent only.\n"
        "- Route all other queries to general_query_agent only."
    ),
    add_chat_history_to_messages=True,
    markdown=True,
    storage=SqlAgentStorage(
        db_file="db/sessions.db",
        table_name="ai_sessions",
    ),
)

def getAgentResponse(msg: str) -> str :
    """
    Directs the Phidata agent on the given user message and return the agent's textual reply.

    Parameters:
        msg (str): The user's input message to send to the agent.

    Returns:
        str: The content of the agent's response if successful.
             If the response object has no 'content' attribute, returns an empty string.
             In case of any exception during agent execution, returns an error message.

    """
    try:
        run = agent_team.run(message=msg)
        if hasattr(run, 'content'):
            return run.content

        return ""
    except Exception as e:
        return "Sorry, I encountered an error while processing your request."
