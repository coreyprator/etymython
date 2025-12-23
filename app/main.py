from fastapi import FastAPI

app = FastAPI(
    title="Etymython API",
    description="Greek mythology etymology learning system",
    version="0.1.0"
)

@app.get("/")
def root():
    return {"message": "Welcome to Etymython", "status": "running"}

@app.get("/health")
def health():
    return {"status": "healthy"}
