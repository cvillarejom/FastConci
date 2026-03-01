from fastapi import FastAPI

app = FastAPI(title="FastConci")

@app.get("/health")
def health():
    return {"status":"ok"}

@app.get("/version")
def version():
    return {"name":"FastConci", "current_version": 0.1}