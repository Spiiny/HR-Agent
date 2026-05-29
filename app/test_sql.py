import sqlite3
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage,SystemMessage,AIMessage

load_dotenv()
DB_PATH = "db/hr_agent.db"

model = ChatOpenAI(
    model="gpt-4o-mini",
    temperature=0
)

def get_schema():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(
        "SELECT name FROM sqlite_master WHERE type='table';"
    )
    tables = cursor.fetchall()
    schema = ""

    for table in tables:
        table_name = table[0]
        schema += f"\nTable: {table_name}\n"
        schema += "Columns:\n"
        cursor.execute(
            f"PRAGMA table_info({table_name});"
        )
        columns = cursor.fetchall()

        for column in columns:
            column_name = column[1]
            schema += f"- {column_name}\n"


    conn.close()
    return schema


def generate_sql(
    user_query,
    schema
):

    messages = [
        SystemMessage(
            content="""
            You are an SQLite expert.

            Generate ONLY valid SQLite SQL queries.

            DO NOT:
            - explain anything
            - add markdown
            - add comments

            Return ONLY raw SQL.
            """
        ),

        HumanMessage(
            content=f"""
            Database Schema:

            {schema}

            User Question:
            {user_query}
            """
        )
    ]

    result = model.invoke(messages)
    sql_query = result.content.strip()
    return sql_query


def execute_sql(sql_query):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    try:
        cursor.execute(sql_query)
        results = cursor.fetchall()
        columns = [
            description[0]
            for description in cursor.description
        ]
        conn.close()
        return columns, results

    except Exception as e:
        conn.close()
        return None, str(e)


def run_sql_pipeline(user_query,chat_history):

    if chat_history:
        rewrite_messages = [
            SystemMessage(
                content=f"""
                    You are an HR database query rewriting assistant.

                    Your task is to rewrite follow-up
                    questions into fully standalone questions.

                    Use the conversation history carefully.

                    Resolve references such as:
                    - he
                    - she
                    - they
                    - them
                    - this
                    - those employees
                    - that employee
                    - that department

                    Preserve all important context from
                    previous conversation turns.

                    Examples:

                    Previous:
                    "Show employees in Bangalore"

                    Follow-up:
                    "Who among them are full time employees?"

                    Rewritten:
                    "Which employees in Bangalore are full time employees?"

                    Return ONLY the rewritten standalone question.
                """
            )

        ] + chat_history + [

            HumanMessage(
                content=user_query
            )
        ]
        rewrite_result = model.invoke(
            rewrite_messages
        )
        standalone_query = (
            rewrite_result.content.strip()
        )
    else:
        standalone_query = user_query

    schema = get_schema()
    sql_query = generate_sql(
        standalone_query,
        schema
    )
    columns, results = execute_sql(
        sql_query
    )

    if columns is None:
        return f"SQL Error: {results}"

    if not results:
        return "No matching records found."

    results_text = "\n".join(
        [
            str(dict(zip(columns, row)))
            for row in results
        ]
    )
    format_messages = [

        SystemMessage(
            content="""
            You are an HR assistant.

            Convert database query results into
            natural and user-friendly responses.

            Rules:
            - Keep answers concise
            - Use bullet points if needed
            - Do not mention SQL
            - Do not show raw dictionaries
            - Sound conversational
            """
        ),
        HumanMessage(
            content=f"""
            User Question:
            {user_query}

            Database Results:
            {results_text}
            """
        )
    ]

    formatted_response = model.invoke(
        format_messages
    )
    final_answer = (
        formatted_response.content
    )
    return final_answer
