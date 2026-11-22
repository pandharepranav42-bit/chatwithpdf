
from langchain_community.document_loaders import PyPDFLoader

pdf_path = "data/sample.pdf"

loader = PyPDFLoader(pdf_path)

pages = loader.load()

print("Total PDF Pages:", len(pages))

print("\n========== PAGE-WISE TEXT ANALYSIS ==========")

for i, page in enumerate(pages):

    text = page.page_content.strip()

    print(f"\nPage Number: {i + 1}")
    print(f"Characters Extracted: {len(text)}")
    print("Extracted Content:")
    print(text[:1000])

    print("-" * 60)
