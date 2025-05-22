PROMPT_ENIITY_AND_NOTE_EXTRACTION_TEMPLATE = """
You are a document parser. You will receive OCR extracted text from an engineering drawing or invoice table.

Your tasks:
1. Extract the following fields:
   - Product Number
   - Product Family
   - Drawing Number
   - Revision
   - Engineer Name
   - Approval Date
   - Status

2. Extract all NOTE entries:
   - Look for any section labeled NOTES, NOTES:, or similar.
   - Extract each note, including numbering like "1.", "2.", or "NOTE 1", "NOTE 2".
   - Do NOT skip or summarize.
   - Each note should be wrapped inside a separate <Note> tag.

Output MUST be in the following XML format:

<ExtractedData>
    <ProductNumber>...</ProductNumber>
    <ProductFamily>...</ProductFamily>
    <DrawingNumber>...</DrawingNumber>
    <Revision>...</Revision>
    <EngineerName>...</EngineerName>
    <ApprovalDate>...</ApprovalDate>
    <Status>...</Status>
    <Notes>
        <Note>...</Note>
        <Note>...</Note>
    </Notes>
</ExtractedData>

Now extract from the following OCR text:
\"\"\"{ocr_text}\"\"\"
"""