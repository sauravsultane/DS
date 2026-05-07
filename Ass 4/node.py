import socket
import time
import random
import sys

def start_node(node_id, host='localhost', port=8000):

    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    client.connect((host, port))

    # Simulated clock drift
    drift = random.uniform(-5, 5)

    local_time = time.time() + drift

    print(f"[Node {node_id}] Initial Time: {local_time}")

    while True:

        data = client.recv(1024).decode()

        if data == 'GET_TIME':

            # Send local clock time
            client.sendall(str(local_time).encode())

        elif data.startswith('OFFSET'):

            offset = float(data.split(':')[1])

            # Adjust local clock
            local_time += offset

            print(f"[Node {node_id}] Adjusted by {offset:+.2f} seconds")

            print(f"[Node {node_id}] New Time: {local_time}")

            break

    client.close()


if __name__ == "__main__":

    node_id = int(sys.argv[1]) if len(sys.argv) > 1 else 1

    start_node(node_id)