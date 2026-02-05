from .calculator import calculator
from .rag import rag_tool
from .search import search_tool
from .stocks import get_stock_price

TOOLS = [search_tool, calculator, get_stock_price, rag_tool]
