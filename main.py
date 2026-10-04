from fastapi import FastAPI
from routes import chat, auth


app = FastAPI()
app.include_router(chat.router)
app.include_router(auth.router)

@app.get("/")
def main():
    return "Hello from chatllm!"


if __name__ == "__main__":
    main()
