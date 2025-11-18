from pydantic import BaseModel, Field, ConfigDict
from typing import Literal, TypedDict, Optional

class FileSchema(BaseModel):
    path: str = Field(description="Location and path of file to create or modify.")
    purpose: str = Field(description="Purpse of this file.")

class PlanSchema(BaseModel):
    name: str = Field(description="Name of application to build.")
    description: str = Field(description="One sentence description of application to build.")
    tech_stack : str = Field(description="The tech stack that will be used to build the application.")
    features: list[str] = Field(description="List of features that will be included in the application.")
    files: list[FileSchema] = Field(description="List of files to create or modify during the build process.")
    
    def __str__(self):
        return f"""
            name: {self.name}
            description: {self.description}
            tech Stack: {self.tech_stack}
            features: {self.features}
            files: {self.files}
        """
    
class TaskSchema(BaseModel):
    path: str = Field(description="The path of file to modify.")
    task_description: str = Field(description="Detailed description of the task to perform on the file.")
    
class ArchitectSchema(BaseModel):
    tasks: list[TaskSchema] = Field(description="List of tasks to perform during the build process.")
    # model_config = ConfigDict(extra="allow")  # allow extra fields to be later added

class CoderState(BaseModel):
    architect: ArchitectSchema = Field(description="List of implementation tasks to perform during the build process.")
    curr_task_ind: int = Field(0, description="Index of current task being worked on.")
    curr_file_content: Optional[str] = Field(None, description="Current file content being worked on.")

class AgentState(TypedDict):
    user_prompt: str
    plan: PlanSchema
    architect: ArchitectSchema
    coder_state: Optional[CoderState]
    status: Literal["DONE", "IN_PROGRESS", "ERROR"]
    