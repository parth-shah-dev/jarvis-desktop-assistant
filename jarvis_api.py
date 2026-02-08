from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import threading

# ✅ Import main() from jarvis.py
from jarvis import main as jarvis_main

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def run_jarvis():
    print(">>> JARVIS THREAD STARTED")
    jarvis_main()   # ✅ call the imported function

@app.post("/api/run")
def start_jarvis():
    t = threading.Thread(target=run_jarvis)
    t.daemon = True
    t.start()
    return {"status": "Jarvis started successfully"}
