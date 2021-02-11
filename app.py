import sys, os
from dotenv import load_dotenv
import uvicorn
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
load_dotenv(os.path.join(BASE_DIR, ".env"))
sys.path.append(BASE_DIR)

from src.server import app

if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=5000)
