# 🎉 Agentic RAG Party Planner

An intelligent AI agent that helps you plan the perfect party using **Agentic RAG** with LangGraph. The agent combines semantic search over guest information with various tools for comprehensive party planning assistance.

[![Demo Video](media/agentic_rag_demo.mp4)](https://github.com/user-attachments/assets/a6f9b548-7267-4839-a1e4-089f2e866b10)

## ✨ Core Features

- 🎯 **Guest Information Retrieval**: Semantic search over guest database
- 🌤️ **Weather Information**: Location-based weather updates  
- 🔍 **Web Search**: Find party ideas, vendors, and services
- 📊 **Hugging Face Hub Stats**: AI model information and statistics
- 🖥️ **Interactive Web Interface**: Streamlit frontend with execution visualization
- 🤖 **CLI Interface**: Command-line access for quick queries

## 📁 Project Structure

```
agentic-rag-party-planner/
├── src/
│   ├── app.py              # Main agent logic and CLI interface
│   ├── frontend.py         # Streamlit web interface
│   ├── tools.py            # Tool implementations
│   └── retriever.py        # RAG system for guest information
├── .streamlit/
│   └── config.toml         # Streamlit configuration
├── requirements.txt        # Python dependencies
├── .gitignore             # Git ignore rules
└── README.md              # This file
```

## 🛠️ Available Tools

| Tool | Description | Use Cases |
|------|-------------|-----------|
| **Guest Info Retriever** | Semantic search over guest database | "Find guests who are family members", "Who is Sarah?" |
| **Weather Info** | Location-based weather information | "What's the weather in New York?", "Check weather for outdoor party" |
| **Web Search** | DuckDuckGo search integration | "Birthday party decoration ideas", "Find local caterers" |
| **Hub Stats** | Hugging Face model statistics | "Most popular models by author", "AI model information" |

## 🔧 Technical Details

### Agent Architecture
The agent uses LangGraph's StateGraph to orchestrate tool usage:
1. **Human Input** → **Assistant** (LLM reasoning)
2. **Tool Selection** → **Tool Execution** → **Assistant** (results processing)
3. **Final Response** generation

### RAG Implementation
- **Dataset**: Pre-loaded guest information from Hugging Face datasets
- **Embeddings**: sentence-transformers/all-MiniLM-L6-v2
- **Search**: Cosine similarity with top-k retrieval
- **Documents**: Structured guest profiles with metadata

## 🚀 Future Changes

### MCP (Model Context Protocol) Integration
- **Standardized Tool Interface**: Replace current custom tool implementations with MCP-compatible tools
- **Enhanced Capabilities**: Connect to external services like calendar APIs, restaurant booking systems, and event management platforms
- **Real-time Data**: Connect to live APIs for weather, traffic, and venue availability

### Collecting Real World Data
- Currently using a dummy data for the guest database
- Next step is to create a database representative of the real-world guest population. Guests may include:
    - Athletes such as Lebron James, 
    - Celebrities such as Tom Cruise, Lady Gaga and Kim Kardashian
    - AI Influencers such as Andrew Ng, Yann LeCun
- Agent will be able to communicate at a deeper level, facilitating a more personalized experience.

This will make the agent more extensible and capable of handling real-world party planning scenarios with live data integration.


