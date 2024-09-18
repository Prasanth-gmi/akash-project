from crewai import Agent, Crew, Task
from langchain_groq import ChatGroq
from tools.git import github_repository_tool
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import requests
from fastapi.openapi.docs import get_swagger_ui_html
from fastapi.responses import RedirectResponse
app = FastAPI()
my_llm = ChatGroq(
        api_key="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",
        model="llama3-8b-8192",
    )
class PostCreateRequest(BaseModel):
    repo_name: str
    description: str
    file_name: str
    local_file_path: str

@app.get("/", include_in_schema=False)
async def custom_docs():
    return get_swagger_ui_html(openapi_url="/openapi.json", title="FastAPI Documentation")
@app.post("/gitrepo/create/")
async def create_post(request: PostCreateRequest):
    repo_name = request.repo_name
    description = request.description
    file_name = request.file_name
    local_file_path = request.local_file_path
    # repo_name = input("Enter the repo name : ")
    # description = input("Enter the description name : ")
    # file_name = input("Enter the file name : ")
    # local_file_path = input("Enter the local file path : ")
    ScrumMaster = Agent(
        role="Scrum Master",
        goal=f"Create a new repository on GitHub named '{repo_name}' with the provided description and push a file to it.",
        backstory="You are a Scrum Master with excellent knowledge in managing repositories on GitHub. Your task is to create a new repository and push a file to it using the provided information.",
        llm=my_llm,
        verbose=True,
        allow_delegation=False,
    )
    scrum_master_task = Task(
        description=f"Create a new repository on GitHub named '{repo_name}' with the description '{description}' and push the file '{file_name}' to it.",
        expected_output=f"A confirmation message that a new repository on GitHub with the name '{repo_name}' has been created and the file '{file_name}' has been pushed to it.",
        agent=ScrumMaster,
        tools=[github_repository_tool],
    )
    crew = Crew(
        agents=[ScrumMaster], 
        tasks=[scrum_master_task], 
        verbose=True
    )
    result = crew.kickoff()
    print(result)