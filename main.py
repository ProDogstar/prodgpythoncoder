from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pydantic import BaseModel
import subprocess
import tempfile
import os

app = FastAPI()

class CodeRequest(BaseModel):
    code: str

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def home():
    return FileResponse("index.html")


@app.post("/run-code")
def run_code(req: CodeRequest):
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".py") as f:
            f.write(req.code.encode())
            file_path = f.name

        result = subprocess.run(
            ["python3", file_path],
            capture_output=True,
            text=True,
            timeout=3
        )

        os.remove(file_path)

        return {
            "output": result.stdout,
            "error": result.stderr
        }

    except Exception as e:
        return {
            "output": "",
            "error": str(e)
        }
