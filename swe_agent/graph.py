from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
from prompts import planner_agent_prompt, architect_agent_prompt
from schemas import PlanSchema, ArchitectSchema

from typing import Annotated, Literal, TypedDict, List
from langgraph.graph import StateGraph, START, END

load_dotenv()

llm = ChatOpenAI(model='gpt-4.1-nano')

class AgentState(TypedDict):
    user_prompt: str
    plan: PlanSchema
    architect: ArchitectSchema

def planner_agent(state: AgentState) -> AgentState:
    user_prompt: str = state["user_prompt"]
    prompt = planner_agent_prompt(user_prompt)
    response: PlanSchema = llm.with_structured_output(PlanSchema).invoke(prompt)
    if response is None:
        raise Exception("Planner Agent: Unable to generate plan.")
    
    return {"plan": response}

def architect_agent(state: AgentState) -> AgentState:
    plan_str = str(state["plan"])
    prompt = architect_agent_prompt(plan_str)
    response = llm.with_structured_output(ArchitectSchema).invoke(prompt)
    if response is None:
        raise Exception("Architect Agent: Unable to generate tasks.")
    
    return {"architect": response}

if __name__ == "__main__":
    graph = StateGraph(AgentState)
    graph.add_node("planner", planner_agent)
    graph.add_node("architect", architect_agent)
    graph.set_entry_point("planner")
    graph.add_edge("planner", "architect")
    
    swe_agent = graph.compile()
    user_prompt = "Create a simple calculator web application"
    res = swe_agent.invoke({"user_prompt": user_prompt})
    
    print(res)
