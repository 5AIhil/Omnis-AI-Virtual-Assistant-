import os
from typing import TypedDict, Annotated, Sequence
from langchain_core.messages import BaseMessage
from langchain_groq import ChatGroq
from langgraph.graph import StateGraph, END, START
from langgraph.prebuilt import ToolNode
import operator

class AgentState(TypedDict):
    messages: Annotated[Sequence[BaseMessage], operator.add]

def create_agent_graph(tools):
    model_name = os.getenv("GROQ_MODEL_NAME", "llama-3.3-70b-versatile")
    llm = ChatGroq(model=model_name)
    
    if tools:
        llm = llm.bind_tools(tools)
    
    def call_model(state: AgentState):
        messages = state["messages"]
        response = llm.invoke(messages)
        return {"messages": [response]}
        
    def should_continue(state: AgentState):
        messages = state["messages"]
        last_message = messages[-1]
        if hasattr(last_message, "tool_calls") and last_message.tool_calls:
            return "tools"
        return END

    workflow = StateGraph(AgentState)
    workflow.add_node("agent", call_model)
    
    if tools:
        tool_node = ToolNode(tools)
        workflow.add_node("tools", tool_node)
        workflow.add_edge("tools", "agent")
        
    workflow.add_edge(START, "agent")
    
    if tools:
        workflow.add_conditional_edges("agent", should_continue, ["tools", END])
    else:
        workflow.add_edge("agent", END)
        
    # We can add memory here later if we want persistent sessions
    # using langgraph.checkpoint.memory.MemorySaver
    return workflow.compile()
