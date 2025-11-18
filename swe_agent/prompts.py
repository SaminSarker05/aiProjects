
def planner_agent_prompt(user_prompt: str) -> str:
    llm_prompt = f"""
    You are a software engineer and Planner agent. Use the user prompt to create a complete engineering
    project PLAN.

    User prompt: {user_prompt}
    """
    return llm_prompt