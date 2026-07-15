import http.server
import urllib.request
import json

OLLAMA_BASE = "http://localhost:11434"

class ProxyHandler(http.server.SimpleHTTPRequestHandler):
    def do_OPTIONS(self):
        self.send_response(200)
        self._send_cors_headers()
        self.end_headers()

    def do_GET(self):
        if self.path.startswith('/api/'):
            self._proxy_request('GET')
        else:
            super().do_GET()

    def do_POST(self):
        if self.path.startswith('/api/'):
            self._proxy_request('POST')
        else:
            self.send_error(404)

    def do_DELETE(self):
        if self.path.startswith('/api/'):
            self._proxy_request('DELETE')
        else:
            self.send_error(404)

    def _send_cors_headers(self):
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, DELETE, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')

    def _proxy_request(self, method):
        url = OLLAMA_BASE + self.path
        body = None
        if method == 'POST':
            length = int(self.headers.get('Content-Length', 0))
            body = self.rfile.read(length) if length > 0 else None

        try:
            req = urllib.request.Request(url, data=body, method=method)
            req.add_header('Content-Type', 'application/json')
            resp = urllib.request.urlopen(req)

            # Check if this is a streaming response
            content_type = resp.headers.get('Content-Type', '')
            is_stream = False
            if body:
                try:
                    parsed = json.loads(body)
                    is_stream = parsed.get('stream', False)
                except:
                    pass

            self.send_response(resp.status)
            self._send_cors_headers()
            for key, val in resp.headers.items():
                if key.lower() not in ('access-control-allow-origin', 'transfer-encoding'):
                    self.send_header(key, val)
            self.end_headers()

            # Stream the response
            while True:
                chunk = resp.read(4096)
                if not chunk:
                    break
                self.wfile.write(chunk)
                if is_stream:
                    self.wfile.flush()

        except urllib.error.HTTPError as e:
            self.send_response(e.code)
            self._send_cors_headers()
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(e.read())
        except Exception as e:
            self.send_response(502)
            self._send_cors_headers()
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({"error": str(e)}).encode())

    def log_message(self, format, *args):
        print(f"[Server] {args[0]}")

if __name__ == '__main__':
    PORT = 8080
    server = http.server.HTTPServer(('', PORT), ProxyHandler)
    print(f"\n  LocalAI Chat Server running at http://localhost:{PORT}")
    print(f"  Proxying Ollama API from {OLLAMA_BASE}")
    print(f"  Press Ctrl+C to stop\n")
    server.serve_forever()
