import os
from dotenv import load_dotenv

load_dotenv()

DEMO_WARNING = (
    "Gemini API key was not available, so LegalEase is running in demo mode."
)


class GeminiDocumentGenerator:

    def __init__(self):
        self.api_key = os.getenv("GEMINI_API_KEY")
        self.model = os.getenv(
            "GEMINI_MODEL",
            "gemini-2.5-flash"
        )

        self.client = None
        self.mode = "demo"

        if self.api_key and self.api_key != "YOUR_GEMINI_API_KEY_HERE":
            try:
                from google import genai

                self.client = genai.Client(
                    api_key=self.api_key
                )

                self.mode = "gemini"

            except Exception:
                self.client = None
                self.mode = "demo"

    def generate_document(
        self,
        document_type,
        parties,
        terms,
        dates,
        jurisdiction=None,
        additional_instructions=None
    ):

        if self.mode == "gemini":
            prompt = f"""
Create a professional legal document.

Document type:
{document_type}

Parties:
{parties}

Dates:
{dates}

Terms:
{terms}

Jurisdiction:
{jurisdiction or "Not specified"}

Additional instructions:
{additional_instructions or "None"}

Write a clear, structured document with:
1. Title
2. Parties
3. Effective Date
4. Purpose
5. Terms and Conditions
6. Termination
7. Governing Law
8. General Provisions
9. Signature section

Do not invent personal facts that were not provided.
Clearly structure the document for editing and review.
"""

            try:
                response = self.client.models.generate_content(
                    model=self.model,
                    contents=prompt
                )

                return response.text

            except Exception:
                return self._demo_document(
                    document_type,
                    parties,
                    terms,
                    dates,
                    jurisdiction
                )

        return self._demo_document(
            document_type,
            parties,
            terms,
            dates,
            jurisdiction
        )

    def _demo_document(
        self,
        document_type,
        parties,
        terms,
        dates,
        jurisdiction
    ):

        return f"""
{document_type.upper()}

PARTIES
{parties}

EFFECTIVE DATE
{dates}

PURPOSE
This document sets out the terms and conditions agreed between the parties.

TERMS AND CONDITIONS

{terms}

TERMINATION
Either party may terminate this agreement subject to the applicable terms
and notice requirements agreed by the parties.

GOVERNING LAW
{jurisdiction or "To be specified by the parties."}

GENERAL PROVISIONS
Any amendments should be made in writing and agreed by the parties.

SIGNATURES

Party 1: ______________________________

Name: ________________________________

Date: _________________________________


Party 2: ______________________________

Name: ________________________________

Date: _________________________________
""".strip()