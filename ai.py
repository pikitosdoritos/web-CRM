from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import parse_qs
import html

items = []  # Хранение в памяти


class App(BaseHTTPRequestHandler):

    def send_html(self, content):
        data = content.encode()
        self.send_response(200)
        self.send_header("Content-Type", "text/html")
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def read_form(self):
        length = int(self.headers.get("Content-Length", 0))
        data = self.rfile.read(length).decode()
        return parse_qs(data)

    # ===== GET =====
    def do_GET(self):
        if self.path == "/":
            self.show_list()
        elif self.path.startswith("/delete"):
            index = int(self.path.split("=")[-1])
            if 0 <= index < len(items):
                items.pop(index)
            self.redirect()
        elif self.path.startswith("/edit"):
            index = int(self.path.split("=")[-1])
            self.show_edit(index)
        else:
            self.send_html("Not found")

    # ===== POST =====
    def do_POST(self):
        if self.path == "/create":
            form = self.read_form()
            title = form.get("title", [""])[0]
            if title:
                items.append(title)
            self.redirect()

        elif self.path == "/update":
            form = self.read_form()
            index = int(form.get("index", ["0"])[0])
            title = form.get("title", [""])[0]
            if 0 <= index < len(items):
                items[index] = title
            self.redirect()

    # ===== Pages =====
    def show_list(self):
        list_html = ""
        for i, item in enumerate(items):
            list_html += f"""
            <li>
                {html.escape(item)}
                <a href="/edit?id={i}">edit</a>
                <a href="/delete?id={i}">delete</a>
            </li>
            """

        html_page = f"""
        <h1>CRUD</h1>

        <form method="post" action="/create">
            <input name="title">
            <button>Create</button>
        </form>

        <ul>
            {list_html}
        </ul>
        """
        self.send_html(html_page)

    def show_edit(self, index):
        if 0 <= index < len(items):
            value = html.escape(items[index])
            html_page = f"""
            <h1>Edit</h1>
            <form method="post" action="/update">
                <input type="hidden" name="index" value="{index}">
                <input name="title" value="{value}">
                <button>Save</button>
            </form>
            <a href="/">Back</a>
            """
            self.send_html(html_page)
        else:
            self.redirect()

    def redirect(self):
        self.send_response(303)
        self.send_header("Location", "/")
        self.end_headers()


if __name__ == "__main__":
    server = HTTPServer(("127.0.0.1", 8000), App)
    print("http://127.0.0.1:8000")
    server.serve_forever()
