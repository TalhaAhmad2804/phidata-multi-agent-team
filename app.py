from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import sqlite3
from agent_phidata import agent_team

app = FastAPI(title="Phidata Chat API")

_db_file: str | None = None
_table_name: str | None = None


class InitRequest(BaseModel):
    db_file: str       # path to your SQLite file
    table_name: str    # name of the table to log chats into


class ChatRequest(BaseModel):
    message: str       # user's input message


@app.post("/api/init")
def api_init(req: InitRequest):
    """
    Remember the SQLite file and table, and create table if needed.
    
    """
    global _db_file, _table_name
    try:
        conn = sqlite3.connect(req.db_file, check_same_thread=False)
        cur = conn.cursor()
        cur.execute(f"""
            CREATE TABLE IF NOT EXISTS {req.table_name} (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                role TEXT NOT NULL,
                content TEXT NOT NULL,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP
            );
        """)
        conn.commit()
        conn.close()

        _db_file = req.db_file
        _table_name = req.table_name
        return {"status": "initialized", "db_file": _db_file, "table_name": _table_name}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Initialization failed: {e}")


@app.post("/api/chat")
def api_chat(req: ChatRequest):
    """
    Manually log user message, invoke the agent_team, then log its reply.
    """
    if not _db_file or not _table_name:
        raise HTTPException(status_code=400, detail="DB not initialized. Call /api/init first.")

    try:
        conn = sqlite3.connect(_db_file, check_same_thread=False)
        cur = conn.cursor()
        cur.execute(
            f"INSERT INTO {_table_name}(role, content) VALUES (?, ?)",
            ("user", req.message)
        )
        conn.commit()
    except Exception as e:
        conn.close()
        raise HTTPException(status_code=500, detail=f"DB write (user) failed: {e}")

    try:
        resp = agent_team.run(message=req.message, stream=False)
        reply = getattr(resp, "content", str(resp))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Agent error: {e}")

    try:
        cur.execute(
            f"INSERT INTO {_table_name}(role, content) VALUES (?, ?)",
            ("assistant", reply)
        )
        conn.commit()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"DB write (assistant) failed: {e}")
    finally:
        conn.close()

    return {"reply": reply}


@app.get("/api/history")
def api_history():
    """
    Return the full chat history from the configured table, in order.
    """
    if not _db_file or not _table_name:
        raise HTTPException(status_code=400, detail="DB not initialized. Call /api/init first.")

    try:
        conn = sqlite3.connect(_db_file, check_same_thread=False)
        cur = conn.cursor()
        cur.execute(
            f"SELECT role, content, created_at FROM {_table_name} ORDER BY created_at ASC"
        )
        rows = cur.fetchall()
        conn.close()
        return [
            {"role": role, "content": content, "created_at": ts}
            for role, content, ts in rows
        ]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"History query failed: {e}")
