import streamlit as st
import os
from typing import List
import torch
from langchain_core.messages import HumanMessage, AIMessage, ToolMessage

# Configure Streamlit to avoid PyTorch compatibility issues
os.environ["STREAMLIT_SERVER_FILE_WATCHER_TYPE"] = "none"
os.environ["STREAMLIT_SERVER_RUN_ON_SAVE"] = "false"
torch.classes.__path__ = []

# Import the party agent from our app (same directory)
from app import party_agent

def format_message(message):
    """Format different types of messages for display"""
    if hasattr(message, 'content'):
        content = message.content
        
        if hasattr(message, 'tool_calls') and message.tool_calls:
            # This is an AI message with tool calls
            tool_info = []
            for tool_call in message.tool_calls:
                tool_info.append(f"🔧 **Tool:** {tool_call['name']}")
                if 'args' in tool_call:
                    args_str = ", ".join([f"{k}: {v}" for k, v in tool_call['args'].items()])
                    tool_info.append(f"   **Args:** {args_str}")
            return "\n".join(tool_info)
        
        elif hasattr(message, 'name'):
            # This is a tool message
            return f"🔧 **{message.name} Result:**\n{content}"
        
        else:
            # Regular AI or Human message
            return content
    
    return str(message)

def main():
    st.set_page_config(
        page_title="Party Planning Assistant",
        page_icon="🎉",
        layout="wide"
    )
    
    st.title("🎉 Party Planning Assistant")
    st.markdown("Ask me anything about party planning! I can help with guest information, weather, search queries, and more.")
    
    # Initialize session state
    if 'messages' not in st.session_state:
        st.session_state.messages = []
    if 'execution_steps' not in st.session_state:
        st.session_state.execution_steps = []
    
    # Chat input
    user_input = st.chat_input("Enter your party planning question...")
    
    if user_input:
        # Add user message to session state
        st.session_state.messages.append({"role": "user", "content": user_input})
        st.session_state.execution_steps = []
        
        # Create human message
        messages = [HumanMessage(content=user_input)]
        
        # Show processing indicator
        with st.spinner("Processing your request..."):
            try:
                # Stream the agent execution to capture intermediate steps
                execution_steps = []
                
                # Invoke the agent and capture the full response
                response = party_agent.invoke({"messages": messages})
                
                # Extract all messages from the response
                all_messages = response.get('messages', [])
                
                # Process each message for display
                for i, msg in enumerate(all_messages):
                    if hasattr(msg, 'tool_calls') and msg.tool_calls:
                        # AI message with tool calls
                        execution_steps.append({
                            "type": "tool_call",
                            "content": format_message(msg)
                        })
                    elif hasattr(msg, 'name'):
                        # Tool response message
                        execution_steps.append({
                            "type": "tool_response", 
                            "content": format_message(msg)
                        })
                    elif isinstance(msg, AIMessage):
                        # Final AI response
                        execution_steps.append({
                            "type": "final_response",
                            "content": msg.content
                        })
                
                # Store execution steps and final response
                st.session_state.execution_steps = execution_steps
                final_response = all_messages[-1].content if all_messages else "No response generated."
                st.session_state.messages.append({"role": "assistant", "content": final_response})
                
            except Exception as e:
                st.error(f"An error occurred: {str(e)}")
                st.session_state.messages.append({"role": "assistant", "content": f"Sorry, I encountered an error: {str(e)}"})
    
    # Display chat history
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.write(message["content"])
    
    # Display execution process if available
    if st.session_state.execution_steps:
        st.divider()
        
        with st.expander("🔍 View Agent Execution Process", expanded=False):
            for i, step in enumerate(st.session_state.execution_steps):
                if step["type"] == "tool_call":
                    st.markdown("**🤖 Agent Planning:**")
                    st.info(step["content"])
                elif step["type"] == "tool_response":
                    st.markdown("**⚙️ Tool Execution:**")
                    st.success(step["content"])
                elif step["type"] == "final_response":
                    st.markdown("**💭 Final Response:**")
                    st.markdown(step["content"])
                
                if i < len(st.session_state.execution_steps) - 1:
                    st.markdown("---")
    
    # Sidebar with information
    with st.sidebar:
        st.markdown("## 🤖 Agent Capabilities")
        st.markdown("""
        This party planning assistant can help you with:
        
        **🎯 Guest Information**
        - Find guest details by name or relation
        - Search through guest database
        
        **🌤️ Weather Information**
        - Get weather info for locations
        - Plan outdoor events accordingly
        
        **🔍 Web Search**
        - Search for party ideas
        - Find vendors and services
        
        **📊 Hugging Face Hub Stats**
        - Get model statistics
        - Find popular AI models
        """)
        
        st.markdown("---")
        st.markdown("## 💡 Example Questions")
        st.markdown("""
        - "Who are the family members I should invite?"
        - "What's the weather like in New York?"
        - "Search for birthday party decoration ideas"
        - "Find information about guest named Sarah"
        """)
        
        if st.button("Clear Chat History"):
            st.session_state.messages = []
            st.session_state.execution_steps = []
            st.rerun()

if __name__ == "__main__":
    main() 