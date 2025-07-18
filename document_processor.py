import fitz  # PyMuPDF
from langchain.text_splitter import RecursiveCharacterTextSplitter
from sentence_transformers import SentenceTransformer
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
        self.text_chunks = []
        self.embeddings = None

    def process_pdf(self, pdf_path: str) -> tuple[int, list[str], np.ndarray]:
        """Extract text from PDF and generate embeddings."""
        # Extract text from PDF
        doc = fitz.open(pdf_path)
        text = ""
        for page in doc:
            text += page.get_text()
        doc.close()

        # Split text into chunks
        self.text_chunks = self.text_splitter.split_text(text)

        # Generate embeddings
        self.embeddings = self.embedder.encode(self.text_chunks, convert_to_numpy=True)

        return len(self.text_chunks), self.text_chunks, self.embeddings