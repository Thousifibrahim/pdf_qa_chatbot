import torch
from typing import Any, List, Optional

# LangChain components
from langchain.chains import RetrievalQA
from langchain_community.vectorstores import FAISS
from langchain_huggingface.embeddings import HuggingFaceEmbeddings
from langchain_core.language_models.llms import BaseLLM
from langchain_core.callbacks import CallbackManagerForLLMRun
from langchain_core.outputs import LLMResult, Generation # Ensure these are imported

# Hugging Face transformers pipeline
from transformers import pipeline

# Local modules
from document_processor import DocumentProcessor

# --- CustomHuggingFacePipeline (LLM Wrapper) ---
class CustomHuggingFacePipeline(BaseLLM):
    pipeline: Any

    def __init__(self, pipeline: Any, **kwargs: Any):
        super().__init__(pipeline=pipeline, **kwargs)

    @property
    def _llm_type(self) -> str:
        return "custom_huggingface_pipeline"

    def _generate(
        self,
        prompts: List[str],
        stop: Optional[List[str]] = None,
        run_manager: Optional[CallbackManagerForLLMRun] = None,
        **kwargs: Any,
    ) -> LLMResult:
        """
        Generates responses using the Hugging Face pipeline.
        Parses LangChain's standard QA prompt to extract question and context.
        """
        list_of_generations = []

        for prompt_str in prompts: # Renamed 'prompt' to 'prompt_str' to avoid confusion with the pipeline's 'prompt' dict
            question = ""
            context = ""

            # --- Refined Prompt Parsing Logic ---
            # Look for the "Question:" marker. Everything before it is context.
            # Everything after it (and before "Helpful Answer:") is the question.
            try:
                # Split the prompt by "Question:"
                parts = prompt_str.split("Question:", 1)
                if len(parts) > 1:
                    context_part = parts[0].strip()
                    question_and_answer_part = parts[1].strip()

                    # Extract the question (before "Helpful Answer:")
                    q_parts = question_and_answer_part.split("Helpful Answer:", 1)
                    if len(q_parts) > 0: # Question should be the first part
                        question = q_parts[0].strip()
                    
                    # Clean up the context part: remove the initial instruction and "context:" label
                    # Example: "Use the following pieces of context to answer the question at the end.\ncontext:\n..."
                    # Or: "context:\n..."
                    if context_part.startswith("Use the following pieces of context to answer the question at the end."):
                        context = context_part[len("Use the following pieces of context to answer the question at the end."):].replace("context:", "").strip()
                    elif context_part.startswith("context:"):
                         context = context_part[len("context:"):].strip()
                    else:
                        # Fallback if no specific instruction or "context:" prefix is found
                        context = context_part.strip()
                else:
                    # If "Question:" not found, assume the entire prompt is a simple question
                    question = prompt_str.strip()
                    context = "" # No explicit context found
                
                # Further refine context: remove "Document(page_content=" if present from LangChain
                # Sometimes LangChain might put Document objects string representation directly.
                if context.startswith("Document(page_content='"):
                    context = context[len("Document(page_content='"):].rsplit("')", 1)[0] # Remove prefix and suffix

            except Exception as e:
                # Log or print a warning, but still attempt to answer
                print(f"Warning: Complex prompt parsing failed: {e}. Attempting fallback.")
                question = prompt_str.split("Question:", 1)[-1].split("Helpful Answer:", 1)[0].strip() if "Question:" in prompt_str else prompt_str
                context = prompt_str.split("Question:", 1)[0].replace("Use the following pieces of context to answer the question at the end.", "").replace("context:", "").strip() if "Question:" in prompt_str else ""

            # Ensure context and question are not empty or just whitespace
            if not question:
                print(f"Warning: Extracted question is empty from prompt: {prompt_str[:100]}...")
                answer_text = "I couldn't identify a clear question to answer."
            else:
                try:
                    # Call the transformers pipeline
                    # Ensure context is a string, even if empty
                    qa_input = {"question": question, "context": context if context else ""}
                    result = self.pipeline(qa_input)
                    answer_text = result["answer"]
                except Exception as e:
                    print(f"Error during Hugging Face pipeline inference: {e}")
                    answer_text = f"An internal error occurred: {e}. Could not generate answer."

            list_of_generations.append([Generation(text=answer_text)])

        return LLMResult(generations=list_of_generations)


    def invoke(self, input: str, config: Optional[dict] = None, **kwargs: Any) -> str:
        llm_result = self._generate([input], **kwargs)
        if llm_result.generations and llm_result.generations[0] and llm_result.generations[0][0]:
            return llm_result.generations[0][0].text
        return "Error: Could not get a valid response from the LLM."


# --- QAChain Class ---
class QAChain:
    def __init__(self):
        self.doc_processor = DocumentProcessor()
        # Ensure HuggingFaceEmbeddings import is correct as per earlier fix
        self.embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
        self.qa_pipeline = pipeline(
            "question-answering",
            model="distilbert-base-cased-distilled-squad",
            tokenizer="distilbert-base-cased-distilled-squad",
            device=0 if torch.cuda.is_available() else -1
        )
        self.llm = CustomHuggingFacePipeline(pipeline=self.qa_pipeline)
        self.qa_chain = None
        self.vector_store = None

    def load_document(self, pdf_path: str) -> int:
        chunk_count, texts, embeddings = self.doc_processor.process_pdf(pdf_path)
        self.vector_store = FAISS.from_texts(texts, self.embeddings)
        
        # Important: Ensure the prompt template is suitable for your HF QA model
        # Using "stuff" chain type, which puts all context into one prompt.
        # Default prompt template works fine if parsing in _generate is correct.
        self.qa_chain = RetrievalQA.from_chain_type(
            llm=self.llm,
            chain_type="stuff",
            retriever=self.vector_store.as_retriever(search_kwargs={"k": 3}),
            return_source_documents=True
        )
        return chunk_count

    def ask_question(self, question: str) -> dict:
        if self.qa_chain is None:
            return {"error": "No document loaded. Please load a PDF first.", "answer": "", "source_documents": []}
        
        try:
            result = self.qa_chain.invoke({"query": question})
            answer = result.get("result", "I could not find a relevant answer in the document.")
            source_docs = [doc.page_content for doc in result.get("source_documents", [])]
            
            return {
                "answer": answer,
                "source_documents": source_docs
            }
        except Exception as e:
            print(f"Error in ask_question (LangChain chain invocation): {e}")
            return {
                "answer": f"An error occurred while getting the answer: {e}. Please check the console.",
                "source_documents": [],
                "error": str(e)
            }