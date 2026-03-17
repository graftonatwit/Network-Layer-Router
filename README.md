# Network-Layer-Router
Simplified Router Simulation
Overview

router.py is a Python-based network-layer router simulator designed to model the behavior of packet queues under various scheduling disciplines. It reads datagram arrivals from standard input and processes them according to user-specified queueing policies.

This starter code provides a foundation for studying queueing disciplines, including First-Come-First-Served (FCFS), Priority Queuing, Round Robin (RR), and optionally Weighted Fair Queueing (WFQ).

Features

Packet Parsing
Reads datagrams with the following format:

<arrival_time_ms> <flow_id> <priority> <size_bytes> <payload>

Example:

12.0 2 1 512 DATA_42

Queueing Disciplines

FCFS – Processes packets in arrival order.

Priority Queue – Strict priority-based scheduling (min-heap).

Round Robin (RR) – Cycles through flows fairly.

Weighted Fair Queueing (WFQ) – Extra credit: cycles through flows based on user-specified weights.

Simulation Control

Adjustable output/transmission rate (packets per second).

Easy extension for additional queueing policies and statistics.

Usage
Run with FCFS (default)
python3 router.py --policy fcfs < datagrams.txt
Run with Priority Queuing
python3 router.py --policy priority < datagrams.txt
Run with Round Robin
python3 router.py --policy rr < datagrams.txt
Run with Weighted Fair Queueing (Extra Credit)
python3 router.py --policy wfq --weights 3,2,1 < datagrams.txt
Optional Parameters

--output_rate : Transmission rate in packets per second (default: 10.0).

--weights : Comma-separated list of weights for WFQ scheduling.

Packet Class

The Packet class represents a network datagram:

arrival_time – float, in milliseconds

flow_id – integer, flow identifier

priority – integer, packet priority

size – integer, size in bytes

payload – string data

Example:

pkt = Packet(12.0, 2, 1, 512, "DATA_42")
QueueManager Class

The QueueManager handles packets according to the selected policy:

enqueue(pkt) – Adds a packet to the appropriate queue.

dequeue() – Removes the next packet according to the scheduling discipline.

Policy Behavior:

Policy	Behavior
fcfs	Dequeues packets in the order they arrived.
priority	Dequeues packets with the lowest priority number first.
rr	Round-robin over flow queues to ensure fairness among flows.
wfq	Cycles through flows according to weights, dequeuing packets fairly.
Example Input File (datagrams.txt)
0.0 1 0 512 DATA_1
1.0 2 1 256 DATA_2
2.0 1 0 1024 DATA_3
3.0 3 2 512 DATA_4

Run simulation:

python3 router.py --policy rr < datagrams.txt

Expected console output:

[INPUT] Packet(flow=1, prio=0, size=512, payload='DATA_1')
[INPUT] Packet(flow=2, prio=1, size=256, payload='DATA_2')
[SEND] Packet(flow=1, prio=0, size=512, payload='DATA_1')
[SEND] Packet(flow=2, prio=1, size=256, payload='DATA_2')
Notes

Currently, router.py is a starter simulation (Week 1).

The WFQ policy is optional and considered extra credit.

You can extend the code to track metrics like average delay, queue length, and packet drops.

Sleep intervals simulate real-time packet transmission based on --output_rate.

Author

Trevor Grafton

Implements a simplified router simulator suitable for networking labs and algorithm practice.

