import streamlit as st
import io
from pdf2image import convert_from_bytes
from PIL import Image
import pytesseract

st.title("Scanned PDF to Editable Text")

uploaded_file = st.file_uploader("Upload a scanned PDF", type=["pdf"])
if uploaded_file is not None:
    # Convert PDF to images
    with st.spinner("Converting PDF to images..."):
        # convert_from_bytes returns a list of PIL Images, one per page.
        try:
            images = convert_from_bytes(uploaded_file.read())
        except Exception as e:
            st.error(f"Failed to convert PDF: {e}")
            st.stop()

    if images:
        st.success(f"Converted {len(images)} pages to images.")

        # Perform OCR on each page
        ocr_texts = []
        with st.spinner("Performing OCR on each page..."):
            for i, img in enumerate(images, start=1):
                text = pytesseract.image_to_string(img)
                ocr_texts.append(text)

        # Combine all pages into one text (or handle separately)
        combined_text = "\n\n---PAGE BREAK---\n\n".join(ocr_texts)

        # Display text in a text area for editing
        edited_text = st.text_area("Extracted Text (editable):", value=combined_text, height=400)

        # Provide download button for edited text
        if st.button("Download Edited Text"):
            txt_bytes = io.StringIO(edited_text)
            st.download_button(
                label="Download as TXT",
                data=txt_bytes.getvalue(),
                file_name="extracted_text.txt",
                mime="text/plain"
            )
    else:
        st.warning("No images were extracted from the PDF.")
