import cv2 # import OpenCV libraries 
import time
import numpy as np
from ultralytics import YOLO

from fastapi import FastAPI 
from fastapi.responses import StreamingResponse

def start_detection(args):
    # Load YOLO model
    model = YOLO(args.model, task='detect')
    labels = model.names  # dictionary of class names (e.g., {0: 'person', 1: 'bicycle', ...})

    # Open webcam (0 = default camera)
    opencam = cv2.VideoCapture(0, cv2.CAP_V4L2)
    opencam.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc(*"MJPG"))
    opencam.set(cv2.CAP_PROP_FPS, 30)
    opencam.set(cv2.CAP_PROP_BUFFERSIZE, 1) 


    # The values of 3 and 4 are tied to OpenCV libraries 
    # 3 - cv2.CAP_PROP_FRAME_WIDTH
    # 4 - cv2.CAP_PROP_FRAME_HEIGHT

    # Set resolution if user specified it
    resize = False
    if args.resolution:
        resize = True
        resW, resH = int(args.resolution.split('x')[0]), int(args.resolution.split('x')[1]) # this creates a canvas which can be coded to map the servos 
        opencam.set(3, resW)
        opencam.set(4, resH)
    if not opencam.isOpened():
        raise RuntimeError("Unable to find camera(/dev/video).")        

    
    # Bounding box colors
    bbox_colors = [(0, 255, 0), (0, 0, 255), (255, 0, 0)]  # green, red, blue

    # Variables for FPS calculation
    avg_frame_rate = 0
    frame_rate_buffer = []
    fps_avg_len = 100

    DETECT_EVERY = 2
    frame_i = 0
    last_boxes = None

    # Inference loop
    def start_stream():
        nonlocal avg_frame_rate, frame_i, last_boxes 
        while True:
            t_start = time.perf_counter() # returns the value of a high resolution performance counter measured in fractional seconds

            # Grab a frame from webcam applying ret -> boolean flag to make sure the frame is valid
            ret, frame = opencam.read() # "," tuple packing allowing to set ret and frame the same value

            run_det = (frame_i) % DETECT_EVERY == 0
            if not ret:
                print("Unable to read from webcam. Trying Again.")
                time.sleep(0.02)
                continue
                
            # Resize if requested
            if resize:
                frame = cv2.resize(frame, (resW, resH))

            # Run YOLO detection
            run_det = (frame_i % DETECT_EVERY == 0)
            if run_det:
                results = model(frame, verbose=False)
                last_boxes = results[0].boxes

            detections = last_boxes
            frame_i += 1

            object_count = 0

            # Loop through detections
            for i in range(len(detections)):
                # Get bounding box
                xyxy = detections[i].xyxy.cpu().numpy().squeeze().astype(int)
                xmin, ymin, xmax, ymax = xyxy

                # Get class and confidence
                classidx = int(detections[i].cls.item())
                classname = labels[classidx]
                conf = detections[i].conf.item()

                # Draw any object above threshold
                if conf > args.thresh:
                    color = bbox_colors[classidx % len(bbox_colors)]
                    cv2.rectangle(frame, (xmin, ymin), (xmax, ymax), color, 2)

                    label = f'{classname}: {int(conf*100)}%'
                    cv2.putText(frame, label, (xmin, max(ymin-5, 15)), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2)
                    object_count += 1
                      # Calculate FPS

            # Draw FPS
            t_stop = time.perf_counter()
            frame_rate_calc = 1.0 / (t_stop - t_start)
            if len(frame_rate_buffer) >= fps_avg_len:
                frame_rate_buffer.pop(0)
            frame_rate_buffer.append(frame_rate_calc)
            avg_frame_rate = np.mean(frame_rate_buffer)

            # Draw FPS count on screen 
            cv2.putText(frame, f'FPS: {avg_frame_rate:.2f}', (10, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2)

            # Draw object count
            cv2.putText(frame, f'Objects detected: {object_count}', (10, 45), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2)

            ok, buf = cv2.imencode(".jpg", frame, [int(cv2.IMWRITE_JPEG_QUALITY), 80])
            if not ok:
                continue
            jpg = buf.tobytes()
            yield (b"--frame\r\nContent-Type: image/jpeg\r\n\r\n" + jpg + b"\r\n")



    app = FastAPI()

    @app.get("/video")    
    def video():
        return StreamingResponse(
            start_stream(),
            media_type="multipart/x-mixed-replace; boundary=frame"
        )

    

    # Cleanup
    def cleanup():
        try:
            opencam.release()
            cv2.destroyAllWindows()
        except Exception:
            pass

    return app, cleanup
