from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import parse_qs
from html import escape
import json
import os

PORT = 8000

DATA_FILE = "data.json"


def load_clients():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
        
    return []
   
def save_clients(clients):    
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(clients, f, ensure_ascii=False, indent=4)
    
def generate_rows():
    rows = ""
    
    clients = load_clients()
    # Sort by ID descending to show newest first
    clients.sort(key=lambda x: int(x.get("id", 0)), reverse=True)
    
    for c in clients:
        # Use .get() to avoid KeyError
        id_val = c.get("id", "")
        fullname = c.get("fullname", "")
        dob = c.get("dob", "")
        phone = c.get("phone", "")
        email = c.get("email", "")
        position = c.get("position", "")
        date = c.get("date", "")
        status = c.get("status", "")
        
        rows += f"""
        <tr data-id="{id_val}" onclick="selectRow(this)">
            <td>{id_val}</td>
            <td>{escape(fullname)}</td>
            <td>{escape(dob)}</td>
            <td>{escape(phone)}</td>
            <td>{escape(email)}</td>
            <td>{escape(position)}</td>
            <td>{escape(date)}</td>
            <td>{escape(status)}</td>
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
        if self.path == "/":
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
            
            if new_client["fullname"].strip():
                clients = load_clients()
                if clients:
                    new_id = max(int(c["id"]) for c in clients) + 1
                else:
                    new_id = 1
                    
                new_client["id"] = str(new_id)
    
                clients.append(new_client)
                save_clients(clients)
            
            self.send_response(303)
            self.send_header("Location", "/")
            self.end_headers()
            
            return
        
        if self.path == "/delete":
                content_length = int(self.headers["Content-Length"])
                body = self.rfile.read(content_length).decode()
                data = parse_qs(body)
                
                delete_id = data.get("selected_id", [""])[0]
                
                if delete_id:
                    clients = load_clients()
                    clients = [c for c in clients if c["id"] != delete_id]
                    save_clients(clients)
                    
                self.send_response(303)
                self.send_header("Location", "/")
                self.end_headers()
                
                return
        
        if self.path == "/update":
            content_length = int(self.headers["Content-Length"])
            body = self.rfile.read(content_length).decode()
            data = parse_qs(body)
            
            update_id = data.get("selected_id", [""])[0]
            
            if update_id:
                clients = load_clients()
                
                for client in clients:
                    if client["id"] == update_id:
                        client["fullname"] = data.get("fullname", [""])[0]
                        client["dob"] = data.get("dob", [""])[0]
                        client["phone"] = data.get("phone", [""])[0]
                        client["email"] = data.get("email", [""])[0]
                        client["position"] = data.get("position", [""])[0]
                        client["date"] = data.get("date", [""])[0]
                        client["status"] = data.get("status", [""])[0]
                        
                        break

                save_clients(clients)

            self.send_response(303)
            self.send_header("Location", "/")
            self.end_headers()
            
            return
        
if __name__ == "__main__":
    server = HTTPServer(("127.0.0.1", PORT), CRMHandler)
    print(f"Server running on http://localhost:{PORT}")
    server.serve_forever()