from dotenv import load_dotenv
from typing import Annotated, Literal, TypedDict, List
from prompts import planner_agent_prompt, architect_agent_prompt, coder_agent_prompt
from schemas import *
from utils import *
from langgraph.graph import StateGraph, END
from langgraph.prebuilt import create_react_agent
from langchain_openai import ChatOpenAI

load_dotenv()

llm = ChatOpenAI(model='gpt-4.1-nano')

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
    coder_state = state.get("coder_state")
    if coder_state is None:
        coder_state = CoderState(architect=state["architect"], curr_task_ind=0)
    
    list_of_tasks = coder_state.architect.tasks
    if coder_state.curr_task_ind >= len(list_of_tasks):
        return {"coder_state": coder_state, "status": "DONE"}

    curr_task = list_of_tasks[coder_state.curr_task_ind]    
    existing_code = read_file.run(curr_task.path)
    user_prompt = (
        f"task: {curr_task.task_description}"
        f"file: {curr_task.path}"
        f"existing_code: {existing_code}"
        "use write_file(path, content) to modify the file"
    )
    system_prompt = coder_agent_prompt()
    
    monkey_tools = [read_file, write_file, ls_files, get_cwd]
    swe_agent = create_react_agent(model=llm,  tools=monkey_tools)
    swe_agent.invoke({"messages": [{"role": "system", "content": system_prompt}, {"role": "user", "content": user_prompt} ]})
    
    coder_state.curr_task_ind += 1
    return {"coder_state": coder_state, "status": "IN_PROGRESS"}

if __name__ == "__main__":
    graph = StateGraph(AgentState)
    graph.add_node("plan_monkey", planner_agent)
    graph.add_node("architect_monkey", architect_agent)
    graph.add_node("code_monkey", code_monkey_agent)
    
    graph.set_entry_point("plan_monkey")
    graph.add_edge("plan_monkey", "architect_monkey")
    graph.add_edge("architect_monkey", "code_monkey")
    graph.add_conditional_edges(
        "code_monkey",
        lambda state: "END" if state.get("status") == "DONE" else "code_monkey",
        {"END": END, "code_monkey": "code_monkey"}
    )
    
    swe_agent = graph.compile()
    user_prompt = "Create a simple tic tac toe web application."
    res = swe_agent.invoke({"user_prompt": user_prompt})
