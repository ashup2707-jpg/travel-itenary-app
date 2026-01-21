"""
Vector store setup for RAG using Chroma
"""
import chromadb
from typing import List, Dict, Optional
import os
from dotenv import load_dotenv

# Load .env from project root
env_path = os.path.join(os.path.dirname(__file__), '..', '..', '.env')
if os.path.exists(env_path):
    load_dotenv(env_path)
else:
    # Try loading from current directory
    load_dotenv()

class VectorStore:
    """
    Vector store for RAG using Chroma (local) or Pinecone (cloud)
    """
    
    def __init__(self, use_pinecone: bool = False, collection_name: str = "travel_guides"):
        self.use_pinecone = use_pinecone
        self.collection_name = collection_name
        
        if use_pinecone:
            # TODO: Initialize Pinecone client
            # import pinecone
            # pinecone.init(api_key=os.getenv("PINECONE_API_KEY"))
            raise NotImplementedError("Pinecone not yet implemented. Use Chroma for now.")
        else:
            # Use Chroma (local, free) - New API
            # Create persistent client that saves to disk
            db_path = os.path.join(os.path.dirname(__file__), '..', '..', 'chroma_db')
            self.client = chromadb.PersistentClient(path=db_path)
            self.collection = self.client.get_or_create_collection(
                name=collection_name,
                metadata={"hnsw:space": "cosine"}
            )
    
    def add_documents(self, documents: List[Dict]):
        """
        Add documents to vector store
        
        Args:
            documents: List of dicts with 'text', 'metadata', and optionally 'id'
        """
        if not documents:
            return
        
        texts = []
        metadatas = []
        ids = []
        
        for i, doc in enumerate(documents):
            texts.append(doc["text"])
            metadatas.append(doc.get("metadata", {}))
            ids.append(doc.get("id", f"doc_{i}"))
        
        self.collection.add(
            documents=texts,
            metadatas=metadatas,
            ids=ids
        )
    
    def query(
        self,
        query_text: str,
        n_results: int = 5,
        filter_metadata: Optional[Dict] = None
    ) -> List[Dict]:
        """
        Query vector store for similar documents
        
        Args:
            query_text: Query string
            n_results: Number of results to return
            filter_metadata: Optional metadata filter (e.g., {"city": "Jaipur"})
        
        Returns:
            List of similar documents with metadata and citations
        """
        try:
            where = filter_metadata if filter_metadata else None
            
            # Check if collection has documents
            doc_count = self.collection.count()
            if doc_count == 0:
                print(f"   ⚠️  Vector store collection '{self.collection_name}' is empty!")
                return []
            
            results = self.collection.query(
                query_texts=[query_text],
                n_results=min(n_results, doc_count),  # Don't ask for more than available
                where=where
            )
            
            # Format results
            formatted_results = []
            if results.get('documents') and len(results['documents']) > 0 and results['documents'][0]:
                for i in range(len(results['documents'][0])):
                    formatted_results.append({
                        "text": results['documents'][0][i],
                        "metadata": results['metadatas'][0][i] if results.get('metadatas') and results['metadatas'][0] else {},
                        "distance": results['distances'][0][i] if results.get('distances') and results['distances'][0] else None,
                        "id": results['ids'][0][i] if results.get('ids') and results['ids'][0] else None
                    })
            
            return formatted_results
        except Exception as e:
            print(f"   ❌ Error querying vector store: {e}")
            import traceback
            traceback.print_exc()
            return []
    
    def get_collection_stats(self) -> Dict:
        """Get statistics about the collection"""
        count = self.collection.count()
        return {
            "collection_name": self.collection_name,
            "document_count": count
        }


# Test function
if __name__ == "__main__":
    store = VectorStore()
    
    # Test adding documents
    test_docs = [
        {
            "text": "Jaipur is known as the Pink City and is famous for its historic palaces and forts.",
            "metadata": {"city": "Jaipur", "section": "understand", "source": "wikivoyage"},
            "id": "test_1"
        },
        {
            "text": "The Hawa Mahal is a beautiful palace with 953 windows.",
            "metadata": {"city": "Jaipur", "section": "see", "source": "wikivoyage"},
            "id": "test_2"
        }
    ]
    
    print("📦 Adding test documents...")
    store.add_documents(test_docs)
    
    print("🔍 Querying: 'What to see in Jaipur?'")
    results = store.query("What to see in Jaipur?", n_results=2)
    
    for result in results:
        print(f"\n📄 {result['text'][:50]}...")
        print(f"   Metadata: {result['metadata']}")
    
    print(f"\n✅ Collection stats: {store.get_collection_stats()}")
