from langchain_text_splitters import (
    RecursiveCharacterTextSplitter
)

from langchain_huggingface import (
    HuggingFaceEmbeddings
)

from langchain_community.vectorstores import (
    FAISS
)


# -------------------------------
# Create Vector Store
# -------------------------------

def create_vectorstore(documents):

    """
    Creates a FAISS vector store.

    Expected format:

    documents = [

        {
            "text": "Page content",
            "source": "document.pdf",
            "page": 1
        }

    ]
    """


    # Text splitter

    text_splitter = RecursiveCharacterTextSplitter(

        chunk_size=1000,

        chunk_overlap=200

    )


    all_chunks = []

    all_metadatas = []


    # Process every page

    for document in documents:

        text = document["text"]

        source = document["source"]

        page = document["page"]


        # Split page text into chunks

        chunks = text_splitter.split_text(

            text

        )


        # Store chunks

        all_chunks.extend(

            chunks

        )


        # Store metadata

        all_metadatas.extend(

            [

                {

                    "source": source,

                    "page": page

                }

                for _ in chunks

            ]

        )


    # Create embedding model

    embeddings = HuggingFaceEmbeddings(

        model_name="all-MiniLM-L6-v2"

    )


    # Create FAISS vector store

    vectorstore = FAISS.from_texts(

        texts=all_chunks,

        embedding=embeddings,

        metadatas=all_metadatas

    )


    return vectorstore


# -------------------------------
# Retrieve Context
# -------------------------------

def retrieve_context(

    vectorstore,

    question,

    k=4

):

    """
    Retrieves relevant document chunks
    with source and page metadata.
    """


    # Similarity search

    results = vectorstore.similarity_search(

        question,

        k=k

    )


    context = ""


    # Build context for LLM

    for i, doc in enumerate(

        results

    ):

        source = doc.metadata.get(

            "source",

            "Unknown Document"

        )


        page = doc.metadata.get(

            "page",

            "Unknown Page"

        )


        context += (

            f"\n--- "

            f"Source: {source} | "

            f"Page: {page}"

            f" ---\n"

        )


        context += doc.page_content

        context += "\n"


    return context, results
