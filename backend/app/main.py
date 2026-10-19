from fastapi import FastAPI

app = FastAPI(title="Urban Ripple Engine")


@app.get("/")
def root():
    return {
        "message": "Urban Ripple Engine API is running"
    }


@app.get("/health")
def health():
    return {
        "status": "healthy"
    }