from azure.storage.blob.aio import BlobServiceClient
from azure.storage.blob import generate_blob_sas, BlobSasPermissions
from app.core.config import settings
from datetime import datetime, timedelta

async def upload_file_to_blob(file_stream: bytes, blob_path: str, content_type: str) -> str:
    blob_service_client = BlobServiceClient.from_connection_string(settings.AZURE_STORAGE_CONNECTION_STRING)
    
    async with blob_service_client:
        container_client = blob_service_client.get_container_client(settings.AZURE_CONTAINER_NAME)
        blob_client = container_client.get_blob_client(blob_path)
        
        from azure.storage.blob import ContentSettings
        content_settings = ContentSettings(content_type=content_type)
        
        await blob_client.upload_blob(
            file_stream, 
            overwrite=True, 
            content_settings=content_settings
        )
        
        return blob_client.url

def generate_sas_url(blob_url: str) -> str:
    """Generates a SAS token for a given blob URL and appends it."""
    # Parse the connection string to extract account name and key
    conn_str = settings.AZURE_STORAGE_CONNECTION_STRING
    conn_dict = dict(item.split("=", 1) for item in conn_str.split(";") if "=" in item)
    
    account_name = conn_dict.get("AccountName")
    account_key = conn_dict.get("AccountKey")
    
    if not account_name or not account_key:
        return blob_url # Fallback if using a different auth method where keys aren't in conn string
        
    # Extract blob_path from the full blob_url
    # Example URL: https://account.blob.core.windows.net/container/path/to/blob
    try:
        from urllib.parse import unquote
        # The URL might be URL-encoded (like %20 for spaces), but generate_blob_sas expects the raw unencoded string!
        raw_blob_url = unquote(blob_url)
        blob_path = raw_blob_url.split(f"/{settings.AZURE_CONTAINER_NAME}/")[1]
    except IndexError:
        return blob_url # If parsing fails, just return original
        
    sas_token = generate_blob_sas(
        account_name=account_name,
        container_name=settings.AZURE_CONTAINER_NAME,
        blob_name=blob_path,
        account_key=account_key,
        permission=BlobSasPermissions(read=True),
        expiry=datetime.utcnow() + timedelta(hours=1)
    )
    
    return f"{blob_url}?{sas_token}"
