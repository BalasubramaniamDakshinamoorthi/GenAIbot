# Vector Database
---
Whatever Documents we decide to use as our source material for generation, we need to store them somewhere once we have created embeddings from the text. There are many "local" solutions to this, but in a production setting, it's sometimes easier and more reliable to host the vector database on a cloud platform and just connect via API.

In this case, we are using Qdrant as a vector db. Qdrant is simply the software and it is hosted on a Google Cloud Platform (GCP) instance that is free-tier. This gives us about 4GB of storage and 1GB of RAM to work with, which is usually enough for a small application such as this.

The "nodes" in the vector db contain (in addition to the text and embeddings) metadata such as authors, description of the document, document type, publish date, and title of the document. This allows us to use that information for better retrieval purposes.

If you would like to run a version locally, check out the demos on their [website](https://qdrant.tech/).
