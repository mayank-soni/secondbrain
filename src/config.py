import pathlib

# Get path to the database
BASE_DIR_PATH = pathlib.Path(__file__).parent.parent
CHROMA_DATABASE_PATH = BASE_DIR_PATH / "data" / "chroma"
TELEGRAM_DATA_PATH = BASE_DIR_PATH / "data" / "result.json"
