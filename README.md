# Halo MCU-ECU CAN Bus Simulator

Three-node virtual-CAN communication simulator for Halo's MCU/ECU CAN architecture.

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
python3 sim.py all
python3 sim.py all --fault-after 10
```
Or run each node separately:
```bash
python3 sim.py mcu
python3 sim.py epr
python3 sim.py etc
```

At the final thrust-profile timestamp, the MCU sends zero thrust followed by
the shutdown CAN frame (`0x102`, standard ID, empty payload). EPR reports SAFE
with a vent request, and ETC reports INHIBITED with zero actuator output, then
all nodes close their CAN buses and exit. In `all` mode, the launcher waits up
to five seconds for remaining nodes to exit before terminating stuck tasks.
You can also send the shutdown frame to EPR and ETC with `cansend vcan0 102#`.

## Thrust plotter
Install Matplotlib
```bash
python -m pip install matplotlib
```
Run plotter (optionally with specific file):
```bash
python visualize_thrust_profile.py [file]
```
