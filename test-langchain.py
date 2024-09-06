import os
from dotenv import load_dotenv
import logging

from utilities import get_similar_sessions

from langchain_openai import AzureChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.schema import StrOutputParser
from langchain.schema.runnable import Runnable
from langchain.schema.runnable.config import RunnableConfig
from langchain_core.runnables import RunnableLambda
from langchain_core.runnables import RunnablePassthrough

load_dotenv()

logging.basicConfig(level=logging.INFO)

llm = AzureChatOpenAI(
    azure_endpoint=os.environ["AZURE_OPENAI_ENDPOINT"],
    azure_deployment=os.environ["AZURE_OPENAI_CHAT_DEPLOYMENT_NAME"],
    openai_api_version=os.environ["AZURE_OPENAI_API_VERSION"],
)

prompt = ChatPromptTemplate.from_messages(
    [
        (
            "ai",
            """ 
            You are a system assistant who helps users find the right session to watch from the conference, based off the sessions that are provided to you.
            Sessions will be provided in an assistant message in the format of `title|abstract|speakers|start-time|end-time`. You can use only the provided session list to help you answer the user's question.
            If the user ask a question that is not related to the provided sessions, you can respond with a message that you can't help with that question.
            """,
        ),
        (
            "human", """
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

retriever = RunnableLambda(get_similar_sessions).bind() 

rag_chain = {"sessions": retriever, "question": RunnablePassthrough()} | prompt | llm

# result = retriever.invoke("is there any sesison on SQL and AI?")
# print(result)    

#response = rag_chain.invoke("is there any sesison on SQL and AI?")
#print(response.content)

print()

for chunk in rag_chain.stream("how do I learn how to bake bread"):
    print(chunk.content,end="", flush=True)

print()

