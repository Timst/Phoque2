"""Phoque server entry point."""

import uvicorn
from phoque_server.server import app

def main():
    """Run the Phoque server."""
    uvicorn.run(app, host="0.0.0.0", port=8000)

if __name__ == "__main__":
    main()