from fastapi import FastAPI
import uvicorn
app = FastAPI()


@app.get("/")
def hello_world():
    # return {"message": "Hello User,Welcome to the Docker World!"}
    return "Hello User,Welcome to the Docker World!"


if __name__ == "__main__":
    # uvicorn.run(app, host="127.0.0.1", port=8000)
    uvicorn.run(app, host="0.0.0.0", port=7000)
