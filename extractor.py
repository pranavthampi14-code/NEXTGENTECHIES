# For the legal-demystify POC, extractor simply returns the full OCR text.
def extract_text_block(text):
    # Optionally, implement rule-based splitting, header removal, or PII masking here.
    # For now, return the text truncated to a reasonable length for the Gemini prompt.
    max_chars = 6000
    if len(text) > max_chars:
        # prefer keeping beginnings and ends
        return text[:4000] + '\n\n...[truncated]...\n\n' + text[-1000:]
    return text
