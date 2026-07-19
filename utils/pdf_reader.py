import fitz


def extract_text(uploaded_file):

    """
    Extracts text from a PDF page by page.

    Returns:

    [
        {
            "text": "Page content...",
            "page": 1
        }
    ]
    """

    # Open uploaded PDF

    pdf_document = fitz.open(

        stream=uploaded_file.read(),

        filetype="pdf"

    )


    pages = []


    # Extract each page separately

    for page_number, page in enumerate(

        pdf_document,

        start=1

    ):

        text = page.get_text()


        if text.strip():

            pages.append(

                {

                    "text": text,

                    "page": page_number

                }

            )


    # Close PDF

    pdf_document.close()


    return pages