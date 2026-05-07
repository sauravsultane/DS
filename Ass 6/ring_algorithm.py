class RingAlgorithm:

    def __init__(self, processes):

        self.processes = sorted(processes)

        self.ring = self.processes[:]

        self.coordinator = None

    def is_alive(self, process_id):

        return process_id in self.ring

    def hold_election(self, initiator):

        print(f"Process {initiator} starts election.")

        election_list = [initiator]

        current_index = self.ring.index(initiator)

        while True:

            current_index = (current_index + 1) % len(self.ring)

            next_process = self.ring[current_index]

            if next_process == initiator:
                break

            print(f"Election message from {election_list[-1]} to {next_process}")

            election_list.append(next_process)

        winner = max(election_list)

        self.coordinator = winner

        print(f"\nProcess {winner} is elected as the new coordinator.")


# Example Usage

processes = [1, 2, 3, 4]

ring = RingAlgorithm(processes)

ring.hold_election(initiator=2)