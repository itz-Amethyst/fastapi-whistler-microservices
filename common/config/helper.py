import os
from pathlib import Path
from dotenv import load_dotenv, dotenv_values

PROJECT_DIR: Path = Path(__file__).parent.parent.parent
DOTENV = os.path.join(PROJECT_DIR, ".env")
print(DOTENV)

load_dotenv(dotenv_path=DOTENV)

config = dotenv_values(DOTENV)
