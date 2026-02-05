from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings

llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash")
llm_general = ChatGoogleGenerativeAI(model="gemini-2.5-flash")


embeddings = GoogleGenerativeAIEmbeddings(model="models/gemini-embedding-001")
