# Copyright 2025 Google LLC
# Apache License 2.0

from google.auth import default
import vertexai
from vertexai.preview import rag
import os
from dotenv import load_dotenv, set_key

# Load environment variables from .env file
load_dotenv()

# --- Configuration ---
PROJECT_ID = os.getenv("GOOGLE_CLOUD_PROJECT")
if not PROJECT_ID:
    raise ValueError("GOOGLE_CLOUD_PROJECT environment variable not set in .env")

LOCATION = os.getenv("GOOGLE_CLOUD_LOCATION")
if not LOCATION:
    raise ValueError("GOOGLE_CLOUD_LOCATION environment variable not set in .env")

CORPUS_DISPLAY_NAME = "Markdown_FAQ_Corpus"
CORPUS_DESCRIPTION = "Corpus containing a local Markdown FAQ document"
MARKDOWN_FILENAME = "faq.md"
LOCAL_MD_PATH = rf"C:\Users\Felix Yu\Downloads\{MARKDOWN_FILENAME}"
ENV_FILE_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".env"))


def initialize_vertex_ai():
    credentials, _ = default()
    vertexai.init(project=PROJECT_ID, location=LOCATION, credentials=credentials)


def create_or_get_corpus():
    embedding_model_config = rag.EmbeddingModelConfig(
        publisher_model="publishers/google/models/text-embedding-004"
    )
    existing_corpora = rag.list_corpora()
    corpus = None
    for existing_corpus in existing_corpora:
        if existing_corpus.display_name == CORPUS_DISPLAY_NAME:
            corpus = existing_corpus
            print(f"Found existing corpus with display name '{CORPUS_DISPLAY_NAME}'")
            break
    if corpus is None:
        corpus = rag.create_corpus(
            display_name=CORPUS_DISPLAY_NAME,
            description=CORPUS_DESCRIPTION,
            embedding_model_config=embedding_model_config,
        )
        print(f"Created new corpus with display name '{CORPUS_DISPLAY_NAME}'")
    return corpus


def upload_md_to_corpus(corpus_name, md_path, display_name, description):
    print(f"Uploading {display_name} to corpus...")
    try:
        rag_file = rag.upload_file(
            corpus_name=corpus_name,
            path=md_path,
            display_name=display_name,
            description=description,
        )
        print(f"Successfully uploaded {display_name} to corpus")
        return rag_file
    except Exception as e:
        print(f"Error uploading file {display_name}: {e}")
        return None


def update_env_file(corpus_name, env_file_path):
    try:
        set_key(env_file_path, "RAG_CORPUS", corpus_name)
        print(f"Updated RAG_CORPUS in {env_file_path} to {corpus_name}")
    except Exception as e:
        print(f"Error updating .env file: {e}")


def list_corpus_files(corpus_name):
    files = list(rag.list_files(corpus_name=corpus_name))
    print(f"Total files in corpus: {len(files)}")
    for file in files:
        print(f"File: {file.display_name} - {file.name}")


def main():
    initialize_vertex_ai()
    corpus = create_or_get_corpus()
    update_env_file(corpus.name, ENV_FILE_PATH)

    if not os.path.exists(LOCAL_MD_PATH):
        raise FileNotFoundError(f"Markdown file not found at {LOCAL_MD_PATH}")

    upload_md_to_corpus(
        corpus_name=corpus.name,
        md_path=LOCAL_MD_PATH,
        display_name=MARKDOWN_FILENAME,
        description="Markdown FAQ document"
    )

    list_corpus_files(corpus_name=corpus.name)


if __name__ == "__main__":
    main()
