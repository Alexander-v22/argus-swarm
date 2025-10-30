# Argus – AI-Controlled Turret (Prototype)

Argus is my project to create an AI-controlled turret system. This repository marks the early development phase of the system. The long-term goal is to integrate Argus into the larger **Aegis** framework, where it will work alongside autonomous robots for surveillance, interception, and swarm coordination.

## Current Status

**Working:**
- YOLO object detection with person tracking
- Real-time video streaming via FastAPI
- ESP32-based servo control (pan/tilt) via UART
- Proportional control system for smooth tracking
- Automatic centering when no target detected

**In Development:**
-  MQTT communication protocol for Aegis integration
-  Multi-unit coordination and swarm behavior
-  Enhanced tracking algorithms
-  Mesh network resilience
---

## System Overview
Argus uses a vision-based tracking system that:
1. Detects persons using YOLOv8 with BoT-SORT tracking
2. Calculates target position relative to frame center
3. Sends pan/tilt commands to ESP32 microcontroller via UART
4. Controls servos to keep target centered in frame
5. Streams annotated video feed over HTTP

### Hardware Components
- **Camera**: Logitech Brio 101 Full HD 1080p Webcam 
- **Microcontroller**: ESP32 (UART serial communication at 115200 baud)
- **Servos**: Pan/tilt servo mount (0-180° range)
- **Host**: Raspberry Pi 5

### Intelligent Tracking
- **Proportional Control**: Smooth servo movement with configurable gain (Kp)
- **Low-pass Filtering**: Alpha blending prevents jerky movements
- **Dead Zone**: 20px threshold prevents micro-adjustments
- **Auto-Reset**: Returns to center position after 2 seconds of no detection

### Performance Optimizations
To maintain high frame rates, the system skips frames and only runs detection on every second frame. Video streaming uses MJPEG compression with adjustable quality settings to balance bandwidth and visual fidelity. Buffer management keeps latency low by maintaining a minimal buffer size of 1 frame. FPS metrics are averaged over 100 frames to provide stable performance readings without rapid fluctuation.

### Communication Infrastructure
- **UART**: Direct servo control via ESP32 (`/dev/ttyAMA0`)
- **MQTT**: Framework for future Aegis unit coordination (in progress)
- **HTTP**: Real-time video streaming at `/video` endpoint


## The Vision: Aegis Integration

Argus is designed as a stationary sensor node within the Aegis autonomous defense network:

**Planned Capabilities:**
- **Distributed Detection**: Share target coordinates across multiple Argus units
- **Swarm Coordination**: Collaborate with mobile Aegis robots for tracking
- **Threat Assessment**: Prioritize targets based on behavior and proximity
- **Redundancy**: Maintain operation if individual units fail
- **Mesh Communication**: Operate without centralized control

**Potential Real-World Use Cases:**
- Perimeter monitoring for large properties
- Wildlife observation and documentation
- Security system integration
- Autonomous patrol coordination



## Roadmap

**Phase 1: Core Detection** ✅ (Current)
- Object detection and tracking
- Servo control integration
- Video streaming

**Phase 2: Communication** 🔨 (In Progress)
- MQTT message protocol design
- Target coordinate sharing
- Multi-unit synchronization

**Phase 3: Intelligence**
-  Behavioral analysis and threat scoring
-  Predictive tracking algorithms
-  Automatic handoff between units

**Phase 4: Aegis Integration**
-  Mobile robot coordination
-  Mesh network implementation
-  Fault-tolerant operation
-  Autonomous patrol patterns


## Credits

This detection script is adapted from the work of [EdjeElectronics](https://github.com/EdjeElectronics/Train-and-Deploy-YOLO-Models). Their repository provides an excellent foundation for training and deploying YOLO models.
