import os
from dotenv import load_dotenv

from utilities import get_similar_sessions

from langchain_openai import AzureChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.schema import StrOutputParser
from langchain.schema.runnable import Runnable
from langchain.schema.runnable.config import RunnableConfig

import chainlit as cl

load_dotenv()

@cl.step(type="tool", name="GetSimilarSessions")
async def GetSimilarSessions(search_text: str) -> str:
    return await cl.make_async(get_similar_sessions)(search_text)

@cl.on_chat_start
async def on_chat_start():
    model = AzureChatOpenAI(
        openai_api_version=os.environ["AZURE_OPENAI_API_VERSION"],
        azure_deployment=os.environ["AZURE_OPENAI_CHAT_DEPLOYMENT_NAME"],
        streaming=True
    )
    prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                """ 
                You are a system assistant who helps users find the right session to watch from the conference, based off the sessions that are provided to you.
                Sessions will be provided in an assistant message in the format of `title|abstract|speakers|start-time|end-time`. You can use only the provided session list to help you answer the user's question.
                If the user ask a question that is not related to the provided sessions, you can respond with a message that you can't help with that question.
                Your aswer must have the session title, a short very short summary of the abstract, the speakers, the start time, and the end time.
                """,
            ),
            (
                "system", """
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
    runnable = prompt | model | StrOutputParser()
    cl.user_session.set("runnable", runnable)    

@cl.on_message
async def on_message(message: cl.Message):
    runnable = cl.user_session.get("runnable")  # type: Runnable

    # Use a chainlit tool to get similar sessions
    # as another option to langchain integration
    similar_sessions = await GetSimilarSessions(message.content);

    msg = cl.Message(content="")
    input = {"question": message.content, "sessions": similar_sessions}

    for chunk in await cl.make_async(runnable.stream)(
        input = input,
        config = RunnableConfig(callbacks=[cl.LangchainCallbackHandler()]),
    ):
        await msg.stream_token(chunk)

    await msg.send()
