from app.chains.text_to_sql_chain import generate_sql_query_chain
from langchain_core.runnables import Runnable

class Text2SQLHandler(Runnable):
    """Handler class inheriting from Runnable to manage Text2SQL requests."""

    def __init__(self):
        self.chain = generate_sql_query_chain()  # Initialize the Text2SQL chain

    async def invoke(self, inputs: dict, *args, **kwargs) -> dict:
        """Override the invoke method to process inputs and return SQL results."""
        try:
            question = inputs.get("question", "").strip()
            if not question:
                return {"error": "Question is required"}

            print(f"Received question: {question}")

            # Ensure the result is fully awaited and not a coroutine
            result = await self._safe_invoke_chain({"question": question})

            print(f"Generated SQL Query: {result.content}")
            return {"sql_query": result.content}

        except Exception as e:
            print(f"Error: {str(e)}")
            return {"error": str(e)}

    async def _safe_invoke_chain(self, inputs: dict):
        """Ensure the chain result is resolved to prevent deepcopy issues."""
        result = await self.chain.invoke(inputs)
        return result
