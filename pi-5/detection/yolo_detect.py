import cv2 # import OpenCV libraries 
import time
import numpy as np
from ultralytics import YOLO

from fastapi import FastAPI 
from fastapi.responses import StreamingResponse
from esp_comms.uart_con import ESP32UART



def start_detection(args):
    print("1 - loading model...")
    model = YOLO(args.model, task="detect")
    labels = model.names
    print("2 - model loaded")

    print("3 - opening camera...")
    opencam = cv2.VideoCapture(0, cv2.CAP_V4L2)
    opencam.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc(*"MJPG"))
    opencam.set(cv2.CAP_PROP_FPS, 30)
    opencam.set(cv2.CAP_PROP_BUFFERSIZE, 1)
    print("4 - camera opened")

    resize = False
    if args.resolution:
        resize = True
        resW, resH = int(args.resolution.split('x')[0]), int(args.resolution.split('x')[1])
        opencam.set(3, resW)
        opencam.set(4, resH)

    if not opencam.isOpened():
        raise RuntimeError("Unable to find camera(/dev/video).")

    bbox_colors = [(0, 255, 0), (0, 0, 255), (255, 0, 0)]

    avg_frame_rate = 0
    frame_rate_buffer = []
    fps_avg_len = 100

    DETECT_EVERY = 2
    frame_i = 0
    last_boxes = None

    print("5 - starting uart...")
    uart = ESP32UART("/dev/ttyAMA0", 115200, timeout=0.5)
    pan_angle = 90
    tilt_angle = 90
    uart.send_angles(pan_angle, tilt_angle)
    print("6 - uart ready, starting uvicorn...")

    def start_stream():
        nonlocal avg_frame_rate, frame_i, last_boxes, tilt_angle, pan_angle
        last_seen = time.time()
        while True:
            t_start = time.perf_counter()

            ret, frame = opencam.read()

            run_det = (frame_i) % DETECT_EVERY == 0
            if not ret:
                print("Unable to read from webcam. Trying Again.")
                time.sleep(0.02)
                continue

            if resize:
                frame = cv2.resize(frame, (resW, resH))

            run_det = (frame_i % DETECT_EVERY == 0)
            if run_det:
                results = model.track(frame, persist=True, tracker="botsort.yaml", verbose=False)
                detections = results[0].boxes

            t_stop = time.perf_counter()
            frame_rate_calc = 1 / (t_stop - t_start)
            if len(frame_rate_buffer) >= fps_avg_len:
                frame_rate_buffer.pop(0)
            frame_rate_buffer.append(frame_rate_calc)
            avg_frame_rate = np.mean(frame_rate_buffer)

            object_count = 0
            best_det = None
            best_conf = 0

            for i in range(len(detections)):
                xyxy = detections[i].xyxy.cpu().numpy().squeeze().astype(int)
                xmin, ymin, xmax, ymax = xyxy

                classidx = int(detections[i].cls.item())
                classname = labels[classidx]
                conf = detections[i].conf.item()

                if conf > args.thresh and classname == "person":
                    color = bbox_colors[classidx % len(bbox_colors)]
                    cv2.rectangle(frame, (xmin, ymin), (xmax, ymax), color, 2)
                    label = f'{classname}: {int(conf*100)}%'
                    cv2.putText(frame, label, (xmin, max(ymin-5, 15)), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2)
                    object_count += 1

                    if conf > best_conf:
                        best_conf = conf
                        best_det = (xmin, ymin, xmax, ymax)

            if best_det is not None:
                xmin, ymin, xmax, ymax = best_det
                cenx = (xmax + xmin) // 2
                ceny = (ymax + ymin) // 2

                y_thresh= 440
                box_height = ymax -ymin #tells me the box hight the inner canvas 
                print(f"box_height={box_height}")
                distx = cenx - (resW // 2)
                disty = ceny - (resH // 2)
                print(f"distx={distx}, disty={disty}, pan={pan_angle:.1f}, tilt={tilt_angle:.1f}, box_height= {box_height:.1f}")

                kp_pan = 0.3
                kp_tilt = 0.3
                alpha = 0.1

                target_pan = pan_angle - distx * kp_pan if abs(distx) > 20 else pan_angle

                if box_height < y_thresh and abs(disty) > 20: 
                    target_tilt = tilt_angle - disty * kp_tilt 

                else:
                    target_tilt = tilt_angle

                pan_angle = (1 - alpha) * pan_angle + alpha * target_pan
                tilt_angle = (1 - alpha) * tilt_angle + alpha * target_tilt

                pan_angle = max(0, min(180, pan_angle))
                tilt_angle = max(0, min(180, tilt_angle))
                last_seen = time.time()
                uart.send_angles(pan_angle, tilt_angle)
            else:
                if time.time() - last_seen > 2:
                    pan_angle = 90
                    tilt_angle = 135
                    uart.send_angles(pan_angle, tilt_angle)

            cv2.putText(frame, f'FPS: {frame_rate_calc:.2f}', (10, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (173, 216, 230), 2)
            cv2.putText(frame, f'Objects detected: {object_count}', (10, 45), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (173, 216, 230), 2)

            ok, buf = cv2.imencode(".jpg", frame, [int(cv2.IMWRITE_JPEG_QUALITY), 50])
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

    def cleanup():
        try:
            opencam.release()
            cv2.destroyAllWindows()
        except Exception:
            pass

    return app, cleanup