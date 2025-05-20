import streamlit as st
import pandas as pd

st.set_page_config(page_title="Document Management", layout="wide")

st.title("📚 Document Management")

st.markdown("""
View the status of your uploaded and processed documents.
""")

if "documents" not in st.session_state or not st.session_state.documents:
    st.info("No documents processed yet. Please upload documents from the main page.")
else:
    st.subheader("Processed Documents Overview")
    
    # Create a list of dictionaries for DataFrame conversion
    docs_for_df = []
    for doc_info in st.session_state.documents:
        docs_for_df.append({
            "Document ID": doc_info.get("doc_id", "N/A"),
            "Filename": doc_info.get("filename", "N/A"),
            "Status": doc_info.get("status", "N/A"),
            "Pages / Segments": doc_info.get("pages", "N/A") # Number of pages for PDF, or 1 for image
        })
    
    df = pd.DataFrame(docs_for_df)
    st.dataframe(df, use_container_width=True)