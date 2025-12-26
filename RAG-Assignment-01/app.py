import streamlit as st
import os
import chromadb

from langchain_community.document_loaders import PyPDFLoader
from sentence_transformers import SentenceTransformer

# Initialize embedding model
embedding_model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

# Initialize ChromaDB
db = chromadb.PersistentClient(path="./knowledge_base")
collection = db.get_or_create_collection(name="resume")

# Streamlit UI
st.set_page_config(page_title="Resume Shortlisting using RAG")
st.title("AI Enabled Resume Shortlisting Application")


# Function to load full PDF content
def load_pdf_resume(pdf_path):
    loader = PyPDFLoader(pdf_path)
    docs = loader.load()
    resume_content = ""
    for page in docs:
        resume_content += page.page_content
    metadata = {
        "source": os.path.basename(pdf_path),
        "page_count": len(docs)
    }
    return resume_content, metadata


# Upload resume
def upload_resume(uploaded_file):
    save_dir = "resumes"
    os.makedirs(save_dir, exist_ok=True)
    file_path = os.path.join(save_dir, uploaded_file.name)

    # Save PDF
    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    # Load full PDF
    resume_text, metadata = load_pdf_resume(file_path)

    # Create embedding for entire resume
    embedding = embedding_model.encode([resume_text]).tolist()

    # Store in ChromaDB
    collection.add(
        ids=[uploaded_file.name],
        embeddings=embedding,
        metadatas=[metadata],
        documents=[resume_text]
    )


# Streamlit Upload Section
st.subheader("Upload Resume")
uploaded_files = st.file_uploader(
    "Upload Resume PDF(s)",
    type="pdf",
    accept_multiple_files=True
)

if uploaded_files:
    for file in uploaded_files:
        upload_resume(file)
    st.success("Resume(s) uploaded successfully")


# Streamlit Available Resumes
st.subheader("Available Resumes")
data = collection.get()
resume_names = set(meta["source"] for meta in data["metadatas"])
for name in resume_names:
    st.write("•", name)


# Streamlit Delete Resume
st.subheader("Delete Resume")

delete_resumes = st.multiselect(
    "Select Resume(s) to Delete",
    list(resume_names)
)

if st.button("Delete Selected Resumes"):
    if delete_resumes:
        for resume in delete_resumes:
            # Delete from ChromaDB
            collection.delete(where={"source": resume})

            # Delete PDF file
            file_path = os.path.join("resumes", resume)
            if os.path.exists(file_path):
                os.remove(file_path)

        st.success("Selected resume(s) deleted successfully")
    else:
        st.warning("Please select at least one resume to delete")


# Streamlit Shortlist Resumes
st.subheader("Shortlist Resumes")
job_description = st.text_area("Enter Job Description")
top_n = st.number_input("Number of resumes", 1, 10, 3)

if st.button("Shortlist"):
    query_embedding = embedding_model.encode([job_description]).tolist()
    results = collection.query(
        query_embeddings=query_embedding,
        n_results=top_n
    )
    shortlisted = set(meta["source"] for meta in results["metadatas"][0])
    st.success("Shortlisted Resumes:")
    for r in shortlisted:
        st.write("✅", r)