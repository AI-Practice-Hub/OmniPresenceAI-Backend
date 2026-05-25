from langchain_openai import AzureChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from app.core.config import settings

# 1. Initialize the LLM
llm = AzureChatOpenAI(
    azure_endpoint=settings.AZURE_OPENAI_ENDPOINT,
    azure_deployment=settings.AZURE_OPENAI_DEPLOYMENT_NAME,
    openai_api_version=settings.AZURE_OPENAI_API_VERSION,
    openai_api_key=settings.AZURE_OPENAI_API_KEY,
)

# 2. Design the Prompt
prompt = ChatPromptTemplate.from_messages([
    ("system", "You are an expert scriptwriter for short, engaging AI avatar videos. "
               "Convert the user's rough idea into a natural, spoken-word script. "
               "Include appropriate pacing, natural pauses, and conversational tone. "
               "Output ONLY the spoken script, without any stage directions."),
    ("user", "{idea}")
])

# 3. Build the Chain
script_chain = prompt | llm | StrOutputParser()

async def generate_script_async(idea: str) -> str:
    """
    Takes a rough idea from the user and generates a spoken-word script using Azure OpenAI.
    """
    # 4. Invoke the chain asynchronously
    return await script_chain.ainvoke({"idea": idea})
