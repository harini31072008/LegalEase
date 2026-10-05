import html
import re


def format_html_preview(text: str, brand_name: str = "LegalEase") -> str:
    """
    Convert generated legal document text into a clean HTML preview.
    """

    if not text:
        return "<p>No document content available.</p>"

    escaped = html.escape(text.strip())

    lines = escaped.splitlines()

    output = []

    output.append("""
    <div style="
        max-width: 900px;
        margin: auto;
        padding: 40px;
        background: white;
        color: #222;
        font-family: Georgia, 'Times New Roman', serif;
        line-height: 1.7;
        border: 1px solid #ddd;
        border-radius: 10px;
    ">
    """)

    output.append(
        f"""
        <div style="
            text-align:center;
            margin-bottom:30px;
            padding-bottom:15px;
            border-bottom:2px solid #333;
        ">
            <div style="
                font-size:14px;
                color:#666;
                font-family:Arial,sans-serif;
            ">
                {html.escape(brand_name)}
            </div>
        </div>
        """
    )

    in_list = False

    for line in lines:
        line = line.strip()

        if not line:
            if in_list:
                output.append("</ul>")
                in_list = False
            continue

        # Main title
        if re.match(r"^(LEGAL|AGREEMENT|CONTRACT|DOCUMENT)\b", line, re.I):
            if in_list:
                output.append("</ul>")
                in_list = False

            output.append(
                f"""
                <h1 style="
                    text-align:center;
                    font-size:28px;
                    margin:20px 0;
                ">
                    {line}
                </h1>
                """
            )

        # Numbered headings
        elif re.match(r"^\d+[\.\)]\s+[A-Z][A-Z\s&\-]+$", line):
            if in_list:
                output.append("</ul>")
                in_list = False

            output.append(
                f"""
                <h2 style="
                    margin-top:25px;
                    font-size:20px;
                ">
                    {line}
                </h2>
                """
            )

        # All-uppercase headings
        elif (
            len(line) < 120
            and line.upper() == line
            and re.search(r"[A-Z]", line)
        ):
            if in_list:
                output.append("</ul>")
                in_list = False

            output.append(
                f"""
                <h2 style="
                    margin-top:25px;
                    font-size:20px;
                ">
                    {line}
                </h2>
                """
            )

        # Bullet points
        elif line.startswith("- ") or line.startswith("• "):
            if not in_list:
                output.append("<ul>")
                in_list = True

            item = re.sub(r"^[-•]\s*", "", line)

            output.append(
                f"""
                <li style="margin-bottom:8px;">
                    {item}
                </li>
                """
            )

        else:
            if in_list:
                output.append("</ul>")
                in_list = False

            output.append(
                f"""
                <p style="margin:12px 0;">
                    {line}
                </p>
                """
            )

    if in_list:
        output.append("</ul>")

    output.append(
        """
        <div style="
            margin-top:40px;
            padding-top:15px;
            border-top:1px solid #ccc;
            text-align:center;
            font-size:12px;
            color:#777;
            font-family:Arial,sans-serif;
        ">
            Generated using LegalEase — AI-powered legal document generator
        </div>
        """
    )

    output.append("</div>")

    return "\n".join(output)