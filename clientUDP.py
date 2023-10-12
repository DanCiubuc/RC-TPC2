import socket
import random
import select

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

 # Create a UDP socket at client side

UDPClientSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

# Send to server using created UDP socket
UDPClientSocket.sendto(bytesToSend, serverAddressPort)

msgFromServer = UDPClientSocket.recvfrom(bufferSize)

msg = "Message from Server {}".format(msgFromServer[0])

print(msg)