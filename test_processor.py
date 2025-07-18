from document_processor import DocumentProcessor
import os

# Create a sample PDF or use an existing one
pdf_path = "sample.pdf"  # Replace with a real PDF file
if os.path.exists(pdf_path):
    processor = DocumentProcessor()
    chunk_count = processor.process_pdf(pdf_path)
    print(f"Processed {chunk_count} chunks")
    results = processor.search("What is the main topic?")
    print("Search results:", results)
else:
    print("Please provide a valid PDF file")