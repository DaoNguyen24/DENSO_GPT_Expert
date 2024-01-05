import openai
from pydantic import BaseModel
from langchain.agents import tool
from answering import Response
from history_retrive import retrive_history


@tool
def get_history(query:str)-> str:
 """Search for history of a machine"""
 return retrive_history(query=query)

@tool
def get_instruction(query:str)->str:
    """Use when you want to solve for a problem of a machine"""
    return Response(query=query)

