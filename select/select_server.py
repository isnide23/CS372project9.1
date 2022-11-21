# Example usage:
#
# python select_server.py 3490

import sys
import socket
import select


def run_server(port):
    s = socket.socket()
    s.bind(("", port))
    s.listen()

    read_set = [s]
    # main loop:
    while True:
    # call select() and get the sockets that are ready to read
        ready_to_read, _, _ = select.select(read_set, {}, {})

    # for all sockets that are ready to read:
        for r_sock in ready_to_read:
        #   if the socket is the listener socket:
        #   accept() a new connection
        #   add the new socket to our set!
            if r_sock is s:
                client_con, client_addr = s.accept()
                print(f"{client_addr}: connected")

                read_set.append(client_con)
        #   else the socket is a regular socket:
        #   recv() the data from the socket
            else:
                data = r_sock.recv(4096)
        #   if you receive zero bytes
        #   the client hung up
        #   remove the socket from tbe set!
                if not data:
                    print(f"{r_sock.getpeername()}: disconnected")

                    read_set.remove(r_sock)
                else:
                    print(f"{r_sock.getpeername()}: {len(data)} bytes: {data}")

  

#--------------------------------#
# Do not modify below this line! #
#--------------------------------#

def usage():
    print("usage: select_server.py port", file=sys.stderr)

def main(argv):
    try:
        port = int(argv[1])
    except:
        usage()
        return 1

    run_server(port)

if __name__ == "__main__":
    sys.exit(main(sys.argv))
