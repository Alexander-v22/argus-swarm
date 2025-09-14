import cv2
import time
import numpy as np
from ultralytics import YOLO
import os, sys

def start_detection(args):
    # --- sanity: require a real model file ---
    if os.path.isdir(args.model):
        print(f"ERROR: --model points to a directory: {args.model}. Pass a model FILE like .pt/.onnx/.torchscript")
        sys.exit(1)

    print(f"[info] loading model: {args.model}")
    model = YOLO(args.model, task='detect')

    # --- force CPU to avoid backend init stalls ---
    try:
        model.to('cpu')
        print("[info] model set to CPU")
    except Exception as e:
        print(f"[warn] couldn't force CPU: {e}")

    labels = model.names

    # --- open camera 0 (use V4L2 on Pi) ---
    opencam = cv2.VideoCapture(0, cv2.CAP_V4L2)
    if not opencam.isOpened():
        print("ERROR: camera index 0 didn't open. Try a different index or /dev/videoN")
        sys.exit(1)

    # Prefer MJPG to reduce CPU load on Pi
    try:
        opencam.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc(*"MJPG"))
    except Exception:
        pass

    # Set resolution if user specified it
    resize = False
    if args.resolution:
        resize = True
        resW, resH = map(int, args.resolution.lower().split('x'))
        opencam.set(cv2.CAP_PROP_FRAME_WIDTH, resW)
        opencam.set(cv2.CAP_PROP_FRAME_HEIGHT, resH)

    # --- warmup: run a single dummy inference to verify the model actually executes ---
    try:
        _ = model.predict(source=np.zeros((480, 640, 3), dtype=np.uint8),
                          conf=getattr(args, "thresh", 0.5),
                          imgsz=640,
                          verbose=True)
        print("[info] warmup inference OK")
    except Exception as e:
        print(f"ERROR: model inference failed during warmup: {e}")
        sys.exit(1)

    bbox_colors = [(0, 255, 0), (0, 0, 255), (255, 0, 0)]
    avg_frame_rate = 0.0
    frame_rate_buffer = []
    fps_avg_len = 100

    print("Press 'q' to quit.")
    while True:
        t_start = time.perf_counter()

        ret, frame = opencam.read()
        if not ret or frame is None:
            print("Unable to read from webcam. Exiting.")
            break

        if resize:
            frame = cv2.resize(frame, (resW, resH))

        # Use built-in confidence filter (faster than filtering after)
        results = model.predict(source=frame,
                                conf=getattr(args, "thresh", 0.5),
                                imgsz=640,  # try 416/320 if you want more FPS
                                verbose=False)
        detections = results[0].boxes
        object_count = 0

        if detections is not None and len(detections) > 0:
            xyxy = detections.xyxy.cpu().numpy().astype(int)
            clss = detections.cls.cpu().numpy().astype(int)
            confs = detections.conf.cpu().numpy()

            for i in range(xyxy.shape[0]):
                xmin, ymin, xmax, ymax = xyxy[i].tolist()
                classidx = clss[i]
                conf = confs[i]
                if conf >= getattr(args, "thresh", 0.5):
                    color = bbox_colors[classidx % len(bbox_colors)]
                    cv2.rectangle(frame, (xmin, ymin), (xmax, ymax), color, 2)
                    name = labels[classidx] if isinstance(labels, (list, tuple)) else labels.get(classidx, str(classidx))
                    cv2.putText(frame, f"{name}: {int(conf*100)}%",
                                (xmin, max(ymin-5, 15)),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2)
                    object_count += 1

        cv2.putText(frame, f'FPS: {avg_frame_rate:.2f}', (10, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2)
        cv2.putText(frame, f'Objects detected: {object_count}', (10, 45), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2)
        cv2.imshow("YOLO Detection", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

        dt = time.perf_counter() - t_start
        if dt > 0:
            fr = 1.0 / dt
            if len(frame_rate_buffer) >= fps_avg_len:
                frame_rate_buffer.pop(0)
            frame_rate_buffer.append(fr)
            avg_frame_rate = float(np.mean(frame_rate_buffer))

    opencam.release()
    cv2.destroyAllWindows()
