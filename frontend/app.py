from dotenv import load_dotenv

load_dotenv()


from components import init_session, render_chat, render_sidebar

init_session()
render_sidebar()
render_chat()
