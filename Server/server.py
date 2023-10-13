import socket
import random
import pickle
import os


# server reply - (status - (0,1,2), num_transfered_bytes, the actual bytes)

def serializeAndSend(UDPSocket, fileName):
    return 0

# the reply can be lost
def serverReply (msg, sock, address):
    # msg is a byte array ready to be sent
    # Generate random number in the range of 0 to 10
    rand = random.randint(0, 10)
    # If rand is less is than 3, do not respond
    if rand >= 3:
        return sock.sendto(msg, address)

# checks if the offset is valid
def isOffsetValid (fileName, offset, noBytes):
    file_size = os.path.getsize(fileName)
    # Offset cannot be negative nor bigger than the file size
    if offset < 0 or offset >= file_size:
        return False
    # If the offset plus size exceeds the file size, the chunk is too large

    # The offset is valid
    return True

# server is invoked with:
#   python server.py portSP

# create socket ss and bind it to portSP
# while TRUE:
#   receive datagram with request and deserialize it using pickle.

#   This is how we deserialize using pickle
#   message, address = sock.recvfrom(1024)
#   request=pickle.loads(message)
#   fileName = request[0]
#   offset = request[1]
#   noBytes = request[2]
#   print(f'file= {fileName},offset={offset},noBytes={noBytes}')

#
#   open file for reading
#   if open fails reply with a datagram with status 1; the other fields must be filled

#   verify if the offset is valid using os.path.filesize(…) method
#   (had to use os.path.getsize because filesize doesn't exist!!!)
#   if open fails reply with a datagram with status 2

#   if both previous tests succeed use seek to position the file pointer
#   in the required position and try to read S bytes from the file
#   reply with a tuple (0, no_of_bytes_read, file_chunk)

#   serialize the reply using pickle and call serverReply

#   This is how we serialize using pickle
#   request = (fileName, offset, blockSize)
#   req = pickle.dumps(request)
#   UDPSocket.sendto(req, endpoint)

# OPTINAL TODO: Study Performance

#---------------------------------------- CODE ----------------------------------------------#

SERVER_DIR = "server"

localIP     = "127.0.0.1"
localPort   = 20001
bufferSize  = 32000
serverName = "localhost"

UDP_RUNNING = "UDP server up and listening"
CLOSE_SOCKET = "i want to close client socket"
OK = "0-OK"
FILE_NOT_FOUND = "1 - file does not exist"
INVALID_OFFSET = "2 - invalid offset"
READ_BINARY = "rb"

msgFromServer       = "Hello UDP Client"
bytesToSend         = str.encode(msgFromServer)

 # Create a datagram socket
UDPServerSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

 # Bind to address and ip
UDPServerSocket.bind((localIP, localPort))

print(UDP_RUNNING)

 # Listen for incoming datagrams
while True:
    try:
        #   receive datagram with request and deserialize it using pickle.
        message, address = UDPServerSocket.recvfrom(bufferSize)

        request=pickle.loads(message)
        fileName = request[0]
        offset = request[1]
        noBytes = request[2]
        print(f'file= {fileName},offset={offset},noBytes={noBytes}')

        try:
            #   open file for reading
            with open(fileName, READ_BINARY) as file:
                # Reached the end of the file
                if offset + noBytes >= os.path.getsize(fileName):

                    # Calculate how many bytes are left in the file from the current offset
                    bytes_left = os.path.getsize(fileName) - offset
                    file.seek(offset)
                    chunkRead = file.read(bytes_left)

                    #   reply with a tuple (0, no_of_bytes_read, file_chunk)
                    reply = (0, len(chunkRead), chunkRead)

                    #   serialize the reply using pickle and call serverReply
                    replySerialized = pickle.dumps(reply)
                    serverReply(replySerialized, UDPServerSocket, address)

                    if not chunkRead:
                        break
                else:
                    #   verify if the offset is valid using os.path.filesize(…) method
                    if not isOffsetValid(fileName, offset, noBytes):
                        raise ValueError(INVALID_OFFSET)

                    #   use seek to position the file pointer
                    #   in the required position and try to read S bytes from the file
                    file.seek(offset)
                    chunkRead = file.read(noBytes)

                    #   reply with a tuple (0, no_of_bytes_read, file_chunk)
                    reply = (0, len(chunkRead), chunkRead)

                    #   serialize the reply using pickle and call serverReply
                    replySerialized = pickle.dumps(reply)
                    serverReply(replySerialized, UDPServerSocket, address)
        #   File not found
        except FileNotFoundError:
            reply = (1, 0, 0)
            replySerialized = pickle.dumps(reply)
            serverReply(replySerialized, UDPServerSocket, address)

        #   Invalid Offset
        except ValueError as e:
            reply = (2, 0, 0)
            replySerialized = pickle.dumps(reply)
            serverReply(replySerialized, UDPServerSocket, address)
    except KeyboardInterrupt:
        print(CLOSE_SOCKET)
        UDPServerSocket.close()
        break
