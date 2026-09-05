"""WSGI entry point for Looking Glass Web Alternative."""

from backend.app import app

__all__ = ["app"]


if __name__ == "__main__":
    app.run(debug=False, host="0.0.0.0", port=5001, threaded=True)
