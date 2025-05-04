from dotenv import load_dotenv
import os

load_dotenv()

from app import create_app
app = create_app()

if __name__ == "__main__":

    host = os.getenv("HOST", "127.0.0.1")
    port = int(os.getenv("PORT", 5000))

    app.run(host="0.0.0.0", port=port, debug=True)
