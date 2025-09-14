import argparse
from detection import yolo_detect

def start_uart_thread():
    def _runner():
        # import happens inside the thread; its top-level loop runs here
        import esp_comms.uart_con  # do NOT import this at the top of main.py
    t = threading.Thread(target=_runner, daemon=True)
    t.start()
    return t


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--model', required=True, help='Path to YOLO model file (example: "runs/detect/train/weights/best.pt")')
    parser.add_argument('--thresh', type=float, default=0.5, help='Minimum confidence threshold')
    parser.add_argument('--resolution', default=None, help='Resolution in WxH (example: "640x480")')
    

    args = parser.parse_args()
    yolo_detect.start_detection(args)

if __name__ == "__main__":
    main()


