from http.server import BaseHTTPRequestHandler, HTTPServer


class HttpProcessor(BaseHTTPRequestHandler):
	def do_GET(self):
		self.send_response(404)
		# self.send_header('content-type','text/html')
		self.end_headers()
		# self.wfile.write(b'<h1>HELLO</h1>')
		
if __name__ == '__main__':
	serv = HTTPServer(("localhost", 1), HttpProcessor)
	print("Working...")
	serv.serve_forever()