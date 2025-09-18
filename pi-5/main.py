import argparse
import uvicorn 
from detection import yolo_detect


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--model', required=True, help='Path to YOLO model file (example: "runs/detect/train/weights/best.pt")')
    parser.add_argument('--thresh', type=float, default=0.5, help='Minimum confidence threshold')
    parser.add_argument('--resolution', default=None, help='Resolution in WxH (example: "640x480")')
    parser.add_argument('--port', type=int, default=8000, help='HTTP port for the video server')
    args = parser.parse_args()

    app, cleanup = yolo_detect.start_detection(args)

    try:
        uvicorn.run(app, host="0.0.0.0", port=args.port, log_level="warning")
    finally:
        cleanup()

if __name__ == "__main__":
    main()


