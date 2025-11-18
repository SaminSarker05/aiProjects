from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
from prompts import planner_agent_prompt
from schemas import PlanSchema

from typing import Annotated, Literal, TypedDict, List
from langgraph.graph import StateGraph, START, END

load_dotenv()

llm = ChatOpenAI(model='gpt-4.1-nano')

class AgentState(TypedDict):
    user_prompt: str

def planner_agent(state: AgentState) -> AgentState:
    user_prompt = state["user_prompt"]
    prompt = planner_agent_prompt(user_prompt)
    return llm.with_structured_output(PlanSchema).invoke(prompt)

if __name__ == "__main__":
    graph = StateGraph(AgentState)
    graph.add_node("planner", planner_agent)
    
    graph.set_entry_point("planner")
    graph.set_finish_point("planner")
    
    swe_agent = graph.compile()
    res = swe_agent.invoke({"user_prompt": "Create a simple calculator web application"})
    
    print(res)