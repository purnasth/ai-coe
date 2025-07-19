VYAGUTA_BASE_URL = "https://vyaguta.lftechnology.com"
API_TOKEN_URL = f"{VYAGUTA_BASE_URL}/api/auth/token"
API_PEOPLE_URL = f"{VYAGUTA_BASE_URL}/api/core/users"
CLIENT_ID = "lms"

# RAG Pipeline batching

BATCH_SIZE = 40  # Lower batch size to keep total tokens per request well below 300,000

# RAG Pipeline document directories
DOC_DIRECTORIES = ["docs", "docs-api/people", "docs-confluence"]
# Directory for people markdown data
PEOPLE_MD_DIR = "docs-api/people"

# RAG Pipeline chunking and retrieval
CHUNK_SIZE = 1000
CHUNK_OVERLAP = 200
MAX_CHARS = 2000
RETRIEVER_K = 40
