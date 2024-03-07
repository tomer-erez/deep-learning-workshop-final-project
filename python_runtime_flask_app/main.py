from utility.webServer import flaskApp
import queue
from threading import Event

if __name__ == "__main__":
    
    # create a queue to store the images which will be streamed to the web server
    image_queue = queue.Queue(maxsize=1)

    # create an event to notify the web server that a new image is available to be streamed
    new_image_event = Event()
    

    # Start the flask server to stream the video to the web server
    video_app = flaskApp(
                        host = '127.0.0.1',
                        port= 5000,
                        image_queue=image_queue,
                        new_image_event=new_image_event
                        )

    # Start the process to capture the images and stream the video to the web server
    video_app.app.run(video_app.host, video_app.port, debug=False)


