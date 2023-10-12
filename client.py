import socket
import random
import select
import pickle
import sys

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

#---------------------------------------- VARS ----------------------------------------------#

host_of_server = sys.argv[1]
portSP = int(sys.argv[2])
fileName = sys.argv[3]
chunkSize = int(sys.argv[4])

endpoint   = (host_of_server, int(portSP))
bufferSize          = 1024

#---------------------------------------- CODE ----------------------------------------------#

offset = 0
# TODO: open local file for writing 

# Create a UDP socket at client side
UDPSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

while(True):
    request = (fileName, offset, chunkSize) 
    req = pickle.dumps(request)
    UDPSocket.sendto(req, endpoint)
    
    # gets all of the data from the udp socket
    # data = []
    # while True:
        # packet, address = UDPSocket.recvfrom(4064)
        # print(packet)
        # if not packet: break
        # data.append(packet)
    # res = pickle.loads(b"".join(data))
    
    # se colocar com bufferSize só, ele dá erro de 'socket pickle data was truncated'. Mais TPC para ti :). Aqui em cima está uma solução, mas fica presa, se calhar porque temos que fazer algo semelhante do lado do server...
    server_res, address = UDPSocket.recvfrom(bufferSize*2)
        
    res = pickle.loads(server_res)
    
    # structure of a server reply datagram - (status, num_bytes_trans, bytes_trans i.e. actual bytes of the file)
    
    status = res[0]
    num_bytes_trans = res[1]
    bytes_trans = res[2]
    
    print(f'status={status}, number of bytes to transfer={num_bytes_trans}, bytes={bytes_trans}')
    