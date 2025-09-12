import argparse
from detection import yolo_detect
from esp_comms import uart_con 

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--model', required=True, help='Path to YOLO model file (example: "runs/detect/train/weights/best.pt")')
    parser.add_argument('--thresh', type=float, default=0.5, help='Minimum confidence threshold')
    parser.add_argument('--resolution', default=None, help='Resolution in WxH (example: "640x480")')

    args = parser.parse_args()
    yolo_detect.start_detection(args)

if __name__ == "__main__":
    main()


