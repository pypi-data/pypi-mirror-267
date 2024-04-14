# EmbedAnything


EmbedAnything is a powerful library designed to streamline the creation and management of embedding pipelines. Whether you're working with text, images, audio, or any other type of data[Multimodality to be added], EmbedAnything makes it easy to generate embeddings from multiple sources and store them efficiently in a vector database.

## Key Features

- **Flexible:** Build custom embedding pipelines tailored to your needs.
- **Efficient:** Optimized for speed and performance, with core functionality written in Rust.
- **Scalable:** Store embeddings in a vector database for easy retrieval and scalability.
- **Python Interface:** Packaged as a Python library for seamless integration into your existing projects.

##ToDo
- **Versatile:** Supports a wide range of data types, including text, images, audio, and more.
- **Local embeddings** Release it for local embeddings as well
- **Vector Database** Add functionalities to integrate with any Vector Database
## Installation

`
pip install embed-anything`


Requirements:

Please check if you already have the OpenAI key in the Environment variable. We have only released the OpenAI embedder library so far. Please stay tuned for updates for the local embeddings as well.


##Script:

```python
import embed_anything
from embed_anything import EmbedData
data = embed_anything.embed_file("filename.pdf")
```

