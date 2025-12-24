import os
from google.cloud import secretmanager

def get_secret(secret_id: str, project_id: str = "etymython-project") -> str:
    """Retrieve secret from Google Secret Manager."""
    try:
        client = secretmanager.SecretManagerServiceClient()
        name = f"projects/{project_id}/secrets/{secret_id}/versions/latest"
        response = client.access_secret_version(request={"name": name})
        return response.payload.data.decode("UTF-8").strip()
    except Exception as e:
        # Fall back to environment variable for local development
        env_key = secret_id.upper().replace("-", "_")
        return os.getenv(env_key, "")

# Database configuration
SQL_SERVER = os.getenv("SQL_SERVER", "35.224.242.223")
SQL_DATABASE = os.getenv("SQL_DATABASE", "Etymython")
SQL_USER = os.getenv("SQL_USER", "etymython_user")

def get_database_url() -> str:
    """Build database connection string."""
    password = get_secret("etymython-db-password")
    return (
        f"mssql+pyodbc://{SQL_USER}:{password}@{SQL_SERVER}:1433/{SQL_DATABASE}"
        f"?driver=ODBC+Driver+18+for+SQL+Server&TrustServerCertificate=yes"
    )
