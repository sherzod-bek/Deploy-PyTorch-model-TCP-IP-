import socket  # Import socket module
import pickle  # Import pickle module
from Predict import Predict


# Host ip and port (for connection)
HOST = '111.111.11.111'
PORT = 50007

# create TCP/IP socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

# bind the socket to the port 50007
s.bind((HOST, PORT))

# listen for incoming connections (server mode) with one connection at a time
s.listen(1)

#headersize for recieving data
HEADERSIZE = 10

while True:
    conn, addr = s.accept()
    print('Connected by', addr)

    # recieving data-----------------
    while True:
        data = None
        complete_info = b''
        rec_msg = True
        done = False

        while True:
            mymsg = conn.recv(HEADERSIZE)
            if rec_msg:
                try:
                    x = int(mymsg[:HEADERSIZE ])
                except:
                    done = True
                    x = 0
                rec_msg = False
            if done == False:
                complete_info += mymsg
                if len(complete_info)-HEADERSIZE == x:
                    data = pickle.loads(complete_info[HEADERSIZE:])
                    rec_msg = True
                    complete_info = b''
            if done:
                break
        break
    # ----------------------------------
    pre = Predict()
    res = pre.prediction(data['img'])[0][0]
    # send result back
    # print(res.item())
    conn.send(bytes(str(res.item()),'utf-8'))

    # Clean up the connection
    conn.shutdown(socket.SHUT_WR)
    conn.close()
