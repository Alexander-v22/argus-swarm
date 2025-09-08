# Argus – AI-Controlled Turret (Prototype)

Argus is my project to create an AI-controlled turret system. This repository marks the early development phase of the system. The long-term goal is to integrate Argus into the larger **Aegis** framework, where it will work alongside autonomous robots for surveillance, interception, and swarm coordination.

At this stage, the repository contains only the detection pipeline. The code runs a YOLO model on images, videos, or live camera feeds to detect objects and draw bounding boxes. This serves as the foundation for later development, where Argus will be extended with servo and motor control for turret movement, real-time tracking logic, and networked communication with Aegis units.

The vision for Argus is:
- Detect intruders in real time
- Physically track and aim using a turret mount
- Share detections with Aegis robots over a mesh communication network
- Operate as part of a coordinated defense and monitoring system

---

## Next Steps

This repository currently uses borrowed detection code as a baseline, but it will be modified and expanded to support Argus. Upcoming work includes:
- Coding servo control for turret rotation and tilt  
- Linking detections to real-time aiming and tracking  
- Integrating the turret into the Aegis swarm communication framework  
- Building resilience so Argus can adapt if units fail or signals are disrupted  

---

## Credits

This detection script is adapted from the work of [EdjeElectronics](https://github.com/EdjeElectronics/Train-and-Deploy-YOLO-Models). Their repository provides an excellent foundation for training and deploying YOLO models.
