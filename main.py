from fastapi import FastAPI
from app.routes_v1 import router as v1_router

app = FastAPI(title="BoardCerts Backend Assignment")

# Versioning Strategy [cite: 27]
app.include_router(v1_router, prefix="/v1", tags=["v1"])

# If you create v2, you would import and include it here similarly
# app.include_router(v2_router, prefix="/v2", tags=["v2"])

@app.get("/")
def root():
    return {"message": "Service is running"}