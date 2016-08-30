import http.server
import os.path
import util


class HuffmanRequestHandler (http.server.SimpleHTTPRequestHandler):

    def respond (self, path, header_only=False):
        if os.path.isdir(path):
            path = os.path.join(path, 'index.html')
        try:
            with open(path+'.huf', 'rb') as compressed:
                self.send_response(200)
                self.send_header('Content-type', self.guess_type(path))
                self.end_headers()
                if not header_only:
                    util.decompress(compressed, self.wfile)
        except OSError:
            self.send_error(404, "Not found: {}.huf".format(path))

    def do_GET (self):
        self.respond(self.translate_path(self.path), header_only=False)

    def do_HEAD (self):
        self.respond(self.translate_path(self.path), header_only=True)


if __name__ == '__main__':
    port = 8000
    httpd = http.server.HTTPServer(('', port), HuffmanRequestHandler)
    print('Listening on port {}'.format(port))
    httpd.serve_forever()
