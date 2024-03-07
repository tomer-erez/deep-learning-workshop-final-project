from flask import Flask, render_template, Response
from PIL.Image import fromarray 
from io import BytesIO
import os
import numpy as np
import random

class flaskApp:
    def __init__(self, host: str, port: int,image_queue,new_image_event):
        self.app = Flask(__name__, template_folder = '..\\templates')  # Create Flask app instance here
        self.host = host
        self.port = port
        self.image_queue = image_queue
        self.new_image_event = new_image_event
        # Add routes within the class initialization
        self.app.add_url_rule('/', 'index', self.index)
        self.app.add_url_rule('/video_feed', 'video_feed', self.video_feed)
        self.app.add_url_rule('/quit', 'quit', self.quit)
        self.app.add_url_rule('/generate', 'generate', self.generate)


    def quit(self):
        # terminate the app
        os._exit(0)

    def generate(self):
        img = np.ones((400,400,3),dtype=np.uint8)* random.randint(0,255)
        addImageToWeb(img,self.image_queue,self.new_image_event)
        return 'New image added to the queue.'
    
    def generator(self):
            while True:
                # Wait until new image event is set
                self.new_image_event.wait()  
                 # now that the event was notified, Get the image from the queue
                img = self.image_queue.get()
                if img is None:
                    continue
                img = fromarray(img)
                buf = BytesIO()
                img.save(buf, "JPEG")
                # save the image to a file
                buf.write(b"\r\n--frame\r\n")
                buf.write(b"Content-Type: image/jpeg\r\n\r\n")
                self.new_image_event.clear()
                yield buf.getvalue() 
    
 
    def index(self):
        """
        route to the index page
        """
        return render_template('index.html')

    def video_feed(self):
        """
        this route is used to stream the video from the device to the web server
        """
        return Response(self.generator(), mimetype='multipart/x-mixed-replace; boundary=--frame')

def addImageToWeb(image,queue,new_image_event):
    if queue.qsize() == queue.maxsize:
        queue.get()
    queue.put(image)
    new_image_event.set()
