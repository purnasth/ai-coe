# TODO Case for multiple people with the same name
# TODO Data not trained for handling more detailed people queries


import os
import glob
from langchain_core.documents import Document
from config import PEOPLE_MD_DIR


def load_people_markdown(directory=PEOPLE_MD_DIR):
    people_docs = []
    for md_file in glob.glob(os.path.join(directory, "*.md")):
        with open(md_file, "r", encoding="utf-8") as f:
            content = f.read()
            people_docs.append(
                Document(page_content=content, metadata={"source": md_file})
            )
    return people_docs
