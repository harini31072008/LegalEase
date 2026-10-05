import os
from datetime import date

import requests
import streamlit as st

from dotenv import load_dotenv

from document_utils.exporters import (
    format_docx,
    format_pdf
)

from document_utils.html_preview import (
    format_html_preview
)

from document_utils.sanitize import (
    sanitize_text
)


load_dotenv()


BACKEND_URL = os.getenv(
    "BACKEND_URL",
    "http://127.0.0.1:8000"
).rstrip("/")


st.set_page_config(
    page_title="LegalEase",
    page_icon="⚖️",
    layout="wide"
)


st.markdown(
    """
    <style>

    .main-title {
        text-align: center;
        font-size: 2.7rem;
        font-weight: 800;
        margin-bottom: 5px;
    }

    .subtitle {
        text-align: center;
        color: #9ca3af;
        margin-bottom: 30px;
    }

    .preview-box {
        background: #111827;
        color: #f9fafb;
        padding: 30px;
        border-radius: 16px;
        border: 1px solid #374151;
        max-height: 650px;
        overflow-y: auto;
        line-height: 1.7;
    }

    .warning-box {
        padding: 14px;
        border-radius: 10px;
        background: #2b2110;
        border: 1px solid #735619;
        color: #f5d98b;
        margin-bottom: 20px;
    }

    </style>
    """,
    unsafe_allow_html=True
)


if "generated_document" not in st.session_state:

    st.session_state.generated_document = ""


if "generation_mode" not in st.session_state:

    st.session_state.generation_mode = ""


if "warning" not in st.session_state:

    st.session_state.warning = ""


st.markdown(
    '<div class="main-title">⚖️ LegalEase</div>',
    unsafe_allow_html=True
)


st.markdown(
    '<div class="subtitle">'
    'AI-Powered Legal Document Generator'
    '</div>',
    unsafe_allow_html=True
)


with st.sidebar:

    st.header("📄 Document Details")

    document_type = st.selectbox(
        "Document Type",
        [
            "Employment Contract",
            "Non-Disclosure Agreement (NDA)",
            "Lease Agreement",
            "Freelance Work Contract",
            "Service Agreement",
            "Offer Letter",
            "General Agreement",
            "Custom"
        ]
    )

    if document_type == "Custom":

        document_type = st.text_input(
            "Enter document type",
            "Legal Agreement"
        )

    parties = st.text_area(
        "Parties Involved",
        placeholder=(
            "Jane Doe (Service Provider); "
            "TechNova Inc. (Client)"
        ),
        height=120
    )

    terms = st.text_area(
        "Terms & Conditions",
        placeholder=(
            "Payment within 30 days; "
            "Confidentiality; "
            "Delivery by agreed deadline; "
            "Termination with 15 days notice"
        ),
        height=180,
        help="Separate each term using semicolons (;)."
    )

    dates = st.text_input(
        "Effective Date",
        value=date.today().strftime(
            "%B %d, %Y"
        )
    )

    jurisdiction = st.text_input(
        "Jurisdiction",
        placeholder="Example: Tamil Nadu, India"
    )

    brand_name = st.text_input(
        "Company / Brand Name",
        placeholder="Example: ABC Technologies"
    )

    additional_instructions = st.text_area(
        "Additional Instructions",
        placeholder=(
            "Example: Use simple English and "
            "include a two-year confidentiality period."
        ),
        height=120
    )

    logo = st.file_uploader(
        "Upload Logo",
        type=[
            "png",
            "jpg",
            "jpeg"
        ]
    )

    generate_button = st.button(
        "✨ Generate Document",
        type="primary",
        use_container_width=True
    )


if generate_button:

    if not parties.strip():

        st.error(
            "Please enter the parties involved."
        )

    elif not terms.strip():

        st.error(
            "Please enter the terms and conditions."
        )

    elif not dates.strip():

        st.error(
            "Please enter the effective date."
        )

    else:

        request_data = {

            "document_type":
                document_type,

            "parties":
                parties,

            "terms":
                terms,

            "dates":
                dates,

            "jurisdiction":
                jurisdiction or None,

            "brand_name":
                brand_name or None,

            "additional_instructions":
                additional_instructions or None
        }

        with st.spinner(
            "🤖 Generating your legal document..."
        ):

            try:

                response = requests.post(
                    f"{BACKEND_URL}/generate",
                    json=request_data,
                    timeout=120
                )

                response.raise_for_status()

                result = response.json()

                st.session_state.generated_document = (
                    sanitize_text(
                        result["content"]
                    )
                )

                st.session_state.generation_mode = (
                    result.get(
                        "mode",
                        "unknown"
                    )
                )

                st.session_state.warning = (
                    result.get(
                        "warning",
                        ""
                    )
                )

                st.success(
                    "✅ Document generated successfully!"
                )

            except requests.exceptions.RequestException as error:

                st.error(
                    "❌ Could not connect to FastAPI backend."
                )

                st.info(
                    "Make sure the backend is running:\n\n"
                    "`uvicorn backend.main:app --reload --port 8000`"
                )

                st.caption(
                    str(error)
                )


if st.session_state.generated_document:

    st.divider()

    st.subheader(
        "📑 Generated Document"
    )

    if st.session_state.warning:

        st.markdown(
            f"""
            <div class="warning-box">
            ⚠️ {st.session_state.warning}
            </div>
            """,
            unsafe_allow_html=True
        )

    st.caption(
        f"Generation mode: "
        f"{st.session_state.generation_mode.upper()}"
    )

    preview_html = format_html_preview(
        st.session_state.generated_document
    )

    st.markdown(
        f"""
        <div class="preview-box">
        {preview_html}
        </div>
        """,
        unsafe_allow_html=True
    )

    st.divider()

    st.subheader(
        "✏️ Edit Document"
    )

    edited_document = st.text_area(
        "Edit the document below",
        value=st.session_state.generated_document,
        height=500
    )

    col1, col2 = st.columns(2)

    with col1:

        if st.button(
            "💾 Apply Changes",
            use_container_width=True
        ):

            st.session_state.generated_document = (
                sanitize_text(
                    edited_document
                )
            )

            st.success(
                "Changes applied!"
            )

    with col2:

        if st.button(
            "🔄 Reset",
            use_container_width=True
        ):

            st.rerun()

    final_document = sanitize_text(
        st.session_state.generated_document
    )

    logo_bytes = None

    if logo:

        logo_bytes = logo.getvalue()

    txt_file = final_document.encode(
        "utf-8"
    )

    docx_file = format_docx(
    content=final_document,
    document_type=document_type,
    brand_name=brand_name,
    logo_bytes=logo_bytes
)

    pdf_file = format_pdf(
        final_document,
        document_type,
        brand_name=brand_name or None,
        logo_bytes=logo_bytes
    )

    st.divider()

    st.subheader(
        "⬇️ Download Document"
    )

    col1, col2, col3 = st.columns(3)

    with col1:

        st.download_button(
            "📄 Download TXT",
            data=txt_file,
            file_name="LegalEase_Document.txt",
            mime="text/plain",
            use_container_width=True
        )

    with col2:

        st.download_button(
            "📝 Download DOCX",
            data=docx_file,
            file_name="LegalEase_Document.docx",
            mime=(
                "application/"
                "vnd.openxmlformats-officedocument."
                "wordprocessingml.document"
            ),
            use_container_width=True
        )

    with col3:

        st.download_button(
            "📕 Download PDF",
            data=pdf_file,
            file_name="LegalEase_Document.pdf",
            mime="application/pdf",
            use_container_width=True
        )

else:

    st.info(
        "👈 Enter your document details "
        "from the sidebar and click "
        "**Generate Document**."
    )


st.divider()

st.caption(
    "⚖️ LegalEase is an AI-assisted drafting "
    "tool and does not replace professional legal advice."
)