import http.server
import socketserver
from urllib import request, error
import logging
import hashlib
import os
import threading

# Caching Directory
CACHE_DIR = "proxy_cache"
if not os.path.exists(CACHE_DIR):
    os.makedirs(CACHE_DIR)

# Blocked URLs/IPs List
BLOCKED = ["example.com", "blockedsite.com"]

# Custom Headers
CUSTOM_HEADERS = {"User-Agent": "MyCustomProxy/1.0"}

# Proxy Handler
class ProxyHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        url = self.path[1:]  # Remove leading '/'
        if any(blocked in url for blocked in BLOCKED):
            self.send_response(403)
            self.end_headers()
            self.wfile.write(b"Access Denied: Blocked URL")
            return

        cache_key = hashlib.md5(url.encode()).hexdigest()
        cache_file = os.path.join(CACHE_DIR, cache_key)

        if os.path.exists(cache_file):
            with open(cache_file, "rb") as f:
                logging.info(f"Serving from cache: {url}")
                self.send_response(200)
                self.end_headers()
                self.wfile.write(f.read())
                return

        try:
            req = request.Request(url, headers=CUSTOM_HEADERS)
            with request.urlopen(req) as response:
                content = response.read()

                # Cache the response
                with open(cache_file, "wb") as f:
                    f.write(content)

                self.send_response(200)
                self.send_header("Content-Type", response.headers["Content-Type"])
                self.end_headers()
                self.wfile.write(content)
        except error.URLError as e:
            logging.error(f"Error fetching {url}: {e}")
            self.send_response(500)
            self.end_headers()
            self.wfile.write(b"Internal Proxy Error")

    def log_message(self, format, *args):
        logging.info(f"{self.client_address[0]} - {format % args}")

class ProxyServer(threading.Thread):
    def __init__(self, port=8080):
        super().__init__()
        self.port = port
        self.httpd = None

    def run(self):
        with socketserver.TCPServer(("", self.port), ProxyHandler) as httpd:
            self.httpd = httpd
            logging.info(f"Proxy server running on port {self.port}")
            httpd.serve_forever()

    def stop(self):
        if self.httpd:
            self.httpd.shutdown()
            logging.info("Proxy server stopped")
