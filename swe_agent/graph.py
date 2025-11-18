from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
from prompts import planner_agent_prompt, architect_agent_prompt, coder_agent_prompt
from schemas import PlanSchema, ArchitectSchema

from typing import Annotated, Literal, TypedDict, List
from langgraph.graph import StateGraph

load_dotenv()

llm = ChatOpenAI(model='gpt-4.1-nano')

class AgentState(TypedDict):
    user_prompt: str
    plan: PlanSchema
    architect: ArchitectSchema
    code: str

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

def code_monkey_agent(state: AgentState) -> AgentState:
    list_of_tasks = state["architect"].tasks
    i = 0
    curr_task = list_of_tasks[i].task_description
    prompt = coder_agent_prompt(curr_task)
    response = llm.invoke(prompt)
    return {"code": response.content}

if __name__ == "__main__":
    graph = StateGraph(AgentState)
    graph.add_node("plan_monkey", planner_agent)
    graph.add_node("architect_monkey", architect_agent)
    graph.add_node("code_monkey", code_monkey_agent)
    
    graph.set_entry_point("plan_monkey")
    graph.add_edge("plan_monkey", "architect_monkey")
    graph.add_edge("architect_monkey", "code_monkey")
    
    swe_agent = graph.compile()
    user_prompt = "Create a simple tic tac toe web application."
    res = swe_agent.invoke({"user_prompt": user_prompt})
    
    print(res["code"])
