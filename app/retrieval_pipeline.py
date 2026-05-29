from dotenv import load_dotenv
from langchain_chroma import Chroma
from langchain_core.messages import HumanMessage,SystemMessage,AIMessage
from langchain_openai import ChatOpenAI,OpenAIEmbeddings
load_dotenv()

persistent_directory = "db/chroma_db"
embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
db = Chroma(
    persist_directory=persistent_directory,
    embedding_function=embeddings
)
model = ChatOpenAI(
    model="gpt-4o-mini",
    temperature=0
)
def run_rag_pipeline(user_question,chat_history):

    if chat_history:
        messages = [
            SystemMessage(
                content="""
                Given the conversation history,
                rewrite the new question into a
                standalone searchable question.

                Return ONLY the rewritten question.
                """
            )
        ] + chat_history + [
            HumanMessage(f"New question: {user_question}")
        ]
        result = model.invoke(messages)
        search_question = result.content.strip()
    else:
        search_question = user_question
    retriever = db.as_retriever(
        search_type="similarity_score_threshold",
        search_kwargs={
            "k": 5,
            "score_threshold": 0.3
        }
    )
    docs = retriever.invoke(search_question)
    if not docs:
        return (
            "I could not find relevant "
            "information in the HR policies."
        )
    context = "\n\n".join([doc.page_content for doc in docs])
    combined_input = f"""
    Based on the following documents,
    answer this question:

    Question:
    {user_question}

    Documents:
    {context}

    Please answer ONLY using the provided documents.

    If the answer is not available in the documents,
    clearly say so.
    """
    messages = [
        SystemMessage(
            content="""
            You are an HR policy assistant.

            Answer ONLY using the retrieved documents.

            Do not make assumptions.

            Do not give or use ** in the answer.

            If information is unavailable,
            clearly say so.
            """
        )
    ] + chat_history + [
        HumanMessage(
            content=combined_input
        )
    ]
    result = model.invoke(messages)
    answer = result.content
    chat_history.append(
        HumanMessage(content=user_question)
    )
    chat_history.append(
        AIMessage(content=answer)
    )
    return answer