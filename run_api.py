#!/usr/bin/env python3
"""Start the Banking REST API server."""
import uvicorn

if __name__ == "__main__":
    uvicorn.run(
        "rest_api.app:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
    )
