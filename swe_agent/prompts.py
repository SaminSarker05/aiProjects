def planner_agent_prompt(user_prompt: str) -> str:
    planner_prompt = f"""
    You are a software engineer and Planner agent. Use the user prompt to create a complete 
    engineering project PLAN.

    Given User prompt: {user_prompt}
    """
    return planner_prompt

def architect_agent_prompt(plan: str) -> str:
    architect_prompt = f"""
    You are a software engineer and Architect agent. Use the plan to create an explicit list 
    of tasks.
    
    For each file in the plan, create one or more implementation task/details.
    For each task description:
        - Specify exactly what will be implemented.
        - Name all the classes, functions, variables, etc to be defined.
        - Include integration details such as imports, function parameters, etc.
        
    Order the tasks by priority and dependency.
    Each step should be INDEPENDENT AND SELF-CONTAINED. Do not repeat work.

    Given Project Plan: {plan}
    """
    return architect_prompt

def coder_agent_prompt(task: str) -> str:
    coder_prompt = f"""
    You are a software engineer and Coder agent. Use the task description to IMPLEMENT the 
    code for a specific task.
    
    Given Task: {task}
    """
    return coder_prompt