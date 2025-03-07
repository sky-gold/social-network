from fastapi import FastAPI
from app.database import engine, Base
from app.routers import auth, profile, sessions
import os
import time
from sqlalchemy import text
from sqlalchemy.exc import OperationalError

app = FastAPI(title="User Service")

if not os.getenv("TESTING"):
    def wait_for_db():
        max_retries = 5
        retry_count = 0
        while retry_count < max_retries:
            try:
                with engine.connect() as conn:
                    conn.execute(text("SELECT 1"))
                print("✅ Connected to database")
                return
            except OperationalError:
                retry_count += 1
                time.sleep(3)
        raise Exception("Could not connect to database")

    wait_for_db()
    Base.metadata.create_all(bind=engine)

app.include_router(auth.router)
app.include_router(profile.router)
app.include_router(sessions.router)

@app.get("/health")
def health_check():
    return {"status": "ok"}