import http.server
import socketserver
import os

PORT = 8000

class CustomHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory="js", **kwargs)
    
    # def end_headers(self):
    #     self.send_header("Content-Security-Policy", "script-src 'self' 'unsafe-eval';")
    #     http.server.SimpleHTTPRequestHandler.end_headers(self)

    def end_headers(self):
        # Remove the CSP header line entirely
        http.server.SimpleHTTPRequestHandler.end_headers(self)

Handler = CustomHandler

with socketserver.TCPServer(("", PORT), Handler) as httpd:
    print("Serving at port", PORT)
    httpd.serve_forever()