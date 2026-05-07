import socket
import threading
import json
import time

client_offsets = {}
client_connections = {}

def handle_client(conn, addr, node_id):

    global client_offsets

    print(f"Connected to node {node_id} at {addr}")

    while True:
        try:
            # Step 1: Ask for time
            conn.sendall(b'GET_TIME')

            data = conn.recv(1024).decode()

            if not data:
                break

            client_time = float(data)

            print(f"Node {node_id} time: {client_time}")

            client_offsets[node_id] = client_time

            break

        except:
            break


def start_server(host='localhost', port=8000, expected_clients=3):

    global client_connections

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    server.bind((host, port))

    server.listen()

    print(f"Coordinator listening on {host}:{port}")

    node_id = 1

    while len(client_connections) < expected_clients:

        conn, addr = server.accept()

        client_connections[node_id] = conn

        threading.Thread(
            target=handle_client,
            args=(conn, addr, node_id)
        ).start()

        node_id += 1

    # Wait for all clients
    while len(client_offsets) < expected_clients:
        time.sleep(1)

    # Step 2: Compute average offset
    local_time = time.time()

    all_times = list(client_offsets.values()) + [local_time]

    average_time = sum(all_times) / len(all_times)

    print(f"Local time: {local_time}")

    print(f"Average network time: {average_time}")

    # Step 3: Send offset
    for node_id, conn in client_connections.items():

        offset = average_time - client_offsets[node_id]

        conn.sendall(f"OFFSET:{offset}".encode())

        print(f"Sent offset {offset:+.2f} to node {node_id}")

    server.close()


if __name__ == "__main__":
    start_server()