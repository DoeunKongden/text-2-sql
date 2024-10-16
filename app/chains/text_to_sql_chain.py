from langchain_ollama.llms import OllamaLLM
from langchain.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain.chains.sql_database.query import create_sql_query_chain
from langchain_community.utilities.sql_database import SQLDatabase
from langchain_community.tools.sql_database.tool import QuerySQLDataBaseTool
from operator import itemgetter

# Database credentials
db_user = "postgres"
db_password = "DeN112233"
db_host = "107.23.208.215"
db_name = "sales_db"

# Establish the PostgreSQL database connection
db = SQLDatabase.from_uri(f"postgresql+psycopg2://{db_user}:{db_password}@{db_host}/{db_name}")

# Initialize the language model
llm = OllamaLLM(model="llama3.1", temperature=0.7, timeout=30, max_retries=2)

# Create the query generation chain
generate_query = create_sql_query_chain(llm, db=db)

# Initialize the SQL execution tool
execute_query = QuerySQLDataBaseTool(db=db)


def generate_sql_query_chain():
    """Generate a SQL query from natural language input string."""

    # Create the answer prompt template
    answer_prompt = PromptTemplate.from_template(
        """Given the following user question, corresponding SQL query, and SQL result, answer the user question.
        Question: {question}
        SQL Query: {query}
        SQL Result: {result}
        Answer: """
    )

    # Define the chain for query generation and execution
    try:
        chain = (

                RunnablePassthrough.assign(query=generate_query)  # generating the SQL query
                .assign(result=itemgetter("query") | execute_query)
                | answer_prompt | llm | StrOutputParser()
        )

        return chain

    except Exception as e:
        return e
