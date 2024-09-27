import json
import os
import pdb
import sys

sys.path.append("../src")

from dib.embed.gen_embed import Documents

if __name__ == "__main__":

    with open("../artifacts/txtbooks.json", "r") as f:
        data = json.load(f)

    published_list = [
        "The Elements of Statistical Learning",
        "Dive into Deep Learning",
        # "Python Data Science Handbook",
        # "Introducing Python : Modern Computing in Simple Packages",
    ]

    # published_list = []

    documents = Documents.from_file(data=data, published_list=published_list)

    # pdb.set_trace()
    # print(documents.data)

    documents.gen_embeddings(vector_db="milvus")
