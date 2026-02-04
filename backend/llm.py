from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI

load_dotenv()

llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash-lite")
llm_general = ChatGoogleGenerativeAI(model="gemini-2.5-flash-lite")
