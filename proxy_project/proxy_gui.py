# import sys
# from PyQt5.QtWidgets import (
#     QApplication, QMainWindow, QVBoxLayout, QTextEdit,
#     QPushButton, QWidget, QLineEdit, QLabel, QListWidget
# )
# from PyQt5.QtCore import QThread
# import logging
# import os
# import hashlib
# import socketserver
# import http.server
# from urllib import request, error

# # Blocked URLs/IPs List (Ensure this is defined at the top)
# BLOCKED = ["example.com", "blockedsite.com"]

# # Logger Setup
# logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')

# # Caching Directory
# CACHE_DIR = "proxy_cache"
# if not os.path.exists(CACHE_DIR):
#     os.makedirs(CACHE_DIR)

# # Custom Headers
# CUSTOM_HEADERS = {"User-Agent": "MyCustomProxy/1.0"}

# # Proxy Handler
# class ProxyHandler(http.server.SimpleHTTPRequestHandler):
#     def do_GET(self):
#         url = self.path[1:]  # Remove leading '/'
#         if any(blocked in url for blocked in BLOCKED):
#             self.send_response(403)
#             self.end_headers()
#             self.wfile.write(b"Access Denied: Blocked URL")
#             return

#         cache_key = hashlib.md5(url.encode()).hexdigest()
#         cache_file = os.path.join(CACHE_DIR, cache_key)

#         if os.path.exists(cache_file):
#             with open(cache_file, "rb") as f:
#                 logging.info(f"Serving from cache: {url}")
#                 self.send_response(200)
#                 self.end_headers()
#                 self.wfile.write(f.read())
#                 return

#         try:
#             req = request.Request(url, headers=CUSTOM_HEADERS)
#             with request.urlopen(req) as response:
#                 content = response.read()

#                 # Cache the response
#                 with open(cache_file, "wb") as f:
#                     f.write(content)

#                 self.send_response(200)
#                 self.send_header("Content-Type", response.headers["Content-Type"])
#                 self.end_headers()
#                 self.wfile.write(content)
#         except error.URLError as e:
#             logging.error(f"Error fetching {url}: {e}")
#             self.send_response(500)
#             self.end_headers()
#             self.wfile.write(b"Internal Proxy Error")

#     def log_message(self, format, *args):
#         logging.info(f"{self.client_address[0]} - {format % args}")


# class ProxyServer:
#     def __init__(self, port=8080):
#         self.port = port
#         self.httpd = None

#     def run(self):
#         with socketserver.TCPServer(("", self.port), ProxyHandler) as httpd:
#             self.httpd = httpd
#             logging.info(f"Proxy server running on port {self.port}")
#             httpd.serve_forever()

#     def stop(self):
#         if self.httpd:
#             self.httpd.shutdown()
#             logging.info("Proxy server stopped")


# class ProxyThread(QThread):
#     def __init__(self, port=8080):
#         super().__init__()
#         self.server = ProxyServer(port)

#     def run(self):
#         self.server.run()

#     def stop(self):
#         self.server.stop()


# class ProxyGUI(QMainWindow):
#     def __init__(self):
#         super().__init__()
#         self.setWindowTitle("Python Proxy Server")
#         self.setGeometry(100, 100, 800, 600)

#         self.central_widget = QWidget()
#         self.setCentralWidget(self.central_widget)
#         self.layout = QVBoxLayout()

#         # Logs
#         self.log_area = QTextEdit(self)
#         self.log_area.setReadOnly(True)
#         self.layout.addWidget(self.log_area)

#         # Controls
#         self.start_button = QPushButton("Start Proxy", self)
#         self.start_button.clicked.connect(self.start_proxy)
#         self.layout.addWidget(self.start_button)

#         self.stop_button = QPushButton("Stop Proxy", self)
#         self.stop_button.setEnabled(False)
#         self.stop_button.clicked.connect(self.stop_proxy)
#         self.layout.addWidget(self.stop_button)

#         # Blocked URLs
#         self.blocked_urls_label = QLabel("Blocked URLs/IPs:", self)
#         self.layout.addWidget(self.blocked_urls_label)
#         self.blocked_list = QListWidget(self)
#         self.blocked_list.addItems(BLOCKED)  # Blocked URLs will be added here
#         self.layout.addWidget(self.blocked_list)

#         self.url_input = QLineEdit(self)
#         self.url_input.setPlaceholderText("Add a URL/IP to block")
#         self.layout.addWidget(self.url_input)

#         self.add_url_button = QPushButton("Add URL/IP", self)
#         self.add_url_button.clicked.connect(self.add_blocked_url)
#         self.layout.addWidget(self.add_url_button)

#         self.central_widget.setLayout(self.layout)
#         self.proxy_thread = None

#     def log_message(self, message):
#         self.log_area.append(message)

#     def start_proxy(self):
#         self.proxy_thread = ProxyThread(port=8080)
#         self.proxy_thread.start()
#         self.start_button.setEnabled(False)
#         self.stop_button.setEnabled(True)
#         self.log_message("Proxy server started on port 8080")

#     def stop_proxy(self):
#         if self.proxy_thread:
#             self.proxy_thread.stop()
#             self.proxy_thread.wait()
#             self.proxy_thread = None
#         self.start_button.setEnabled(True)
#         self.stop_button.setEnabled(False)
#         self.log_message("Proxy server stopped")

#     def add_blocked_url(self):
#         url = self.url_input.text().strip()
#         if url:
#             BLOCKED.append(url)  # This will update the global BLOCKED list
#             self.blocked_list.addItem(url)  # Add to the UI list
#             self.log_message(f"Blocked URL/IP added: {url}")
#             self.url_input.clear()

# if __name__ == "__main__":
#     app = QApplication(sys.argv)
#     gui = ProxyGUI()
#     gui.show()
#     sys.exit(app.exec_())


import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QTextEdit,
    QPushButton, QWidget, QLineEdit, QLabel, QListWidget, QFrame
)
from PyQt5.QtCore import QThread
from PyQt5.QtGui import QPalette, QColor
import logging
import os
import hashlib
import socketserver
import http.server
from urllib import request, error

# Blocked URLs/IPs List (Ensure this is defined at the top)
BLOCKED = ["example.com", "blockedsite.com"]

# Logger Setup
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')

# Caching Directory
CACHE_DIR = "proxy_cache"
if not os.path.exists(CACHE_DIR):
    os.makedirs(CACHE_DIR)

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


class ProxyServer:
    def __init__(self, port=8080):
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


class ProxyThread(QThread):
    def __init__(self, port=8080):
        super().__init__()
        self.server = ProxyServer(port)

    def run(self):
        self.server.run()

    def stop(self):
        self.server.stop()


class ProxyGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Python Proxy Server")
        self.setGeometry(100, 100, 800, 600)

        # Set up colors
        self.setStyleSheet("background-color: #EEEEEE;")
        palette = self.palette()
        palette.setColor(QPalette.Window, QColor("#EEEEEE"))
        palette.setColor(QPalette.WindowText, QColor("#344C64"))
        palette.setColor(QPalette.Base, QColor("#FFFFFF"))
        palette.setColor(QPalette.AlternateBase, QColor("#EEEEEE"))
        palette.setColor(QPalette.Text, QColor("#344C64"))
        palette.setColor(QPalette.Button, QColor("#344C64"))
        palette.setColor(QPalette.ButtonText, QColor("#FFFFFF"))
        self.setPalette(palette)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout()

        # Title
        self.title_label = QLabel("<h1 style='color: #344C64;'>Python Proxy Server</h1>", self)
        self.layout.addWidget(self.title_label)

        # Description
        self.description_label = QLabel(
            "<p style='color: #344C64;'>This application allows you to run a Python-based proxy server.\n"
            "It caches web content, blocks specified URLs or IPs, and logs activity.\n"
            "A Python proxy server acts as an intermediary for requests from clients seeking resources from servers.</p>",
            self
        )
        self.description_label.setWordWrap(True)
        self.layout.addWidget(self.description_label)

        # Separator
        self.separator = QFrame()
        self.separator.setFrameShape(QFrame.HLine)
        self.separator.setFrameShadow(QFrame.Sunken)
        self.layout.addWidget(self.separator)

        # Logs
        self.log_area = QTextEdit(self)
        self.log_area.setReadOnly(True)
        self.log_area.setStyleSheet("background-color: #FFFFFF; color: #344C64;")
        self.layout.addWidget(self.log_area)

        # Controls
        self.start_button = QPushButton("Start Proxy", self)
        self.start_button.setStyleSheet("background-color: #344C64; color: #FFFFFF;")
        self.start_button.clicked.connect(self.start_proxy)
        self.layout.addWidget(self.start_button)

        self.stop_button = QPushButton("Stop Proxy", self)
        self.stop_button.setStyleSheet("background-color: #344C64; color: #FFFFFF;")
        self.stop_button.setEnabled(False)
        self.stop_button.clicked.connect(self.stop_proxy)
        self.layout.addWidget(self.stop_button)

        # Blocked URLs
        self.blocked_urls_label = QLabel("<b style='color: #344C64;'>Blocked URLs/IPs:</b>", self)
        self.layout.addWidget(self.blocked_urls_label)
        self.blocked_list = QListWidget(self)
        self.blocked_list.setStyleSheet("background-color: #FFFFFF; color: #344C64;")
        self.blocked_list.addItems(BLOCKED)  # Blocked URLs will be added here
        self.layout.addWidget(self.blocked_list)

        self.url_input = QLineEdit(self)
        self.url_input.setPlaceholderText("Add a URL/IP to block")
        self.url_input.setStyleSheet("background-color: #FFFFFF; color: #344C64;")
        self.layout.addWidget(self.url_input)

        self.add_url_button = QPushButton("Add URL/IP", self)
        self.add_url_button.setStyleSheet("background-color: #344C64; color: #FFFFFF;")
        self.add_url_button.clicked.connect(self.add_blocked_url)
        self.layout.addWidget(self.add_url_button)

        # Footer
        self.footer_label = QLabel(
            "<p style='color: #344C64;'>Submitted By: <b>Burhan Ahmed</b> and <b>Ifra Fazal</b></p>",
            self
        )
        self.layout.addWidget(self.footer_label)

        self.central_widget.setLayout(self.layout)
        self.proxy_thread = None

    def log_message(self, message):
        self.log_area.append(message)

    def start_proxy(self):
        self.proxy_thread = ProxyThread(port=8080)
        self.proxy_thread.start()
        self.start_button.setEnabled(False)
        self.stop_button.setEnabled(True)
        self.log_message("Proxy server started on port 8080")

    def stop_proxy(self):
        if self.proxy_thread:
            self.proxy_thread.stop()
            self.proxy_thread.wait()
            self.proxy_thread = None
        self.start_button.setEnabled(True)
        self.stop_button.setEnabled(False)
        self.log_message("Proxy server stopped")

    def add_blocked_url(self):
        url = self.url_input.text().strip()
        if url:
            BLOCKED.append(url)  # This will update the global BLOCKED list
            self.blocked_list.addItem(url)  # Add to the UI list
            self.log_message(f"Blocked URL/IP added: {url}")
            self.url_input.clear()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    gui = ProxyGUI()
    gui.show()
    sys.exit(app.exec_())
