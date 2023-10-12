import socket
import random
import pickle


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
        sock.sendto(msg, address)
    return

# server is invoked with:
#   python server.py portSP

# create socket ss and bind it to portSP
# while TRUE:
#   receive datagram with request and deserialize it using pickle.
#
#   open file for reading, if open fails reply
#       with a datagram with status 1; the other fields must be filled

#   verify if the offset is valid using os.path.filesize(…) method
#   if open fails reply with a datagram with status 2

#   if both previous tests succeed use seek to position the file pointer
#   in the required position and try to read S bytes from the file
#   reply with a tuple (0, no_of_bytes_read, file_chunk)

#   serialize the reply using pickle and call serverReply

# OPTINAL TODO: Study Performance

#---------------------------------------- CODE ----------------------------------------------#

localIP     = "127.0.0.1"
localPort   = 20001
bufferSize  = 1024

msgFromServer       = "Hello UDP Client"
bytesToSend         = str.encode(msgFromServer)

 # Create a datagram socket
UDPServerSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

 # Bind to address and ip
UDPServerSocket.bind((localIP, localPort))

print("UDP server up and listening")

 # Listen for incoming datagrams
while(True):

    bytesAddressPair = UDPServerSocket.recvfrom(bufferSize)

    message = bytesAddressPair[0]

    address = bytesAddressPair[1]

    clientMsg = "Message from Client:{}".format(message)
    clientIP  = "Client IP Address:{}".format(address)
    
    print(clientMsg)
    print(clientIP)

   

    # Sending a reply to client

    UDPServerSocket.sendto(bytesToSend, address)