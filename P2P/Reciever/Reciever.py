import os
import websockets
from socket import *

################################################################################# 

PORT = 8000
hostName = gethostname()
timeout_connection = 10
request = 'downloading'
response = 'uploading'
storage = 'storage/'
chunkSize = 1024

################################################################################# Send & Recieve

def upload(file_name):
    
    sender = socket(AF_INET, SOCK_DGRAM)
    sender.bind((hostName, PORT))
    
    while True:
        
        request, address = sender.recvfrom(chunkSize)
        requested_file = request.decode('ascii').split()[1]
        
        if requested_file == file_name.split('/')[-1]:
            break
        
    print("Request Sent")
    print(response)
    
    with open(file_name, 'rb') as file:
        chunk_offset = 0
        data = file.read(chunkSize)
        
        while data:
            sender.sendto(data, address)
            data = file.read(chunkSize)
            print('uploaded by : ', hostName , f'file offset : {chunk_offset}')
            chunk_offset += 1
    sender.close()

#-------------------------------------------------------------------------------

def download(file_name):
    
    body = request + "\t" + file_name
    receiver = socket(AF_INET, SOCK_DGRAM)
    receiver.sendto(str.encode(body), (hostName, PORT))
    
    print(body)

    with open(storage + file_name, 'wb') as file:
        data, _ = receiver.recvfrom(chunkSize)
        chunk_offset = 0
        
        try:
            while data:
                receiver.settimeout(timeout_connection)
                file.write(data)
                data, _ = receiver.recvfrom(chunkSize)
                print('downloaded by : ', hostName , f'file offset : {chunk_offset}')
                chunk_offset += 1
        except:
            pass
    receiver.close()

#################################################################################

def run():
    command = input()
    command = command.split()
    if command[0] == "torrent" and command[1] == "-setMode" and (command[2] == "upload" or command[2] == "download"):
        if command[2] == "upload":
            upload(command[3])
        elif command[2] == "download":
            second_command = input().split()
            if second_command[0] == "torrent" and second_command[1] == "-search":
                download(second_command[2])
            else:
                print("Invalid Command")
                return
        else:
            print("Invalid Command")
            return
        print("file shared successfully")

    else:
        print("Invalid Command")
        return


if __name__ == '__main__':
    run()

#################################################################################