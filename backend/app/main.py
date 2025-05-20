import streamlit as st
import os
import time
import uuid
from pathlib import Path


from core.document_processor import process_document, get_document_text_chunks
from services.vector_store import get_chroma_client, create_collection_if_not_exists, add_chunks_to_collection, search_collection
from models.llm_handler import get_groq_chat_response, get_answer_from_context, synthesize_themes
from config import settings

from langchain_huggingface import HuggingFaceEmbeddings


GROQ_API_KEY = settings.GROQ_API_KEY


# Constants
UPLOAD_DIR = os.path.join("F:/INTERNSHIP_ASSIGNMENT/chatbot_theme_identifier/backend/app/data", "uploads")
DB_DIR = os.path.join("F:/INTERNSHIP_ASSIGNMENT/chatbot_theme_identifier/backend/app/data", "chroma_db")
COLLECTION_NAME = "document_collection"

if not os.path.exists(UPLOAD_DIR):
    os.makedirs(UPLOAD_DIR)

@st.cache_resource
def get_embedding_function():
    return HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

@st.cache_resource
def initialize_chromadb():
    client = get_chroma_client(DB_DIR)
    embedding_func = get_embedding_function()
    collection = create_collection_if_not_exists(client, COLLECTION_NAME, embedding_func)
    return client, collection

def initialize_session_state():
    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "documents" not in st.session_state:
        st.session_state.documents = [] # List of dicts: {'doc_id', 'filename', 'status'}
    if "doc_counter" not in st.session_state:
        st.session_state.doc_counter = 0
    if "processing_log" not in st.session_state:
        st.session_state.processing_log = []

def main():
    st.set_page_config(page_title="Document Research Chatbot", layout="wide")
    st.title("📄 Document Research & Theme Identification Chatbot")

    initialize_session_state()
    client, collection = initialize_chromadb()
    embedding_function = get_embedding_function()

    with st.sidebar:
        st.header("📎 Document Upload")
        uploaded_files = st.file_uploader(
            "Upload 75+ documents (PDF, PNG, JPG, TIFF)",
            type=["pdf", "png", "jpg", "jpeg", "tiff"],
            accept_multiple_files=True
        )

        if uploaded_files:
            if st.button("Process Uploaded Documents"):
                with st.spinner("Processing documents... This may take a while."):
                    st.session_state.processing_log = ["Starting document processing..."]
                    for uploaded_file in uploaded_files:
                        try:
                            filename = uploaded_file.name
                            file_path = os.path.join(UPLOAD_DIR, filename)
                            with open(file_path, "wb") as f:
                                f.write(uploaded_file.getbuffer())

                            st.session_state.doc_counter += 1
                            doc_id = f"DOC{st.session_state.doc_counter:03d}"
                            
                            st.session_state.processing_log.append(f"Processing: {filename} as {doc_id}")
                            st.toast(f"Processing: {filename} as {doc_id}")

                            # Process document (OCR, text extraction)
                            # For simplicity, we'll assume process_document returns list of (text, page_num) tuples
                            pages_content = process_document(file_path, doc_id)

                            # Split text into chunks
                            all_chunks_with_metadata = []
                            for text, page_num in pages_content:
                                chunks = get_document_text_chunks(text, doc_id, page_num, filename)
                                all_chunks_with_metadata.extend(chunks)
                            
                            if all_chunks_with_metadata:
                                add_chunks_to_collection(collection, all_chunks_with_metadata)
                                st.session_state.documents.append({"doc_id": doc_id, "filename": filename, "status": "Processed", "pages": len(pages_content)})
                                st.session_state.processing_log.append(f"✅ Successfully processed and indexed: {filename}")
                                st.toast(f"✅ Indexed: {filename}")
                            else:
                                st.session_state.processing_log.append(f"⚠️ No text extracted from: {filename}")
                                st.toast(f"⚠️ No text from: {filename}", icon="⚠️")

                        except Exception as e:
                            st.session_state.processing_log.append(f"❌ Error processing {filename}: {str(e)}")
                            st.error(f"Error processing {filename}: {e}")
                    st.session_state.processing_log.append("All documents processed.")
                    st.success("All selected documents processed!")
                    st.rerun()

        st.subheader("Processing Log")
        if st.session_state.processing_log:
            st.markdown("\n\n".join(st.session_state.processing_log))

    # Main chat interface
    st.header("💬 Chat with your Documents")

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if prompt := st.chat_input("Ask a question about your documents..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            full_response = ""
            with st.spinner("Thinking..."):
                # 1. Search relevant chunks
                relevant_chunks = search_collection(collection, prompt, n_results=10) # Get more chunks for better context

                if not relevant_chunks or not relevant_chunks.get('documents') or not relevant_chunks['documents'][0]:
                    full_response = "I couldn't find any relevant information in the uploaded documents to answer your query."
                    message_placeholder.markdown(full_response)
                else:
                    # 2. Get individual answers (simplified for now)
                    # In a full implementation, this would call LLM for each relevant chunk/doc
                    # For now, we'll use the chunks directly for theme synthesis prompt
                    
                    context_for_synthesis = []
                    individual_responses_display = "### Individual Document Hits:\n\n| Document ID | Page | Relevant Snippet |\n|---|---|---|\n"
                    
                    # Limiting to top 5 unique documents for individual display and synthesis to manage token limits
                    unique_docs_for_synthesis = {}
                    for i, doc_text in enumerate(relevant_chunks['documents'][0]):
                        meta = relevant_chunks['metadatas'][0][i]
                        doc_id = meta.get('doc_id', 'N/A')
                        page = meta.get('page_number', 'N/A')
                        if doc_id not in unique_docs_for_synthesis or len(unique_docs_for_synthesis[doc_id]) < 200: # Limit snippet length
                             unique_docs_for_synthesis.setdefault(doc_id, "")
                             unique_docs_for_synthesis[doc_id] += doc_text[:200] + "... " # Add snippet
                             context_for_synthesis.append(f"Document: {doc_id}, Page: {page}, Content: {doc_text}")
                             individual_responses_display += f"| {doc_id} | {page} | {doc_text[:100]}... |\n"

                    message_placeholder.markdown(individual_responses_display) # Show individual hits first

                    # 3. Synthesize themes
                    synthesized_response = synthesize_themes(GROQ_API_KEY, prompt, context_for_synthesis)
                    full_response = f"{individual_responses_display}\n\n### Synthesized Answer & Themes:\n\n{synthesized_response}"
                    message_placeholder.markdown(full_response)

            st.session_state.messages.append({"role": "assistant", "content": full_response})

if __name__ == "__main__":
    main()
