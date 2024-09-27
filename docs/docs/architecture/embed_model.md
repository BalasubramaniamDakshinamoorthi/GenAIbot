# Embedding Model
---
Retrieval Augmented Generation (RAG) uses embedding models for the information retrieval part of the process. That is, when a user sends an input, it gets vectorized by the embedding model and a search function (usually cosine similarity) is used to retrieve relevant "chunks" from the database to include as context.

The Embedding Model used for the retrieval step in the process is `Cohere/Cohere-embed-english-v3.0`.

### Model Details
#### Release Date: November 2, 2023

**Dimensions**: 1024
**MTEB Performance**: 64.5


This model was trained in multiple stages.

From the Cohere [Website](https://txt.cohere.com/introducing-embed-v3/):
#### Stage 1: Web Crawl for Topic Similarity

Our embedding models have been trained in multiple stages. First, they have been trained on questions and answers from a large web crawl. When we presented our multilingual-v2.0 model last year, we had a collection of over 1.4 billion question-and-answer pairs from 100+ languages on basically every topic on the internet. This first stage ensures the learning of topic similarity between questions and documents (i.e., it will find documents on the same topic as the query).

#### Stage 2: Search Queries for Content Quality

As shown before, learning topic similarity isn't sufficient for many real-world datasets, where you can have redundant information with varying quality levels. Hence, the second stage involved measuring content quality. We used over 3 million search queries from search engines and retrieved the top-10 most similar documents for each query. A large model was then used to rank this according to their content quality for the given query: which document provides the most relevant information, and which the least? 

This signal was returned to the embedding model as feedback to differentiate between high-quality and low-quality content on a given query. The model is trained to understand a broad spectrum of topics and domains using millions of queries.    

#### Stage 3: Embeddings Optimized for Compression

The final stage involves special, compression-aware training. Running semantic search at scale (with hundreds of millions to billions of embeddings) causes high infrastructure costs for the underlying vector database, several magnitudes higher than computing the embeddings. The final stage ensures that the models work well with vector compression methods, reducing your vector database costs by several factors while keeping up to 99.99% search quality. We will soon provide more information on accessing the compressed vectors and saving on your vector database costs.
