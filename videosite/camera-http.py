#
# Simple Web Streaming Server
# based on picamera advanced recipe 4.10 Web streaming
# https://picamera.readthedocs.io/en/release-1.13/recipes2.html#web-streaming
# Copyright 2013-2017 Dave Jones <dave@waveform.org.uk>
#
# adopted by Martin Eigenbrodt pydvlpr@gmail.com
#

import io
import picamera
import logging
import socketserver
from threading import Condition
from http import server



HOST_NAME = ''
PORT = 8000

# HTML pages to serve
PAGE_STREAM= """\
      <html>
      <head>
      <title>Live-Stream</title>
      </head>
      <body>
      <h1>Live Stream</h1>
      <img src="/stream/stream.mjpg" width="640" height="480" />
      </body>
      </html>
      """

PAGE_PREVIEW= """\
      <html>
      <head>
      <title>Live Preview</title>
      </head>
      <body>
      <img src="/preview/preview.jpg" width="640" height="480" />
      </body>
      </html>
      """

class StreamingOutput(object):
    """
        In memory stream for camera record
    """
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
    """
        Handle web request to serve camera preview or stream
    """
    def do_GET(self):

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
                # only one shot record
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
                # continuous recording
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
    """
        Configuration of socketserver and http.server 
        to allow multiple threads and end HTTP headers correctly
    """
    allow_reuse_address = True
    daemon_threads = True

# create PiCamera instance and start streaming if needed
with picamera.PiCamera(resolution='640x480', framerate=24) as camera:
    output = StreamingOutput()
    
    camera.start_recording(output, format='mjpeg')
    try:
        print('Serving on ',PORT)
        address = (HOST_NAME, PORT)
        server = StreamingServer(address, StreamingHandler)
        server.serve_forever()
    finally:
        camera.stop_recording()
