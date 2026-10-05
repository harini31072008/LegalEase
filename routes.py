from fastapi import APIRouter, HTTPException

from .schemas import DocumentRequest, DocumentResponse
from ai_core.gemini_generator import (
    GeminiDocumentGenerator,
    DEMO_WARNING
)

router = APIRouter()

generator = GeminiDocumentGenerator()


@router.post("/generate", response_model=DocumentResponse)
def generate_document(request: DocumentRequest):

    try:
        document = generator.generate_document(
            document_type=request.document_type,
            parties=request.parties,
            terms=request.terms,
            dates=request.dates,
            jurisdiction=request.jurisdiction,
            additional_instructions=request.additional_instructions
        )

        if generator.mode == "gemini":
            mode = "gemini"

            warning = (
                "This document was generated with AI. "
                "Review all clauses, facts, dates and "
                "jurisdiction-specific requirements before use."
            )

        else:
            mode = "demo"

            warning = (
                DEMO_WARNING
                + " "
                + "Review all generated content before use."
            )

        return DocumentResponse(
            document_type=request.document_type,
            content=document,
            mode=mode,
            warning=warning
        )

    except Exception as error:
        raise HTTPException(
            status_code=500,
            detail=str(error)
        )