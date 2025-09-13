import cv2 # import OpenCV libraries 
import time
import numpy as np
from ultralytics import YOLO

def start_detection(args):
    # Load YOLO model
    model = YOLO(args.model, task='detect')
    labels = model.names  # dictionary of class names (e.g., {0: 'person', 1: 'bicycle', ...})

    # Open webcam (0 = default camera)
    opencam = cv2.VideoCapture(0)


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

    # Bounding box colors
    bbox_colors = [(0, 255, 0), (0, 0, 255), (255, 0, 0)]  # green, red, blue

    # Variables for FPS calculation
    avg_frame_rate = 0
    frame_rate_buffer = []
    fps_avg_len = 100

    print("Press 'q' to quit.")

    # Inference loop
    while True:
        t_start = time.perf_counter() # returns the value of a high resolution performance counter measured in fractional seconds

        # Grab a frame from webcam applying ret -> boolean flag to make sure the frame is valid
        ret, frame = opencam.read()
        if not ret:
            print("Unable to read from webcam. Exiting.")
            break

        # Resize if requested
        if resize:
            frame = cv2.resize(frame, (resW, resH))

        # Run YOLO detection
        results = model(frame, verbose=False)
        detections = results[0].boxes

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

        # Draw FPS
        cv2.putText(frame, f'FPS: {avg_frame_rate:.2f}', (10, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2)

        # Draw object count
        cv2.putText(frame, f'Objects detected: {object_count}', (10, 45), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2)

        # Show the frame
        cv2.imshow("YOLO Detection", frame)

        # Quit if 'q' pressed
        if cv2.waitKey(5) & 0xFF == ord('q'):
            break

        # Calculate FPS
        t_stop = time.perf_counter()
        frame_rate_calc = 1.0 / (t_stop - t_start)

        if len(frame_rate_buffer) >= fps_avg_len:
            frame_rate_buffer.pop(0)
        frame_rate_buffer.append(frame_rate_calc)
        avg_frame_rate = np.mean(frame_rate_buffer)

    # Cleanup
    opencam.release()
    cv2.destroyAllWindows()
