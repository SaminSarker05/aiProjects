from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
from pydantic import BaseModel, Field

load_dotenv()

llm = ChatOpenAI(model='gpt-4.1-nano')

class FileSchema(BaseModel):
    path: str = Field(description="Location and path of file to create or modify.")
    purpose: str = Field(description="Purpse of this file.")
    
class PlanSchema(BaseModel):
    name: str = Field(description="Name of application to build.")
    description: str = Field(description="One sentence description of application to build.")
    tech_stack : str = Field(description="The tech stack that will be used to build the application.")
    features: list[str] = Field(description="List of features that will be included in the application.")
    files: list[File] = Field(description="List of files to create or modify during the build process.")

if __name__ == "__main__":
    response = llm.invoke("who was the first preseident of bangladesh? answer in one sentence.")
    print(response.content)