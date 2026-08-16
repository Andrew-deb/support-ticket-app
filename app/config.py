import os
import base64
from dotenv import load_dotenv

# Load .env file for local development
load_dotenv()

# Try to get from environment variable first (for local dev)
LAKEBASE_SECRET_KEY = os.getenv("LAKEBASE_SECRET_KEY")

# If not in environment, fetch from Databricks Secrets
if not LAKEBASE_SECRET_KEY:
    try:
        from databricks.sdk import WorkspaceClient
        w = WorkspaceClient()
        secret_value = w.secrets.get_secret(scope="app-secrets", key="lakebase-connection-string")
        
        # Databricks Secrets API returns base64-encoded values
        # Decode it to get the plain text connection string
        encoded_value = secret_value.value
        LAKEBASE_SECRET_KEY = base64.b64decode(encoded_value).decode('utf-8')
        
    except Exception as e:
        raise ValueError(
            f"Could not retrieve database connection string. "
            f"Ensure LAKEBASE_SECRET_KEY environment variable is set or "
            f"the secret is stored in Databricks Secrets (app-secrets/lakebase-connection-string). "
            f"Error: {e}"
        )

if not LAKEBASE_SECRET_KEY:
    raise ValueError(
        "DATABASE_URL is not set. "
        "Create a .env file with your Lakebase connection string for local dev, "
        "or ensure the secret is configured in Databricks Secrets."
    )