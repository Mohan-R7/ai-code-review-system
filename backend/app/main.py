# backend/app/main.py
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from .api.v1.endpoints import review as review_v1
from .core.cors import setup_cors
app = FastAPI(
    title="AI-Powered Code Review System",
    description="Static analysis + AI suggestions for Python code",
    version="0.1.0"
)

setup_cors(app)

app.include_router(review_v1.router, prefix="/api/v1/review", tags=["Review"])


@app.get("/", response_class=HTMLResponse)
async def root():
    return """
    <html>
        <body style="font-family: Arial; text-align: center; margin-top: 100px;">
            <h1>AI-Powered Code Review System</h1>
            <p>Backend is running!</p>
            <p><a href="/docs" style="font-size: 20px;">Open Interactive API Docs →</a></p>
        </body>
    </html>
    """


@app.get("/api/health")
async def health_check():
    return {"status": "healthy", "message": "FastAPI backend is up!"}
