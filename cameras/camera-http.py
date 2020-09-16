import io
import picamera
import logging
import socketserver
from threading import Condition
from http import server



HOST_NAME = '' 
PORT = 8000

PAGE_STREAM= """\
      <html>
      <head>
      <title>Live-Stream</title>
      </head>
      <body>
      <h1 style="font-size:2vw">Live Stream</h1>
      <img class="img-responsive" src="/stream/stream.mjpg"/>
      </body>
      </html>
      """

PAGE_PREVIEW= """\
      <html>
      <head>
      <title>Live Preview</title>
      </head>
      <body>
      <img class="img-responsive" src="/preview/preview.jpg"/>
      </body>
      </html>
      """

class StreamingOutput(object):
    def __init__(self):
        self.frame = None
        self.buffer = io.BytesIO()
        self.condition = Condition()

    def write(self, buf):
        if buf.startswith(b'\xff\xd8'):
            # New frame, copy the existing buffer's content and notify all
            # clients it's available
            self.buffer.truncate()
            with self.condition:
                self.frame = self.buffer.getvalue()
                self.condition.notify_all()
            self.buffer.seek(0)
        return self.buffer.write(buf)

class StreamingHandler(server.BaseHTTPRequestHandler):
    def do_GET(self):
        print("self.path is ",self.path)
        # preview area
        if self.path == '/preview/':
            self.send_response(301)
            self.send_header('Location', '/preview/preview.html')
            self.end_headers()
        elif self.path == '/preview/preview.html':
            content = PAGE_PREVIEW.encode('utf-8')
            self.send_response(200)
            self.send_header('Content-Type', 'text/html')
            self.send_header('Content-Length', len(content))
            self.end_headers()
            self.wfile.write(content)
        elif self.path == '/preview/preview.jpg':
            self.send_response(200)
            self.send_header('Age', 0)
            self.send_header('Cache-Control', 'no-cache, private')
            self.send_header('Pragma', 'no-cache')
            self.send_header('Content-Type', 'multipart/x-mixed-replace; boundary=FRAME')
            self.end_headers()
            try:
                #while True:
                with output.condition:
                    output.condition.wait()
                    frame = output.frame
                self.wfile.write(b'--FRAME\r\n')
                self.send_header('Content-Type', 'image/jpeg')
                self.send_header('Content-Length', len(frame))
                self.end_headers()
                self.wfile.write(frame)
                self.wfile.write(b'\r\n')
            except Exception as e:
                logging.warning(
                    'Removed streaming client %s: %s',
                    self.client_address, str(e))      
        # stream area      
        elif self.path == '/stream/':
            self.send_response(301)
            self.send_header('Location', '/stream/stream.mjpg')
            self.end_headers()
        elif self.path == '/stream/stream.html':
            content = PAGE_STREAM.encode('utf-8')
            self.send_response(200)
            self.send_header('Content-Type', 'text/html')
            self.send_header('Content-Length', len(content))
            self.end_headers()
            self.wfile.write(content)
        elif self.path == '/stream/stream.mjpg':
            self.send_response(200)
            self.send_header('Age', 0)
            self.send_header('Cache-Control', 'no-cache, private')
            self.send_header('Pragma', 'no-cache')
            self.send_header('Content-Type', 'multipart/x-mixed-replace; boundary=FRAME')
            self.end_headers()
            try:
                while True:
                    with output.condition:
                        output.condition.wait()
                        frame = output.frame
                    self.wfile.write(b'--FRAME\r\n')
                    self.send_header('Content-Type', 'image/jpeg')
                    self.send_header('Content-Length', len(frame))
                    self.end_headers()
                    self.wfile.write(frame)
                    self.wfile.write(b'\r\n')
            except Exception as e:
                logging.warning(
                    'Removed streaming client %s: %s',
                    self.client_address, str(e))
        else:
            self.send_error(404)
            self.end_headers()

class StreamingServer(socketserver.ThreadingMixIn, server.HTTPServer):
    allow_reuse_address = True
    daemon_threads = True


with picamera.PiCamera(resolution='640x480', framerate=24) as camera:
    output = StreamingOutput()
    
    camera.start_recording(output, format='mjpeg')
    try:
        print('Serving on ',PORT)
        address = ('', PORT)
        server = StreamingServer(address, StreamingHandler)
        server.serve_forever()
    finally:
        camera.stop_recording()
