
from azure.search.documents.indexes import SearchIndexerClient
from azure.search.documents.indexes.models import (
    SearchIndexerDataContainer,
    SearchIndexerDataSourceConnection
)
from azure.identity import DefaultAzureCredential
from azure.core.credentials import AzureKeyCredential
from azure.search.documents.indexes._generated.models import NativeBlobSoftDeleteDeletionDetectionPolicy
import os

# AZURE_SEARCH_INDEX = os.getenv("AZURE_SEARCH_INDEX")
BLOB_CONNECTION_STRING = os.getenv("BLOB_CONNECTION_STRING")
BLOB_CONTAINER_NAME = os.getenv("BLOB_CONTAINER_NAME")

AZURE_SEARCH_SERVICE_ENDPOINT = os.getenv("AZURE_SEARCH_SERVICE_ENDPOINT")
AZURE_SEARCH_ADMIN_KEY = os.getenv("AZURE_SEARCH_ADMIN_KEY")

credential = AzureKeyCredential(AZURE_SEARCH_ADMIN_KEY) if len(AZURE_SEARCH_ADMIN_KEY) > 0 else DefaultAzureCredential()


def create_datasource(blob_folder_name, index_name, blob_container_name=BLOB_CONTAINER_NAME, blob_connection_string=BLOB_CONNECTION_STRING):

    # Create a data source
    indexer_client = SearchIndexerClient(AZURE_SEARCH_SERVICE_ENDPOINT, credential)
    # container = SearchIndexerDataContainer(name=blob_container_name)
    container = SearchIndexerDataContainer(name=blob_container_name, query=blob_folder_name)
    data_source_connection = SearchIndexerDataSourceConnection(
        name=f"{index_name}-datasource",
        type="azureblob",
        connection_string=blob_connection_string,
        container=container,
        data_deletion_detection_policy=NativeBlobSoftDeleteDeletionDetectionPolicy()
    )
    data_source = indexer_client.create_or_update_data_source_connection(data_source_connection)

    return data_source

