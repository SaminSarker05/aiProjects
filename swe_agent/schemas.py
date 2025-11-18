
from pydantic import BaseModel, Field

class FileSchema(BaseModel):
    path: str = Field(description="Location and path of file to create or modify.")
    purpose: str = Field(description="Purpse of this file.")

class PlanSchema(BaseModel):
    name: str = Field(description="Name of application to build.")
    description: str = Field(description="One sentence description of application to build.")
    tech_stack : str = Field(description="The tech stack that will be used to build the application.")
    features: list[str] = Field(description="List of features that will be included in the application.")
    files: list[FileSchema] = Field(description="List of files to create or modify during the build process.")
    
    