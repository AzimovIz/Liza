from .extensions import init, add_qdrant_context

extensions = [
    {
        "name": "add_qdrant_context",
        "function": add_qdrant_context
    }
]