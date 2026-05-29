from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.messages import (HumanMessage,SystemMessage)

load_dotenv()


model = ChatOpenAI(
    model="gpt-4o-mini",
    temperature=0
)


def classify_query(user_query, chat_history):

    messages = [

        SystemMessage(
            content=f"""
            You are a query routing assistant.

            Your task is to classify queries.

            Return ONLY one word:

            RAG
            or
            SQL

            Use RAG for:
            - policies
            - rules
            - procedures
            - eligibility
            - work from home
            - conduct
            - informational HR questions

            Use SQL for:
            - employee records
            - leave records
            - ticket data
            - timesheet data
            - counts
            - statuses
            - department queries
            - structured database questions

            This is the chat History : {chat_history}

            Return ONLY:
            RAG
            or
            SQL
            """
        ),

        HumanMessage(
            content=user_query
        )
    ]

    result = model.invoke(messages)

    return result.content.strip()


def main():

    while True:

        query = input("\nEnter Query: ")

        if query.lower() == "quit":
            break

        route = classify_query(query)

        print(f"\nROUTE: {route}")


if __name__ == "__main__":
    main()
