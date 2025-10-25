import requests

# 1. Initialize (only once per database/table)
INIT_URL    = "http://localhost:8000/api/init"
CHAT_URL    = "http://localhost:8000/api/chat"
HISTORY_URL = "http://localhost:8000/api/history"

def init_storage(db_file: str, table_name: str):
    resp = requests.post(INIT_URL, json={
        "db_file": db_file,
        "table_name": table_name
    })
    resp.raise_for_status()
    print("Storage initialized:", resp.json())

def chat(message: str) -> str:
    resp = requests.post(CHAT_URL, json={"message": message})
    resp.raise_for_status()
    return resp.json()["reply"]

def get_history() -> list[dict]:
    resp = requests.get(HISTORY_URL)
    resp.raise_for_status()
    return resp.json()

if __name__ == "__main__":
    # 1) Initialize your storage
    init_storage("my_chats.db", "chat_logs")

    # 2) Chat loop
    while True:
        user_input = input("You> ")
        if user_input.lower() in ("exit", "quit"):
            break
        reply = chat(user_input)
        print("Bot>", reply)

    # 3) At any point, fetch the full history:
    history = get_history()
    print("\n=== Full Chat History ===")
    for turn in history:
        ts = turn["created_at"]
        role = turn["role"]
        content = turn["content"]
        print(f"[{ts}] {role}: {content}")
