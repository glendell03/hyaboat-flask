from flask import Flask, render_template, Response
import cv2
import time
from model.object_detector import ObjectDetector
from model.object_detector import ObjectDetectorOptions
from model.utils import visualize

app = Flask(__name__)


class Args:
    model = "water-hyacinth-model.tflite"
    cameraId = 0
    frameWidth = 640
    frameHeight = 480
    numThreads = 4
    enableEdgeTPU = False


camera = cv2.VideoCapture(0)  # use 0 for web camera
#  for cctv camera use rtsp://username:password@ip_address:554/user=username_password='password'_channel=channel_number_stream=0.sdp' instead of camera
# for local webcam use cv2.VideoCapture(0)


def gen_frames():  # generate frame by frame from camera
    args = Args()
    counter, fps = 0, 0
    start_time = time.time()

    # camera.set(cv2.CAP_PROP_FRAME_WIDTH, args.frameWidth)
    # camera.set(cv2.CAP_PROP_FRAME_HEIGHT, args.frameHeight)

    # Visualization parameters
    row_size = 20  # pixels
    left_margin = 24  # pixels
    text_color = (0, 0, 255)  # red
    font_size = 1
    font_thickness = 1
    fps_avg_frame_count = 10

    # Initialize the object detection model
    # options = ObjectDetectorOptions(
    #     num_threads=args.numThreads,
    #     score_threshold=0.3,
    #     max_results=3,
    #     enable_edgetpu=args.enableEdgeTPU,
    # )

    # detector = ObjectDetector(model_path=args.model, options=options)

    while True:
        # Capture frame-by-frame
        success, frame = camera.read()  # read the camera frame
        if not success:
            break
        else:
            ret, buffer = cv2.imencode(".jpg", frame)

            counter += 1
            image = cv2.flip(frame, 1)

            # # Run object detection estimation using the model.
            # # detections = detector.detect(image)

            # # image = visualize(image, detections)

            # Calculate the FPS
            if counter % fps_avg_frame_count == 0:
                end_time = time.time()
                fps = fps_avg_frame_count / (end_time - start_time)
                start_time = time.time()

            # Show the FPS
            fps_text = "FPS = {:.1f}".format(fps)
            text_location = (left_margin, row_size)
            cv2.putText(
                image,
                fps_text,
                text_location,
                cv2.FONT_HERSHEY_PLAIN,
                font_size,
                text_color,
                font_thickness,
            )

            frame = buffer.tobytes()
            yield (b"--frame\r\n" b"Content-Type: image/jpeg\r\n\r\n" + frame + b"\r\n")


@app.route("/video_feed")
def video_feed():
    # Video streaming route. Put this in the src attribute of an img tag
    return Response(gen_frames(), mimetype="multipart/x-mixed-replace; boundary=frame")


@app.route("/")
def index():
    """Video streaming home page."""
    return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True)
