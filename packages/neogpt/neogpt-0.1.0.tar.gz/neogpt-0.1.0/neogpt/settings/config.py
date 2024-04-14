import os
import sys
import warnings
from datetime import datetime

import toml
import torch
import yaml
from chromadb.config import Settings
from dotenv import load_dotenv
from langchain.chat_loaders.whatsapp import WhatsAppChatLoader
from langchain.text_splitter import Language
from langchain_community.document_loaders import (
    CSVLoader,
    GutenbergLoader,
    HNLoader,
    JSONLoader,
    PDFMinerLoader,
    RecursiveUrlLoader,
    TextLoader,
    UnstructuredEmailLoader,
    UnstructuredEPubLoader,
    UnstructuredExcelLoader,
    UnstructuredHTMLLoader,
    UnstructuredMarkdownLoader,
    UnstructuredPowerPointLoader,
    UnstructuredTSVLoader,
    UnstructuredWordDocumentLoader,
    WebBaseLoader,
    YoutubeLoader,
)

# Load Environment Variables
load_dotenv()

# Supress Warnings
warnings.filterwarnings(
    "ignore", category=UserWarning, message="TypedStorage is deprecated"
)


ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Source Directory for Documents to Ingest
SOURCE_DIR = os.path.join(ROOT_DIR, "documents")
# To store models from HuggingFace
MODEL_DIRECTORY = os.path.join(ROOT_DIR, "models")
# PARENT DB DIRECTORY
PARENT_DB_DIRECTORY = os.path.join(ROOT_DIR, "db")
# CHROMA DB DIRECTORY
CHROMA_PERSIST_DIRECTORY = os.path.join(PARENT_DB_DIRECTORY, "chroma")
# FAISS DB DIRECTORY
FAISS_PERSIST_DIRECTORY = os.path.join(PARENT_DB_DIRECTORY, "faiss")
# PINECONE DB DIRECTORY
PINECONE_PERSIST_DIRECTORY = os.path.join(PARENT_DB_DIRECTORY, "pinecone")
# WORKSPACE DIRECTORY
WORKSPACE_DIRECTORY = os.path.join(ROOT_DIR, "workspace")
# CONVERSATION MEMORY DIRECTORY
CONVERSTAION_MEMORY_DIRECTORY = os.path.join(ROOT_DIR, "conversations")

if not os.path.exists(WORKSPACE_DIRECTORY):
    os.makedirs(WORKSPACE_DIRECTORY)

if not os.path.exists(CONVERSTAION_MEMORY_DIRECTORY):
    os.makedirs(CONVERSTAION_MEMORY_DIRECTORY)


# DEFAULT MEMORY KEY FOR CONVERSATION MEMORY (DEFAULT IS 2)
DEFAULT_MEMORY_KEY = 2

# GGUF MODELS (Recommended , Default and Fast)
MODEL_NAME = os.getenv("MODEL_NAME", "TheBloke/Mistral-7B-Instruct-v0.1-GGUF")
MODEL_FILE = os.getenv("MODEL_FILE", "mistral-7b-instruct-v0.1.Q4_K_M.gguf")

# OpenHathi Hindi Model (Testing)
# MODEL_NAME = "sarvamai/OpenHathi-7B-Hi-v0.1-Base"
# MODEL_FILE = "OpenHathi-7B-Hi-v0.1-Base-q4_1.gguf"

# GPTQ MODELS (Quantized Models)
# MODEL_NAME = "TheBloke/Tinyllama-2-1b-miniguanaco-GPTQ"
# MODEL_FILE = "model.safetensors"

# HUGGING FACE MODEL (Not recommended for low RAM systems)
# MODEL_NAME = "microsoft/phi-1_5"
# MODEL_FILE = None

# DEFAULT EMBEDDING MODEL
EMBEDDING_MODEL = "nomic-ai/nomic-embed-text-v1"
# EMBEDDING MODEL CONFIG
INGEST_THREADS = 8

# MODEL CONFIG
MAX_TOKEN_LENGTH = 8192  # 8192 is the max for Mistral-7B
CONTEXT_WINDOW = MAX_TOKEN_LENGTH
TEMPERATURE = 0.7
N_GPU_LAYERS = 40
MODEL_TYPE = os.environ.get("MODEL_TYPE", "llamacpp")

# PYTORCH DEVICE COMPATIBILITY
if torch.cuda.is_available():
    DEVICE_TYPE = "cuda"
elif torch.backends.mps.is_available():
    DEVICE_TYPE = "mps"
else:
    DEVICE_TYPE = "cpu"

# CHROMA DB SETTINGS
CHROMA_SETTINGS = Settings(anonymized_telemetry=False, is_persistent=True)

# PINECONE SETTINGS
EMBEDDING_DIMENSION = ""
INDEX_NAME = ""

# Reserved File Names
RESERVED_FILE_NAMES = ["builder.url"]

# List of file supported for ingest
DOCUMENT_EXTENSION = {
    ".pdf": PDFMinerLoader,
    ".txt": TextLoader,
    ".csv": CSVLoader,
    ".html": UnstructuredHTMLLoader,
    ".tsv": UnstructuredTSVLoader,
    ".eml": UnstructuredEmailLoader,
    ".epub": UnstructuredEPubLoader,
    ".xls": UnstructuredExcelLoader,
    ".xlsx": UnstructuredExcelLoader,
    ".pptx": UnstructuredPowerPointLoader,
    ".ppt": UnstructuredPowerPointLoader,
    ".docx": UnstructuredWordDocumentLoader,
    ".doc": UnstructuredWordDocumentLoader,
    ".md": UnstructuredMarkdownLoader,
    ".json": JSONLoader,
    # ".py": TextLoader,
}

# List of URL patterns supported for ingest
URL_EXTENSION = {
    ".youtube": YoutubeLoader,
    ".ycombinator": HNLoader,
    ".gutenberg": GutenbergLoader,
    "recursive": RecursiveUrlLoader,
    "normal": WebBaseLoader,
}

# List of all Social Chat and their loaders
SOCIAL_CHAT_EXTENSION = {
    r"^(chat_|_chat|whatsapp_|whatsapp_chat|whatsapp_chat_|whatsapp_)": WhatsAppChatLoader
}


# List of all file extensions for programming languages and their parsers
CODE_EXTENSION = {
    ".cpp": Language.CPP,
    ".go": Language.GO,
    ".java": Language.JAVA,
    ".kt": Language.KOTLIN,
    ".js": Language.JS,
    ".ts": Language.TS,
    ".php": Language.PHP,
    ".proto": Language.PROTO,
    ".py": Language.PYTHON,
    ".rst": Language.RST,
    ".ruby": Language.RUBY,
    ".rs": Language.RUST,
    ".scala": Language.SCALA,
    ".swift": Language.SWIFT,
    ".markdown": Language.MARKDOWN,
    ".latex": Language.LATEX,
    ".html": Language.HTML,
    ".sol": Language.SOL,
    ".cs": Language.CSHARP,
    ".cobol": Language.COBOL,
}


# Initial Query Cost and Total Cost
QUERY_COST = 0
TOTAL_COST = 0

# LOG CONFIG
LOG_FOLDER = os.path.join(os.path.dirname(__file__), "logs")
# BUILDER LOG
BUILDER_LOG_FILE = os.path.join(LOG_FOLDER, "builder.log")
# NEOGPT LOG
NEOGPT_LOG_FILE = os.path.join(LOG_FOLDER, "neogpt.log")

# AGENT CONFIG
PROJECT_COST = 0
AGENT_THOUGHTS = []
QA_ENGINEER_FEEDBACK = ""
CURRENT_WORKING_AGENT = ["NeoGPT"]


def import_config(config_filename):
    # This function overwrites the default configuration with the configuration from the config file
    global \
        MODEL_NAME, \
        MODEL_FILE, \
        EMBEDDING_MODEL, \
        INGEST_THREADS, \
        MAX_TOKEN_LENGTH, \
        N_GPU_LAYERS, \
        DEFAULT_MEMORY_KEY, \
        LOG_FOLDER, \
        SOURCE_DIR, \
        WORKSPACE_DIRECTORY, \
        MODEL_DIRECTORY, \
        PARENT_DB_DIRECTORY, \
        CHROMA_PERSIST_DIRECTORY, \
        FAISS_PERSIST_DIRECTORY, \
        PINECONE_PERSIST_DIRECTORY, \
        MODEL_TYPE, \
        TEMPERATURE, \
        CONTEXT_WINDOW

    SETTINGS_DIR = os.path.join(ROOT_DIR, "settings")

    try:
        if not os.path.isabs(config_filename):
            config_filename = os.path.join(SETTINGS_DIR, config_filename)
        print(f"\nUsing configuration file: {config_filename}")
        with open(config_filename) as stream:
            try:
                config = yaml.safe_load(stream)
            except yaml.YAMLError as exc:
                print(exc)
        # MODEL CONFIG
        MODEL_NAME = config["model"]["MODEL_NAME"]
        MODEL_FILE = config["model"]["MODEL_FILE"]
        EMBEDDING_MODEL = config["model"]["EMBEDDING_MODEL"]
        INGEST_THREADS = config["model"]["INGEST_THREADS"]
        MAX_TOKEN_LENGTH = config["model"]["MAX_TOKEN_LENGTH"]
        N_GPU_LAYERS = config["model"]["N_GPU_LAYERS"]
        TEMPERATURE = config["model"]["TEMPERATURE"]
        CONTEXT_WINDOW = config["model"]["CONTEXT_WINDOW"]
        # MODEL TYPE (mistral, openai, hf)
        MODEL_TYPE = config["neogpt"]["MODEL_TYPE"]
        # DEFAULT MEMORY KEY FOR CONVERSATION MEMORY (DEFAULT IS 2)
        DEFAULT_MEMORY_KEY = config["memory"]["DEFAULT_MEMORY_KEY"]
        LOG_FOLDER = config["logs"]["LOG_FOLDER"]
        # Directories
        SOURCE_DIR = config["directories"]["SOURCE_DIR"]
        WORKSPACE_DIRECTORY = config["directories"]["WORKSPACE_DIRECTORY"]
        MODEL_DIRECTORY = config["directories"]["MODEL_DIRECTORY"]
        # Database Directories
        PARENT_DB_DIRECTORY = config["database"]["PARENT_DB_DIRECTORY"]
    except Exception as e:
        print(f"An error occurred: {e}")

    return {
        "PERSONA": config["neogpt"]["PERSONA"],
        "UI": config["neogpt"]["UI"],
        "VERSION": config["neogpt"]["VERSION"],
        "MODEL_TYPE": config["neogpt"]["MODEL_TYPE"],
    }
