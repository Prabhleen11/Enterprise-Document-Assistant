
import streamlit as st

from utils.pdf_reader import extract_text
from utils.rag import create_vectorstore, retrieve_context
from utils.groq import ask_groq


# -------------------------------
# Page Configuration
# -------------------------------

st.set_page_config(
    page_title="Enterprise Document Assistant",
    page_icon="📄",
    layout="wide"
)


# -------------------------------
# Session State
# -------------------------------

if "messages" not in st.session_state:
    st.session_state.messages = []


if "vectorstore" not in st.session_state:
    st.session_state.vectorstore = None


if "uploaded_file_names" not in st.session_state:
    st.session_state.uploaded_file_names = []


# -------------------------------
# Sidebar
# -------------------------------

st.sidebar.title(
    "📄 Enterprise Document Assistant"
)

st.sidebar.markdown("---")


uploaded_files = st.sidebar.file_uploader(
    "Upload PDF Documents",
    type=["pdf"],
    accept_multiple_files=True
)


# -------------------------------
# Clear Chat
# -------------------------------

if st.sidebar.button("🗑️ Clear Chat"):

    st.session_state.messages = []

    st.rerun()


# -------------------------------
# Main UI
# -------------------------------

st.title(
    "📄 Enterprise Document Assistant"
)

st.markdown(
    """
    **AI-powered document intelligence using Retrieval-Augmented Generation (RAG).**

    Upload one or more PDF documents and ask questions about their content.
    """
)


# -------------------------------
# Process Uploaded PDFs
# -------------------------------

if uploaded_files:

    current_file_names = [
        file.name
        for file in uploaded_files
    ]


    # Detect new files

    if (
        current_file_names
        != st.session_state.uploaded_file_names
    ):

        st.session_state.uploaded_file_names = (
            current_file_names
        )

        # Reset vectorstore

        st.session_state.vectorstore = None

        # Clear previous chat

        st.session_state.messages = []


    st.success(
        f"📚 {len(uploaded_files)} document(s) uploaded"
    )


    st.info(
        "💡 You can ask questions across all uploaded documents."
    )


    # -------------------------------
    # Create Vector Store
    # -------------------------------

    if st.session_state.vectorstore is None:

        with st.spinner(
            "🔄 Processing documents and creating knowledge base..."
        ):

            try:

                documents = []


                # Process every PDF

                for file in uploaded_files:

                    # Extract text page by page

                    pages = extract_text(
                        file
                    )


                    # Check readable text

                    if not pages:

                        st.warning(
                            f"⚠️ No readable text found in {file.name}"
                        )

                        continue


                    # Store every page with metadata

                    for page_data in pages:

                        documents.append(

                            {

                                "text": page_data["text"],

                                "source": file.name,

                                "page": page_data["page"]

                            }

                        )


                # Check if documents exist

                if not documents:

                    st.error(
                        "❌ No readable PDF documents found."
                    )

                    st.stop()


                # Create FAISS vectorstore

                st.session_state.vectorstore = (

                    create_vectorstore(

                        documents

                    )

                )


                st.success(
                    "✅ Documents processed successfully!"
                )


            except Exception as e:

                st.error(
                    f"❌ Error processing documents: {e}"
                )


# -------------------------------
# Display Chat History
# -------------------------------

for message in st.session_state.messages:

    with st.chat_message(
        message["role"]
    ):

        st.markdown(
            message["content"]
        )


# -------------------------------
# Chat Input
# -------------------------------

question = st.chat_input(
    "Ask a question about your documents..."
)


# -------------------------------
# Process User Question
# -------------------------------

if question:


    # Check vectorstore

    if (
        st.session_state.vectorstore
        is None
    ):

        st.warning(
            "⚠️ Please upload at least one PDF first."
        )

        st.stop()


    # -------------------------------
    # Display User Message
    # -------------------------------

    with st.chat_message("user"):

        st.markdown(
            question
        )


    # Save user message

    st.session_state.messages.append(

        {

            "role": "user",

            "content": question

        }

    )


    # -------------------------------
    # Retrieve Context
    # -------------------------------

    with st.spinner(
        "🔍 Searching documents..."
    ):

        context, sources = retrieve_context(

            st.session_state.vectorstore,

            question,

            k=4

        )


    # -------------------------------
    # Generate Answer
    # -------------------------------

    with st.chat_message("assistant"):

        with st.spinner(
            "🤖 Generating answer..."
        ):

            try:

                answer = ask_groq(

                    context,

                    question

                )


                # Display answer

                st.markdown(
                    answer
                )


                # -------------------------------
                # Display Sources
                # -------------------------------

                with st.expander(
                    "📚 View Sources"
                ):

                    for i, source in enumerate(
                        sources
                    ):

                        document_name = (

                            source.metadata.get(

                                "source",

                                "Unknown Document"

                            )

                        )


                        page_number = (

                            source.metadata.get(

                                "page",

                                "Unknown Page"

                            )

                        )


                        st.markdown(

                            f"### 📄 {document_name}"

                        )


                        st.caption(

                            f"Page {page_number}"

                        )


                        st.write(

                            source.page_content

                        )


                # Save assistant response

                st.session_state.messages.append(

                    {

                        "role": "assistant",

                        "content": answer

                    }

                )


            except Exception as e:

                st.error(

                    f"❌ Error generating response: {e}"

                )



