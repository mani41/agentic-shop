from langgraph.graph import StateGraph, START, END

from app.graph.nodes import evaluation_node
from app.graph.state import ShoppingState
from app.graph.agent_node import agent_node
from app.graph.tool_node import tool_node
from app.graph.routing import should_continue


def build_graph():

    graph = StateGraph(ShoppingState)

    graph.add_node(
        "agent",
        agent_node
    )

    graph.add_node(
        "tools",
        tool_node
    )

    graph.add_node(
        "evaluation",
        evaluation_node
    )

    graph.add_edge(
        START,
        "agent"
    )

    graph.add_conditional_edges(
        "agent",
        should_continue,
        {
            "tools": "tools",
            "evaluate": "evaluation",
        }
    )

    graph.add_edge(
        "tools",
        "agent"
    )

    graph.add_edge(
        "evaluation",
        END
    )

    return graph.compile()