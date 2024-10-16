from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from langserve import add_routes
from app.handler.text_to_sql_handler import Text2SQLHandler

app = FastAPI()

text2sql_handler = Text2SQLHandler()


@app.get("/")
async def redirect_root_to_docs():
    return RedirectResponse("/docs")


# Edit this to add the chain you want to add
add_routes(
    app,
    text2sql_handler,
    path="/generate-sql",
    playground_type="chat", )

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
