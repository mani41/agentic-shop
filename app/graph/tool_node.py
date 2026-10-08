from langgraph.prebuilt import ToolNode

from app.tools.product_tools import search_products_tool


tool_node = ToolNode([
    search_products_tool
])