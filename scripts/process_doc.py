import json
import os
import sys

sys.path.append("../src")


from dib.process.pdf_proc import parse_source

if __name__ == "__main__":

    DIRECTORY = os.path.dirname(__file__)

    published_list = [
        "The Elements of Statistical Learning",
        "Dive into Deep Learning",
        "Python Data Science Handbook",
        "Introducing Python : Modern Computing in Simple Packages",
    ]
    with open(f"{DIRECTORY}/../artifacts/sources.json", "r") as f:
        sources = json.load(f)
    new_sources = [x for x in sources if x["title"] not in published_list]
    if len(new_sources) > 0:
        parsed = list(filter(lambda x: x is not None, map(parse_source, new_sources)))
        with open(f"{DIRECTORY}/../artifacts/txtbooks.json", "r") as f:
            current_file = json.load(f)

        final_lofd = [*current_file, *parsed]

        with open(f"{DIRECTORY}/../artifacts/txtbooks.json", "w") as f:
            json.dump(final_lofd, f, indent=2)
    else:
        print("No new sources")
        pass
