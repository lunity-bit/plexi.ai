from http.server import BaseHTTPRequestHandler, HTTPServer
import os
import json

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
INDEX_FILE = os.path.join(BASE_DIR, "index.html")


class Server(BaseHTTPRequestHandler):

    def do_GET(self):

        if self.path == "/":

            try:
                with open(INDEX_FILE, "rb") as file:
                    content = file.read()

                self.send_response(200)
                self.send_header(
                    "Content-Type",
                    "text/html; charset=utf-8"
                )
                self.end_headers()

                self.wfile.write(content)

            except Exception as error:

                self.send_response(500)
                self.end_headers()

                self.wfile.write(
                    str(error).encode()
                )

        else:

            self.send_response(404)
            self.end_headers()


    def do_POST(self):

        if self.path != "/chat":
            self.send_response(404)
            self.end_headers()
            return

        length = int(
            self.headers.get("Content-Length", 0)
        )

        body = self.rfile.read(length)

        try:

            data = json.loads(body)

            message = data.get("message", "")

            from plexi import think

            answer = think(message)

            response = json.dumps({
                "response": answer
            }).encode("utf-8")

            self.send_response(200)

            self.send_header(
                "Content-Type",
                "application/json"
            )

            self.send_header(
                "Access-Control-Allow-Origin",
                "*"
            )

            self.end_headers()

            self.wfile.write(response)

        except Exception as error:

            response = json.dumps({
                "error": str(error)
            }).encode("utf-8")

            self.send_response(500)

            self.send_header(
                "Content-Type",
                "application/json"
            )

            self.end_headers()

            self.wfile.write(response)


server = HTTPServer(
    ("127.0.0.1", 8000),
    Server
)

print("Server online: http://plexi.ai:8000")

server.serve_forever()