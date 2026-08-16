import os
from dotenv import load_dotenv

# Load .env file for local development
# On Databricks Apps, environment variables are injected automatically
load_dotenv()

LAKEBASE_SECRET_KEY = os.getenv("LAKEBASE_SECRET_KEY")

if not LAKEBASE_SECRET_KEY:
    raise ValueError(
        "DATABASE_URL environment variable is not set. "
        "Create a .env file with your Lakebase connection string."
    )
