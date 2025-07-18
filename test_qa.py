from qa_chain import QAChain
import os

pdf_path = "sample.pdf"  # Replace with a real PDF file, ensure it exists in the same directory
if os.path.exists(pdf_path):
    print(f"Loading document from {pdf_path}...")
    qa = QAChain()
    chunk_count = qa.load_document(pdf_path)
    print(f"Processed {chunk_count} chunks from {pdf_path}")
    
    question = "what is described in the document" # Example question
    print(f"\nAsking question: '{question}'")
    response = qa.ask_question(question)
    
    print("\nAnswer:", response["answer"])
    print("\nSource Documents (first 300 chars):")
    for i, doc_content in enumerate(response["source_documents"]):
        print(f"- Doc {i+1}: {doc_content[:300]}...") # Print only first 300 chars for brevity
else:
    print(f"Error: PDF file not found at '{pdf_path}'. Please provide a valid PDF file.")