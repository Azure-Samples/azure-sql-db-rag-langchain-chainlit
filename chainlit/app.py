import os
from dotenv import load_dotenv

from utilities import get_similar_sessions

from langchain_openai import AzureChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.schema import StrOutputParser
from langchain.schema.runnable import Runnable
from langchain.schema.runnable.config import RunnableConfig
from langchain_core.runnables import RunnableLambda, RunnablePassthrough

import chainlit as cl

load_dotenv()

@cl.on_chat_start
async def on_chat_start():
    openai = AzureChatOpenAI(
        openai_api_version=os.environ["AZURE_OPENAI_API_VERSION"],
        azure_deployment=os.environ["AZURE_OPENAI_CHAT_DEPLOYMENT_NAME"],
        streaming=True
    )
    prompt = ChatPromptTemplate.from_messages(
        [
            (
                "ai",
                """ 
                You are a system assistant who helps users find the right session to watch from the conference, based off the sessions that are provided to you.
                Sessions will be provided in an assistant message in the format of `title|abstract|speakers|start-time|end-time`. You can use only the provided session list to help you answer the user's question.
                If the user ask a question that is not related to the provided sessions, you can respond with a message that you can't help with that question.
                Your aswer must have the session title, a very short summary of the abstract, the speakers, the start time, and the end time.
                """,
            ),
            (
                "human",
                """
                The sessions available at the conference are the following: 
                {sessions}                
                """
            ),
            (
                "human",                
                "{question}"
            ),
        ]
    )

    # Use an agent retriever to get similar sessions
    retriever = RunnableLambda(get_similar_sessions, name="GetSimilarSessions").bind() 

    runnable = {"sessions": retriever, "question": RunnablePassthrough()} | prompt | openai | StrOutputParser()
    cl.user_session.set("runnable", runnable)    

@cl.on_message
async def on_message(message: cl.Message):
    runnable = cl.user_session.get("runnable")  # type: Runnable
    
    response_message = cl.Message(content="")

    for chunk in await cl.make_async(runnable.stream)(
        input=message.content,
        config=RunnableConfig(callbacks=[cl.LangchainCallbackHandler()]),
    ):
        await response_message.stream_token(chunk)

    await response_message.send()
