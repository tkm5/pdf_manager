import streamlit as st
from PyPDF2 import PdfReader, PdfWriter
from io import BytesIO
import zipfile


# Define the function to add blank pages to the PDF
def add_blank_pages(input_pdf):
    """
    Adds a blank page after each page in the input PDF.

    Args:
        input_pdf (IO): A file-like object representing the input PDF.

    Returns:
        BytesIO: A file-like object representing the output PDF with blank pages added.
                 Returns None if an exception occurs during processing.

    Raises:
        Exception: Propagates any exceptions raised during PDF reading or writing.
    """
    try:
        reader = PdfReader(input_pdf)
        writer = PdfWriter()

        # Add pages and a blank page after each one
        for i in range(len(reader.pages)):
            writer.add_page(reader.pages[i])
            writer.add_blank_page()

        output_pdf = BytesIO()
        writer.write(output_pdf)
        output_pdf.seek(0)
        return output_pdf
    except Exception as e:
        st.error(f"An error occurred: {e}")
        return None


# Streamlit app title
st.title('PDF Blank Page Inserter')

# Hide the Streamlit default menus and footer
hide_streamlit_style = """
    <style>
    #MainMenu {visibility: hidden;}
    header {visibility: hidden;}
    footer {visibility: hidden;}
    </style>
    """
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

# File uploader for multiple files
uploaded_files = st.file_uploader("Choose PDF files", type="pdf", accept_multiple_files=True)

if uploaded_files:
    # Button to process all files
    if st.button('Add Blank Pages'):
        if len(uploaded_files) == 1:
            # If only one file, process and provide direct download
            with st.spinner(f'Processing {uploaded_files[0].name}...'):
                output_pdf = add_blank_pages(uploaded_files[0])
                if output_pdf:
                    file_name = uploaded_files[0].name.replace('.pdf', '') + "_add_blank.pdf"
                    st.success('File processed!')
                    st.download_button(
                        label="Download PDF with Blank Pages",
                        data=output_pdf,
                        file_name=file_name,
                        mime="application/pdf"
                    )
        else:
            # If multiple files, process and zip them
            zip_buffer = BytesIO()
            with zipfile.ZipFile(zip_buffer, 'a', zipfile.ZIP_DEFLATED) as zip_file:
                for uploaded_file in uploaded_files:
                    with st.spinner(f'Processing {uploaded_file.name}...'):
                        output_pdf = add_blank_pages(uploaded_file)
                        if output_pdf:
                            file_name = uploaded_file.name.replace('.pdf', '') + "_add_blank.pdf"
                            zip_file.writestr(file_name, output_pdf.getvalue())
            st.success('All files processed!')
            zip_buffer.seek(0)
            st.download_button(
                label="Download Zipped PDFs with Blank Pages",
                data=zip_buffer,
                file_name="processed_pdfs.zip",
                mime="application/zip"
            )
