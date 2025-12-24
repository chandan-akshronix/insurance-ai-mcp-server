import base64
import os
from urllib.parse import urlparse, parse_qs, urlunparse
from typing import Dict, Any, Optional, List, Union
from pydantic import BaseModel, HttpUrl, Field, validator
from fastapi import HTTPException
from azure.storage.blob import BlobClient
from io import BytesIO
import requests

class DocumentFetchRequest(BaseModel):
    document_url: str = Field(..., description="Full URL of the document in Azure Blob Storage")
    sas_token: Optional[str] = Field(None, description="SAS token for authentication if not included in the URL")
    output_format: str = Field("base64", description="Output format: 'base64' or 'url'", regex="^(base64|url)$")
    
    @validator('document_url')
    def validate_document_url(cls, v):
        if not v.startswith(('http://', 'https://')):
            raise ValueError("Document URL must start with http:// or https://")
        return v

class DocumentFetchTool:
    def __init__(self):
        self.name = "document_fetch"
        self.description = "Fetch documents or images from Azure Blob Storage using direct URLs"
    
    def _get_blob_client_from_url(self, url: str, sas_token: Optional[str] = None) -> BlobClient:
        """Create a BlobClient from a URL, handling SAS tokens properly"""
        # If SAS token is provided separately, append it to the URL
        if sas_token:
            # Parse the URL to handle the SAS token properly
            parsed_url = urlparse(url)
            # If URL already has query parameters, append the SAS token with '&', otherwise with '?'
            separator = '&' if parsed_url.query else '?'
            url = f"{url}{separator}{sas_token.lstrip('?')}"
        
        # Create a BlobClient using the URL (which may now include the SAS token)
        return BlobClient.from_blob_url(url)
    
    async def process(self, request: Dict[str, Any]) -> Dict[str, Any]:
        try:
            req = DocumentFetchRequest(**request)
            
            # Get the blob client using the URL
            blob_client = self._get_blob_client_from_url(
                url=req.document_url,
                sas_token=req.sas_token
            )
            
            # Get the blob properties first to check if it exists
            try:
                blob_properties = blob_client.get_blob_properties()
            except Exception as e:
                if "The specified blob does not exist" in str(e):
                    raise HTTPException(status_code=404, detail="Document not found at the specified URL")
                raise
            
            # Get the blob content
            download_stream = await blob_client.download_blob()
            content = await download_stream.readall()
            
            # Get content type and extension
            content_type = blob_properties.content_type or "application/octet-stream"
            
            # Determine file extension from content type or URL
            parsed_url = urlparse(req.document_url)
            filename = os.path.basename(parsed_url.path)
            extension = os.path.splitext(filename)[1].lower()
            
            if not extension:
                if 'pdf' in content_type.lower():
                    extension = '.pdf'
                elif 'jpeg' in content_type.lower() or 'jpg' in content_type.lower():
                    extension = '.jpg'
                elif 'png' in content_type.lower():
                    extension = '.png'
                else:
                    extension = '.bin'
            
            # Prepare response based on output format
            if req.output_format.lower() == 'url':
                # Return the original URL if it has a SAS token, otherwise use the one from blob_client
                if '?' in req.document_url or not req.sas_token:
                    download_url = req.document_url
                else:
                    download_url = f"{req.document_url}?{req.sas_token.lstrip('?')}"
                
                return {
                    "status": "success",
                    "content_type": content_type,
                    "file_extension": extension,
                    "file_size": len(content),
                    "download_url": download_url,
                    "format": "url",
                    "file_name": filename or f"document{extension}"
                }
            else:
                # Return content as base64
                content_base64 = base64.b64encode(content).decode('utf-8')
                
                return {
                    "status": "success",
                    "content_type": content_type,
                    "file_extension": extension,
                    "file_size": len(content),
                    "content": content_base64,
                    "format": "base64",
                    "file_name": filename or f"document{extension}"
                }
                
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Failed to fetch document: {str(e)}"
            )

def register_tools(mcp):
    document_fetch_tool = DocumentFetchTool()
    mcp.register_tool(document_fetch_tool)
    return [document_fetch_tool]
