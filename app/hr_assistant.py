from app.router import classify_query
from app.retrieval_pipeline import run_rag_pipeline
from app.test_sql import run_sql_pipeline

def process_query(user_query,chat_history):
    route = classify_query(user_query,chat_history)
    if route == "RAG":
        answer = run_rag_pipeline(user_query,chat_history)
    elif route == "SQL":
        answer = run_sql_pipeline(user_query,chat_history)
    else:
        answer = (
            "I could not determine "
            "how to process the query."
        )
    return {
        "route": route,
        "answer": answer
    }
