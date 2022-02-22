from flask import Flask, Response
from model.detect import run

app = Flask(__name__)


class Args:
    model = "water-hyacinth-model.tflite"
    cameraId = 0
    frameWidth = 640
    frameHeight = 480
    numThreads = 4
    enableEdgeTPU = False


@app.route("/")
def index():
    return "hEllo"


@app.route("/video_feed")
def video_feed():
    args = Args()

    return Response(
        run(
            args.model,
            int(args.cameraId),
            args.frameWidth,
            args.frameHeight,
            int(args.numThreads),
            bool(args.enableEdgeTPU),
        ),
        mimetype="multipart/x-mixed-replace; boundary=frame",
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=2204, threaded=True)
