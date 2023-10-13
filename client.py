import socket
import select
import sys
import pickle


# client_request = (file_name, offset_b, num_bytes_chunk_s)
# client must be able to deal with the situation where a request is not replied
# returns false in the case that the server doesn't respond in one second
def waitForReply( uSocket ):
    rx, tx, er = select.select( [uSocket], [], [], 1)
    # waits for data or timeout after 1 second
    if rx==[]:
        return False
    else:
        return True

# client must be envoked with
#   python client.py host_of_server portSP fileName chunkSize

# create socket sc and bind it to some UDP port
# open local file for writing
# offset = 0
# while TRUE:
#   prepare request(fileName,offset,size) and serialize it with pickle

#   This is how we serialize using pickle
#   request = (fileName, offset, blockSize)
#   req = pickle.dumps(request)
#   UDPSocket.sendto(req, endpoint)

#   send the request to (host_of_server, portSP)
#   wait for reply; if reply does not arrive, repeat request
#   write byte chunk received to file
#   if EOF
#       break
#   else
#       offset = offset + size

# OPTINAL TODO: Study Performance

#---------------------------------------- CODE ----------------------------------------------#


msgFromClient       = "Hello UDP Server"

bytesToSend         = str.encode(msgFromClient)

serverAddressPort   = ("127.0.0.1", 20001)
bufferSize          = 1024
serverName = "localhost"
clientPort = 12000

WRITE_BINARY = "wb"

 # Create a UDP socket at client side
UDPClientSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
UDPClientSocket.bind(("0.0.0.0", clientPort))

# Collect the input and put it into variables
args = sys.argv[1:]

host_of_server = args[0]
portSP = int(args[1])
fileName = args[2]
chunkSize = int(args[3])

print(f'host_of_server= {host_of_server},portSP={portSP},fileName={fileName}, chunkSize={chunkSize}')

offset = 0

with open(fileName, WRITE_BINARY) as file:
    while True:
        # Create request
        request = (fileName, offset, chunkSize)
        req = pickle.dumps(request)
        # Send to server using created UDP socket
        UDPClientSocket.sendto(req, (host_of_server, portSP))

        # wait for reply; if reply does not arrive, repeat request
        if waitForReply(UDPClientSocket):
            replyServer, address = UDPClientSocket.recvfrom(bufferSize)

            reply = pickle.loads(replyServer)

            status = reply[0]

            no_of_bytes_read = reply[1]

            file_chunk = reply[2]

            if status == 0:
                file.write(file_chunk)
                offset = offset + chunkSize

            if no_of_bytes_read < chunkSize:
                break

            if status == 1:
                print("File not Found")

            if status == 2:
                print("Invalid Offset")
