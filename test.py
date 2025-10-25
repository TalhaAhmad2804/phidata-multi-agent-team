""" import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Fetch values
endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
key = os.getenv("AZURE_OPENAI_KEY")
model = os.getenv("AZURE_OPENAI_MODEL_NAME")
deployment = os.getenv("AZURE_OPENAI_DEPLOYMENT")  # if you saved it

# Print values (masking the key slightly for safety)
print(f"Endpoint     : {endpoint}")
print(f"API Key      : {key}")
print(f"Model Name   : {model}")
print(f"Deployment   : {deployment}")


    memory=AgentMemory(
        db=SqliteMemoryDb(
            table_name="user_memories",
            db_file="db/sessions.db",
        ),
        create_session_summary=True,
        create_user_memories=True,
        update_user_memories_after_run=True,
    ),
 """