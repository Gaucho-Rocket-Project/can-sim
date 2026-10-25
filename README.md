# CAN Bus Simulator

Three-node virtual-CAN communication simulator for TVC/ECU architecture.

NO REAL PROPULSION CONTROL: all pressure, temperature, and actuator data are
synthetic; the percent-to-actuator assignment is a placeholder for testing
CAN messaging only. No hardware outputs, calibrated conversion, or valve logic.

## Setup

Install the dependencies:
```bash
sudo apt install can-utils iproute2 python3-pip
python3 -m pip install python-can
```

Create the virtual CAN network:
```bash
sudo modprobe vcan
sudo ip link add dev vcan0 type vcan
sudo ip link set vcan0 up
```
Check the interface:
```bash
ip link show vcan0
```
Monitor CAN traffic:
```bash
candump vcan0
```
Send CAN Frame:
```bash
cansend vcan0 <id>#<message>
```

## Usage 
on Linux after creating vcan0:
```bash
python3 ecu_can_sim.py all
python3 ecu_can_sim.py all --fault-after 10
```
Or run each node separately:
```bash
python3 ecu_can_sim.py mcu
python3 ecu_can_sim.py press
python3 ecu_can_sim.py throttle
```

## Thrust plotter
Install Matplotlib
```bash
python -m pip install matplotlib
```
Run plotter (optionally with specific file):
```bash
python visualize_thrust_profile.py [file]
```