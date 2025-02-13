from event import Event
from qdrant_client import QdrantClient
from sentence_transformers import SentenceTransformer
from qdrant_client.http import models


q_client: QdrantClient = None
model: SentenceTransformer = None


def init(config):
    global q_client, model
    q_client = QdrantClient(host=config["host"], port=config["port"])
    q_client.collection_name = config["collection_name"]
    if not q_client.collection_exists(config["collection_name"]):
        q_client.create_collection(
            collection_name=config["collection_name"],
            vectors_config=models.VectorParams(size=config["model_size"], distance=models.Distance.COSINE)
        )
    model = SentenceTransformer(
        model_name_or_path=config["model"],
        device="cpu"
    )


def add_qdrant_context(event: Event):
    global q_client, model
    vector = model.encode(event.value)
    rez = q_client.query_points(
        collection_name=q_client.collection_name,
        query=vector,
    )
    event.qdrant_context = ""
    if len(rez.points) > 0:
        event.qdrant_context = "\n".join([point.payload["text"] for point in rez.points])

    return event
