from pathlib import Path
import pdfplumber
def load_txt_document(txt_path):
    txt_path=Path(txt_path)
    text = txt_path.read_text(encoding="utf-8").strip()

    return [{
        "source_file":txt_path.name,
        "page":None,
        "text":text,
        "doc_type":"txt"
    }]

def load_pdf_document(pdf_path):
    pdf_path=Path(pdf_path)
    pages=[]
    with pdfplumber.open(pdf_path) as pdf:
        for page_num, page in enumerate(pdf.pages,start=1):
            text = page.extract_text() or ""
            text = text.strip()

            if not text:
                continue

            pages.append({
                "source_file": pdf_path.name,
                "page": page_num,
                "text": text,
                "doc_type": "pdf"
            })
    return pages

def load_course_documents(data_dir=Path("../data")):
    documents=[]
    for path in sorted(Path(data_dir).iterdir()):
        suffix=path.suffix.lower()
        if suffix == ".txt":
            documents.extend(load_txt_document(path))
        elif suffix == ".pdf":
            documents.extend(load_pdf_document(path))
    return documents

def sliding_window_chunks(text, chunk_size=120, overlap=30):
    words=text.split()
    step=max(1, chunk_size - overlap)
    chunks = []

    for start in range (0,len(words),step):
        piece = words[start:start+ chunk_size]
        if not piece:
            break
        chunks.append(" ".join(piece))
        
        if start + chunk_size >= len(words):
            break
    return chunks

def estimate_token_count(text):
    return len(text.split())

def chunk_documents(documents,chunk_size=120,overlap=30):
    chunks = []
    for doc in documents:
        text_chunks = sliding_window_chunks(
            doc["text"],
            chunk_size=chunk_size,
            overlap=overlap
            )
        for idx, chunk_text in enumerate(text_chunks):
            page_part= doc["page"] if doc["page"] is not None else 0
            chunks.append({
                "chunk_id":f"{doc['source_file']}::p{page_part}::c{idx}",
                "text": chunk_text,
                "source_file":doc["source_file"],
                "page": doc["page"],
                "token_count": estimate_token_count(chunk_text),
            })
    return chunks