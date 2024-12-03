import os
from dotenv import load_dotenv

from typing import Annotated, Literal, TypedDict

from langchain_openai import AzureChatOpenAI

from langchain.schema.runnable.config import RunnableConfig
from langchain_core.messages import SystemMessage, HumanMessage

from langchain_core.messages import HumanMessage
from langchain_core.tools import tool
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import END, START, StateGraph, MessagesState
from langgraph.prebuilt import ToolNode

from utilities import get_similar_sessions

import chainlit as cl

load_dotenv()

tools = [get_similar_sessions]
model = AzureChatOpenAI(openai_api_version=os.environ["AZURE_OPENAI_API_VERSION"], azure_deployment=os.environ["AZURE_OPENAI_CHAT_DEPLOYMENT_NAME"])
model = model.bind_tools(tools)

def should_continue(state: MessagesState) -> Literal["tools", END]:
    messages = state["messages"]
    last_message = messages[-1]
    # If the LLM makes a tool call, then we route to the "tools" node
    if last_message.tool_calls:
        return "tools"
    # Otherwise, we stop (reply to the user)
    return END

def call_model(state: MessagesState):
    messages = state["messages"]
    response = model.invoke(messages)
    # We return a list, because this will get added to the existing list
    return {"messages": [response]}

tool_node = ToolNode(tools=tools)

workflow = StateGraph(MessagesState)

workflow.add_node("agent", call_model)
workflow.add_node("tools", tool_node)

workflow.add_edge(START, "agent")

workflow.add_conditional_edges("agent", should_continue)

workflow.add_edge("tools", "agent")

checkpointer = MemorySaver()

graph = workflow.compile(checkpointer=checkpointer)

@cl.on_message
async def on_message(msg: cl.Message):
    config = {"configurable": {"thread_id": cl.context.session.id}}
    final_answer = cl.Message(content="")
    
    for msg, metadata in await cl.make_async(graph.stream)(
        {"messages": [HumanMessage(content=msg.content)]}, 
        stream_mode="messages", 
        config=RunnableConfig(callbacks=[cl.LangchainCallbackHandler()], **config)
        ):        
            if metadata["langgraph_node"] == "agent":
                await final_answer.stream_token(msg.content)

    await final_answer.send()

