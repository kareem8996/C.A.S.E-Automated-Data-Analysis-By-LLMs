from langchain_groq import ChatGroq
from dotenv import load_dotenv
from langgraph.graph import MessagesState
from ...Database.mainDatabase import create_new_chat_id, clear_history, get_model_chat_history, update_st_chat_history

"""
Chatbot.py

This module sets up a language model to act as a chatbot with memory, responding to the user input.

Dependencies:
- langchain_groq
- dotenv

Usage:
1. Ensure that the required dependencies are installed.
2. Set up the necessary environment variables in a .env file.
3. Use the caller_node function to invoke tools based on the state messages.

Functions:
- load_dotenv: Loads environment variables from a .env file.
- caller_node: Invokes tools based on the state messages and returns the response.

Variables:
- ChatID : ID associated with the chat session for a specific user.
- chat_history: The chat history for the current chat session.
- systemprompt: The system prompt.
- model: An instance of Grog Llama3.
- chatBaseTemplate: A template for the chat history, ensuring that the system prompt is passed to the model in it's appropriate place.
"""

load_dotenv()
systemPrompt = "You are a chatbot"
model = ChatGroq(model = "llama3-8b-8192")
chatID = create_new_chat_id("Mohamed")
chat_history = []
chatBaseTemplate = [{ "role" : "system", "content" : systemPrompt}]


def call_model(state):
    input = state["messages"]    
    if get_model_chat_history(chatID) is not []:
        chat_history = chatBaseTemplate + get_model_chat_history(chatID)
    else : 
        chat_history = chatBaseTemplate
    modelInput = chat_history + [{"role" : "human", "content" :  input[-1].content}]
    print(modelInput)
    response = model.invoke(modelInput)
    formatted_response = [{"role" : "ai", "content" :  response.content}]
    lastConv = []
    lastConv.append([modelInput[-1]])
    lastConv.append(formatted_response)
    print(lastConv)
    update_st_chat_history(chatID, lastConv)
    return {"messages": response}
