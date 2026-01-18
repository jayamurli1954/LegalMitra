"""
Simple HTTP server to serve the LegalMitra frontend
This avoids CORS issues when accessing the backend API
"""

import http.server
import socketserver
import os
import webbrowser
import time
from threading import Timer

PORT = 3005
DIRECTORY = "frontend"

class MyHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DIRECTORY, **kwargs)

    def end_headers(self):
        # Add CORS headers to allow API calls
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        super().end_headers()

def open_browser():
    """Open browser after a short delay"""
    time.sleep(1)
    webbrowser.open(f'http://localhost:{PORT}')

if __name__ == "__main__":
    # Change to project root directory
    os.chdir(os.path.dirname(os.path.abspath(__file__)))

    print("=" * 70)
    print("LegalMitra Frontend Server")
    print("=" * 70)
    print(f"\nStarting HTTP server on port {PORT}...")
    print(f"Serving files from: {os.path.abspath(DIRECTORY)}")
    print(f"\nFrontend URL: http://localhost:{PORT}")
    print(f"Backend API:  http://localhost:8888")
    print("\nMake sure the backend server is running on port 8888!")
    print("\nPress Ctrl+C to stop the server")
    print("=" * 70)

    # Open browser in background
    Timer(1.5, open_browser).start()

    # Start server
    with socketserver.TCPServer(("", PORT), MyHTTPRequestHandler) as httpd:
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n\nShutting down server...")
            httpd.shutdown()
