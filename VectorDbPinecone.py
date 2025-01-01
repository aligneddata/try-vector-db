import time
import os
from pinecone import Pinecone, ServerlessSpec
from VectorDbIntf import VectorDbIntf

class VectorDbPinecone(VectorDbIntf):
    def __init__(self, index_name, dimension):
        super().__init__()
        pc = Pinecone(api_key=os.environ.get("PINECONE_API_KEY"))

        cloud = os.environ.get('PINECONE_CLOUD') or 'aws'
        region = os.environ.get('PINECONE_REGION') or 'us-east-1'
        spec = ServerlessSpec(cloud=cloud, region=region)

        if index_name not in pc.list_indexes().names():
            pc.create_index(
                name=index_name,
                dimension=dimension,  # TODO: needs to match embeddings dimension
                metric="cosine",
                spec=spec
            )
            # Wait for index to be ready
            while not pc.describe_index(index_name).status['ready']:
                time.sleep(1)

        # See that it is empty
        print("Index before upsert:")
        print(pc.Index(index_name).describe_index_stats())
        print("\n")
        self.vectorstore = pc
