from http.server import HTTPServer, BaseHTTPRequestHandler
import urllib.parse

LOGIN_FORM = b"""
<!DOCTYPE html>
<html>
<head><title>Test Login</title></head>
<body style="font-family:sans-serif;max-width:400px;margin:80px auto;">
  <h2>Test Login Form (HTTP - Insecure)</h2>
  <form method="POST" action="/login">
    <p>Username:<br><input type="text" name="username" style="width:100%;padding:8px;"></p>
    <p>Password:<br><input type="password" name="password" style="width:100%;padding:8px;"></p>
    <p><button type="submit" style="padding:10px 20px;">Log In</button></p>
  </form>
</body>
</html>
"""


class LoginHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(LOGIN_FORM)

    def do_POST(self):
        length = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(length).decode("utf-8")
        creds = urllib.parse.parse_qs(body)
        username = creds.get("username", [""])[0]
        password = creds.get("password", [""])[0]

        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        msg = f"<html><body style='font-family:sans-serif;max-width:400px;margin:80px auto;'><h2>Login received</h2><p>Username: {username}</p><p>Password: {password}</p><p>This was sent over plain HTTP - visible in Wireshark.</p></body></html>"
        self.wfile.write(msg.encode("utf-8"))

    def log_message(self, format, *args):
        pass  # suppress console noise


if __name__ == "__main__":
    server = HTTPServer(("127.0.0.1", 8080), LoginHandler)
    print("Test login server running at http://127.0.0.1:8080")
    print("Press Ctrl+C to stop")
    server.serve_forever()
