from typing import TypedDict, Annotated
from langgraph.graph.message import add_messages
from langchain_core.messages import AnyMessage, HumanMessage, AIMessage
from langgraph.prebuilt import ToolNode
from langgraph.graph import START, StateGraph
from langgraph.prebuilt import tools_condition
from langchain_ollama import ChatOllama
from tools import search_tool, weather_info_tool, hub_stats_tool
from retriever import guest_info_tool

# Generate the chat interface, including the tools
llm = "qwen2.5-coder:7b"

chat = ChatOllama(model=llm, verbose=True)

tools = [guest_info_tool, search_tool, weather_info_tool, hub_stats_tool]
chat_with_tools = chat.bind_tools(tools)

# Generate the AgentState and Agent graph
class AgentState(TypedDict):
    messages: Annotated[list[AnyMessage], add_messages]

def assistant(state: AgentState):
    return {
        "messages": [chat_with_tools.invoke(state["messages"])],
    }

## The graph
builder = StateGraph(AgentState)

# Define nodes: these do the work
builder.add_node("assistant", assistant)
builder.add_node("tools", ToolNode(tools))

# Define edges: these determine how the control flow moves
builder.add_edge(START, "assistant")
builder.add_conditional_edges(
    "assistant",
    # If the latest message requires a tool, route to tools
    # Otherwise, provide a direct response
    tools_condition,
)
builder.add_edge("tools", "assistant")
party_agent = builder.compile()

def main():
    """Main function for command-line usage"""
    # Prompt user for input message
    user_input = input("Enter your message: ")
    messages = [HumanMessage(content=user_input)]
    response = party_agent.invoke({"messages": messages})
    print(response['messages'][-1].content)

if __name__ == "__main__":
    main()
