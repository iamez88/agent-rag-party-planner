import datasets
from langchain.docstore.document import Document
from langchain.tools import Tool
from sentence_transformers import SentenceTransformer, util
import numpy as np


# Load the dataset
guest_dataset = datasets.load_dataset("agents-course/unit3-invitees", split="train")

# Convert dataset entries into Document objects
docs = [
    Document(
        page_content="\n".join([
            f"Name: {guest['name']}",
            f"Relation: {guest['relation']}",
            f"Description: {guest['description']}",
            f"Email: {guest['email']}"
        ]),
        metadata={"name": guest["name"]}
    )
    for guest in guest_dataset
]

# Initialize sentence transformer model directly
model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

# Pre-compute embeddings for all documents
doc_texts = [doc.page_content for doc in docs]
doc_embeddings = model.encode(doc_texts, convert_to_tensor=True)

def extract_text(query: str) -> str:
    """Retrieves detailed information about guests based on their name or relation using semantic search."""
    # Encode the query
    query_embedding = model.encode(query, convert_to_tensor=True)
    
    # Calculate similarities
    similarities = util.cos_sim(query_embedding, doc_embeddings)[0]
    
    # Get top 3 most similar documents
    top_k = 3
    top_indices = similarities.topk(top_k).indices
    
    # Return the content of top matching documents
    results = [docs[idx].page_content for idx in top_indices]
    
    if results:
        return "\n\n".join(results)
    else:
        return "No matching guest information found."

guest_info_tool = Tool(
    name="guest_info_retriever",
    func=extract_text,
    description="Retrieves detailed information about guests based on their name or relation using semantic search."
)

