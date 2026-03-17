#!/usr/bin/env python3
"""
router.py (Starter Code)
------------------------
This program simulates a simplified network-layer router that processes
incoming datagrams according to different queueing disciplines.

--------------------------------------------------------------
Input Format:
<arrival_time_ms> <flow_id> <priority> <size_bytes> <payload>

Example:
12.0 2 1 512 DATA_42

Usage:
    python3 router.py --policy fcfs
    python3 router.py --policy priority
    python3 router.py --policy rr
    python3 router.py --policy wfq --weights 3,2,1   # optional extra credit
--------------------------------------------------------------
"""

import sys
import argparse
from collections import deque, defaultdict
import heapq
import time


# =====================================================================
# Packet Data Structure
# =====================================================================
class Packet:
    def __init__(self, arrival_time, flow_id, priority, size, payload):
        """Represents a single network-layer packet."""
        self.arrival_time = float(arrival_time)
        self.flow_id = int(flow_id)
        self.priority = int(priority)
        self.size = int(size) # bytes
        self.payload = payload # str
    def __lt__(self, other):
        """Defines ordering for priority queues (min-heap).""" # min-heap
        return self.priority < other.priority # return
    def __repr__(self):
        return (f"Packet(flow={self.flow_id}, prio={self.priority}, " # return
                f"size={self.size}, payload='{self.payload}')") # return str
# =====================================================================
# Queue Manager
# =====================================================================
class QueueManager:
    def __init__(self, policy="fcfs", weights=None):
        self.policy = policy
        self.weights = self.parse_weights(weights)

        # Queues for different policies
        self.queue = deque()                   # FCFS
        self.heap = []                         # Priority Queue
        self.flow_queues = defaultdict(deque)  # RR / WFQ
        self.last_flow = None                  # Round Robin pointer
        # WFQ variables
        self.wfq_finish_times = defaultdict(float) # extra credit
        self.wfq_virtual_time = 0.0 # extra credit

        # WFQ weighted scheduling list
        self.wfq_schedule = []
        if self.weights:
            for fid, w in self.weights.items():
                self.wfq_schedule += [fid] * int(w)
        self.wfq_index = 0

    # -----------------------------------------------------------------
    def parse_weights(self, weights): # parse weights
        """Parse weights for WFQ (Extra Credit)."""
        if not weights: # if no weights
            return {}
        w_list = [float(w) for w in weights.split(",")] # convert str to float
        return {i + 1: w for i, w in enumerate(w_list)} # return dict

    # -----------------------------------------------------------------
    # TODO: Implement enqueue() logic for all policies
    # -----------------------------------------------------------------
    def enqueue(self, pkt):
        """
        Insert packet into the correct queue based on the selected policy.
        For now, only print debug information.
        """
        print(f"[DEBUG] Enqueued packet: {pkt}") # print packet
        if self.policy == "fcfs":
            self.queue.append(pkt)
        elif self.policy == "priority": # priority
            heapq.heappush(self.heap, pkt) # append packet
        elif self.policy == "rr": # round robin
            self.flow_queues[pkt.flow_id].append(pkt) # append packet
        elif self.policy == "wfq": # extra credit
            self.flow_queues[pkt.flow_id].append(pkt) # append packet
    # -----------------------------------------------------------------
    # TODO: Implement dequeue() logic for each policy
    # -----------------------------------------------------------------
    def dequeue(self):
        """
        Select and remove a packet based on the active scheduling policy.
        To start, return None.
        """
        # FCFS
        if self.policy == "fcfs": # fcfs
            if self.queue: #    if queue
                return self.queue.popleft() # return packet
            return None
        # PRIORITY QUEUE (strict priority)
        if self.policy == "priority": # priority
            if self.heap:
                return heapq.heappop(self.heap) # return packet
            return None
        # ROUND ROBIN
        if self.policy == "rr":    # round robin
            if not self.flow_queues: # if no flow queues
                return None
            flow_ids = sorted(self.flow_queues.keys()) # get flow ids
            if self.last_flow not in flow_ids: # if last flow not in flow ids
                self.last_flow = flow_ids[0] # set last flow
            start_index = flow_ids.index(self.last_flow) # get start index
            for i in range(len(flow_ids)): # for each flow
                fid = flow_ids[(start_index + i) % len(flow_ids)] # get flow
                if self.flow_queues[fid]: # if flow queue
                    self.last_flow = fid # set last flow
                    return self.flow_queues[fid].popleft() # return packet

            return None

        # WEIGHTED FAIR QUEUEING (Extra Credit)
        if self.policy == "wfq":
            if not self.flow_queues: # if no flow queues
                return None
            if not self.wfq_schedule: # if no wfq schedule
                return None
            for _ in range(len(self.wfq_schedule)): # for each flow
                fid = self.wfq_schedule[self.wfq_index] # get flow
                self.wfq_index = (self.wfq_index + 1) % len(self.wfq_schedule) # update index
                if self.flow_queues[fid]:
                    return self.flow_queues[fid].popleft() # return packet

            return None
        return None
# =====================================================================
# Main Router Simulation
# =====================================================================
def main():
    parser = argparse.ArgumentParser(description="Simplified Router Simulation") # create parser
    parser.add_argument("--policy", type=str,
                        choices=["fcfs", "priority", "rr", "wfq"],
                        default="fcfs",
                        help="Queueing discipline to use.") # add argument
    parser.add_argument("--output_rate", type=float, default=10.0, # add argument
                        help="Transmission rate (packets per second)") # add argument
    parser.add_argument("--weights", type=str, default=None,
                        help="Comma-separated weights for WFQ (extra credit)")
    args = parser.parse_args() # parse arguments
    queueManage = QueueManager(policy=args.policy, weights=args.weights) # create queue
    send_interval = 1.0/args.output_rate  # seconds between transmissions
    # -----------------------------------------------------------------
    # TODO: Parse input datagrams and print packet info
    # -----------------------------------------------------------------
    packets = []
    for line in sys.stdin: # loop over lines
        if not line.strip() or line.startswith("#"): # skip empty lines
            continue
        arrival_time, flow_id, priority, size, payload = line.strip().split(maxsplit=4) # parse packet
        pkt = Packet(arrival_time, flow_id, priority, size, payload) # create packet
        packets.append(pkt) # append packet
        print(f"[INPUT] {pkt}") # print packet info
    # -----------------------------------------------------------------
    # TODO: Simulate enqueue/dequeue behavior
    # -----------------------------------------------------------------
    print(f"\n[INFO] Parsed {len(packets)} packets.")
    print(f"[INFO] Policy selected: {args.policy}")
    print("[INFO] Router simulation starting...\n")

    # Basic placeholder simulation loop (to be replaced in future weeks)
    for pkt in packets: # loop over packets
        queueManage.enqueue(pkt)  # insert packet
        time.sleep(send_interval)  # wait
        output = queueManage.dequeue() # remove packet
        if output:
            print(f"[SEND] {output}") # print packet

    print("\n[INFO] Simulation complete (Week 1 base run).") # print completion message

if __name__ == "__main__":
    main()