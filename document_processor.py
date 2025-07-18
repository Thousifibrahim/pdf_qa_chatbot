import fitz  # PyMuPDF
from langchain.text_splitter import RecursiveCharacterTextSplitter
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np

class DocumentProcessor:
    def __init__(self):
        # Initialize text splitter
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200,
            length_function=len
        )
        # Initialize embedding model
        self.embedder = SentenceTransformer('all-MiniLM-L6-v2')
        # Initialize FAISS index
        self.dimension = 384  # Dimension of all-MiniLM-L6-v2 embeddings
        self.index = faiss.IndexFlatL2(self.dimension)
        self.text_chunks = []

    def process_pdf(self, pdf_path):
        """Extract text from PDF and create FAISS index."""
        # Extract text from PDF
        doc = fitz.open(pdf_path)
        text = ""
        for page in doc:
            text += page.get_text()
        doc.close()

        # Split text into chunks
        self.text_chunks = self.text_splitter.split_text(text)

        # Generate embeddings
        embeddings = self.embedder.encode(self.text_chunks, convert_to_numpy=True)

        # Add embeddings to FAISS index
        self.index.add(embeddings.astype(np.float32))

        return len(self.text_chunks)

    def search(self, query, k=3):
        """Search for relevant document chunks based on query."""
        # Generate embedding for the query
        query_embedding = self.embedder.encode([query], convert_to_numpy=True).astype(np.float32)
        # Search FAISS index
        distances, indices = self.index.search(query_embedding, k)
        # Retrieve relevant text chunks
        results = [self.text_chunks[idx] for idx in indices[0]]
        return results