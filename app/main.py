from fastapi import FastAPI

app = FastAPI(title="POI Compass API", version="0.1.0")

@app.get("/health", tags=["system"])
def health():
    return {"status": "ok", "version": "0.1.0"}

# TODO: Implement endpoints:
# - /overview
# - /org
# - /roles
# - /qa
# - /recommendation
# - /quiz, /quiz/submit
# - /metrics
# - /gaps
