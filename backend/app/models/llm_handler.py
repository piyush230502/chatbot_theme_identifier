from groq import Groq

def get_groq_chat_response(api_key: str, messages: list, model: str = "gemma2-9b-it"):
    """Gets a chat response from Groq API."""
    try:
        client = Groq(api_key=api_key)
        chat_completion = client.chat.completions.create(
            messages=messages,
            model=model,
        )
        return chat_completion.choices[0].message.content
    except Exception as e:
        print(f"Error calling Groq API: {e}")
        return "Sorry, I encountered an error trying to connect to the AI model."

def get_answer_from_context(api_key: str, query: str, context: str, doc_id: str, page_num: str):
    """
    Uses an LLM to answer a query based on a specific context from a document.
    (This function might be more complex in full implementation for precise citation)
    """
    prompt_messages = [
        {
            "role": "system",
            "content": "You are an AI assistant. Based *only* on the provided context from a document, answer the user's query. "
                       "If the context doesn't contain the answer, state 'Information not found in this segment.' "
                       "Include the Document ID and Page Number in your citation."
        },
        {
            "role": "user",
            "content": f"Document ID: {doc_id}\nPage: {page_num}\nContext: \"{context}\"\n\nQuery: \"{query}\"\n\nAnswer with Citation:"
        }
    ]
    return get_groq_chat_response(api_key, prompt_messages)

def synthesize_themes(api_key: str, user_query: str, retrieved_contexts: list):
    """
    Analyzes responses/contexts from multiple documents to identify common themes.
    retrieved_contexts is a list of strings, each string being "Document: DOC_ID, Page: X, Content: YYY"
    """
    context_str = "\n\n".join(retrieved_contexts)
    
    prompt_messages = [
        {
            "role": "system",
            "content": "You are an AI research assistant. Your task is to analyze the following text segments, which are retrieved from various documents in response to a user's query. "
                       "Identify common themes across these segments. For each theme, provide a concise description and list the Document IDs and Page numbers that support this theme. "
                       "If multiple segments from the same document support a theme, list the document ID once for that theme. Present the output clearly."
                       "Focus on synthesizing information related to the user's original query."
        },
        {
            "role": "user",
            "content": f"User's Original Query: \"{user_query}\"\n\nRetrieved Information from Documents:\n{context_str}\n\nIdentify common themes, describe them, and cite supporting Document IDs and Page numbers."
        }
    ]
    return get_groq_chat_response(api_key, prompt_messages, model="gemma2-9b-it") # Use a more capable model for synthesis