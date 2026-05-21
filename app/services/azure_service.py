from azure.storage.blob.aio import BlobServiceClient
from app.core.config import settings

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
