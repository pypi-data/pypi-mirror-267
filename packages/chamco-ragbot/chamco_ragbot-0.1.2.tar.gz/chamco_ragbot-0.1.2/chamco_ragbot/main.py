import os

import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')



from .filetransfer import sharepoint_auth, download_sharepoint_file, upload_file_to_blob_container
from .datasource import create_datasource
from .chat import chat, get_context, get_response
from .index import create_index
from .indexer import create_indexer, indexer_client
from .skillset import create_skill_set


SHAREPOINT_SITE_URL = os.getenv("SHAREPOINT_SITE_URL")
SHAREPOINT_USERNAME = os.getenv("SHAREPOINT_USERNAME")
SHAREPOINT_PASSWORD = os.getenv("SHAREPOINT_PASSWORD")

BLOB_CONNECTION_STRING = os.getenv("BLOB_CONNECTION_STRING")
BLOB_CONTAINER_NAME = os.getenv("BLOB_CONTAINER_NAME")





def update_rag(file_url, folder_url):

    ctx = sharepoint_auth(SHAREPOINT_SITE_URL, SHAREPOINT_USERNAME, SHAREPOINT_PASSWORD)
    download_path = download_sharepoint_file(ctx, file_url)
    blob_name = upload_file_to_blob_container(download_path, file_url, BLOB_CONNECTION_STRING, BLOB_CONTAINER_NAME)
    index = create_index(file_url)
    data_source = create_datasource(folder_url, index_name=index.name)
    skillset = create_skill_set(index_name=index.name)
    indexer_result = create_indexer(index.name, data_source, skillset.name)
    
    logging.info(f"[Ok] {indexer_result.name} indexer update completed")

    logging.info(f"[Ok] running indexer {indexer_result.name}")
    indexer_client.run_indexer(indexer_result.name)

    logging.info(f"[Ok] RAG update completed")

    # print(f"[Ok] {indexer_result.name} update completed")
    # print(f"[Ok] RAG update completed")





