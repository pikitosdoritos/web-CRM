from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import parse_qs
from html import escape
import os

PORT = 8000

clients = [
    {
        "fullname": "Ivan Ivanov",
        "dob": "2000-01-01",
        "phone": "+38099999999",
        "email": "ivan.ivanov@gmail.com",
        "position": "Python developer",
        "date": "2024-01-01",
        "status": "Interview",
    }
]

def generate_rows():
    rows = ""
    
    for i, c in enumerate(clients, start=1):
        rows += f"""
        <tr>
            <td>{i}</td>
            <td>{escape(c["fullname"])}</td>
            <td>{escape(c["dob"])}</td>
            <td>{escape(c["phone"])}</td>
            <td>{escape(c["email"])}</td>
            <td>{escape(c["position"])}</td>
            <td>{escape(c["date"])}</td>
            <td>{escape(c["status"])}</td>
        </tr>
        """
        
    return rows

class CRMHandler(BaseHTTPRequestHandler):
    
    def do_GET(self):

        if self.path.startswith("/static/"):

            file_path = self.path.lstrip("/")

            if os.path.isfile(file_path):

                self.send_response(200)

                if file_path.endswith(".css"):
                    self.send_header("Content-Type", "text/css")
                elif file_path.endswith(".js"):
                    self.send_header("Content-Type", "application/javascript")
                else:
                    self.send_header("Content-Type", "application/octet-stream")

                self.end_headers()

                with open(file_path, "rb") as f:
                    self.wfile.write(f.read())
            else:
                print("File not found:", file_path)
                self.send_error(404)

            return

        if self.path == "/":
            with open("templates/index.html", "r", encoding="utf-8") as f:
                html = f.read()

            html = html.replace("{{ROWS}}", generate_rows())

            self.send_response(200)
            self.send_header("Content-Type", "text/html")
            self.end_headers()
            self.wfile.write(html.encode())
            return

        self.send_error(404)
        
    def do_POST(self):
        content_length = int(self.headers["Content-Length"])
        body = self.rfile.read(content_length).decode()
        data = parse_qs(body)
        
        new_client = {
            "fullname": data.get("fullname", [""])[0], 
            "dob": data.get("dob", [""])[0],
            "phone": data.get("phone", [""])[0],
            "email": data.get("email", [""])[0],
            "position": data.get("position", [""])[0],
            "date": data.get("date", [""])[0],
            "status": data.get("status", [""])[0],
        }
        
        clients.append(new_client)
        
        self.send_response(303)
        self.send_header("Location", "/")
        self.end_headers()
        
if __name__ == "__main__":
    server = HTTPServer(("127.0.0.1", PORT), CRMHandler)
    print(f"Server running on http://localhost:{PORT}")
    server.serve_forever()