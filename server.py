import socket
import os
from math import ceil
import zipfile
import shutil
import sys

zip_count = 0

#Two ports


def main():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s2 = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    
    host = '127.0.0.1'  # host ip address
    
    port = 12000
    port2 = 12001
    
    username = "jay"
    password = "jay"
    
    s.bind((host, port))
    s2.bind((host,port2))
    

    s.listen()
    s2.listen()
    print(host)
    print("Waiting for a connection...")
    conn, addr = s.accept()
    conn2,addr2 = s2.accept()

    print(addr, "Has connected to the server.")
    print("Connection has been established!")

    for x in range(3, 0, -1):
        answer = "\n530 Please login with USER AND PASSWORD"
        conn.sendall(answer.encode())

        attemptedUsername = conn.recv(2048).decode()
        #print(attemptedUsername)

        attemptedPassword = conn.recv(2048).decode()
        #print(attemptedPassword)

        if attemptedUsername == username and attemptedPassword == password:
            conn.sendall("correct".encode())
            

            while True:
                recieveData = conn.recv(2048).decode()
                # msg = "150 Directory Listing"
                # conn.sendall(msg.encode())
                print(recieveData)
                #checkpoint
                if recieveData == 'LIST':
                    msg = "150 Directory Listing"
                    conn.sendall(msg.encode())
                    x = os.listdir() #list which contains all files and folders
                    y = 0
                    for file in x:
                        if os.path.isfile(file):
                            string = 'F: ' + str(file) #adding 'F' to files and making changes to same postion in list x
                            x[y] = string
                        else:
                            string = 'D: ' + str(file)
                            x[y] = string
                        y += 1
                    x.sort()
                    string = '\n'.join(x)
                    conn2.sendall(string.encode())


                elif recieveData[:3] == 'PWD':
                    string = str(os.getcwd())
                    conn2.sendall(string.encode())
                
                elif recieveData[:4] == 'MKD ':
                    cwd = os.getcwd()
                    new_folder = '/' + recieveData[4:]
                    new_folder_path = cwd + new_folder

                    try:
                        os.mkdir(new_folder_path)
                        msg = "true"
                        conn.sendall(msg.encode())
                    except OSError as error:
                        conn.sendall(error.encode())
                
                elif recieveData[:5] == 'DELE ':
                    filename = recieveData[5: ]
                    if os.path.isfile(filename):
                        os.remove(filename)
                        msg = "true"
                        conn.sendall(msg.encode())
                    else:
                        msg = "false"
                        conn.sendall(msg.encode())
                
                elif recieveData[:4] == 'RMD ':
                    dir_name = recieveData[4:]
                    if os.path.isdir(dir_name):
                        shutil.rmtree(dir_name)
                        msg = "true"
                        conn.sendall(msg.encode())
                    else:
                        msg = "false"
                        conn.sendall(msg.encode())
                        
                        
            

                elif recieveData[:5] == 'RETR ':
                    filename = recieveData[5:]
                    if os.path.isfile(filename):
                        conn.sendall(("file exists with a size of " + str(os.path.getsize(filename))).encode())
                        filesize = int(os.path.getsize(filename))
                        with open(filename, 'rb') as f:
                            packetAmmount = ceil(filesize / 2048)
                            for x in range(0, packetAmmount):
                                bytesToSend = f.read(2048)
                                conn2.send(bytesToSend)

                    else:
                        conn.send("Error while reading the file!".encode())


                elif recieveData[:6] == 'RETRM ':
                    recieved_list = recieveData[6:].split(",")
                    #print(recieved_list)
                    for x in recieved_list:
                        if os.path.isfile(x):
                            filename = x
                            conn.sendall(("file exists with a size of " + str(os.path.getsize(filename))).encode())
                            filesize = int(os.path.getsize(filename))
                            # with open(filename, 'rb') as f:
                            #     packetAmmount = ceil(filesize / 2048)
                            #     for y in range(0, packetAmmount):
                            #         bytesToSend = f.read(2048)
                            #         conn.send(bytesToSend)
                            # f.close()
                            f = open(filename,'rb')
                            packetAmmount = ceil(filesize/2048)
                            for y in range(0,packetAmmount):
                                bytesToSend = f.read(2048)
                                conn.send(bytesToSend)
                            f.close()
                                
                        else:
                            conn.send("Error while reading the file!".encode())


                elif recieveData[:5] == 'RNFR ':
                    filename = recieveData[5: ]
                    if os.path.isfile(filename):
                        msg = "true"
                        conn.sendall(msg.encode())
                        new_name = conn.recv(2048).decode()
                        os.rename(filename,new_name)
                    else:
                        msg = "false"
                        conn.sendall(msg.encode())
                
                elif recieveData == 'CDUP':
                    cwd = os.getcwd()
                    conn.sendall(cwd.encode())
                    os.chdir("..")
                    new_cwd = os.getcwd()
                    conn.sendall(new_cwd.encode())
                
                elif recieveData[:4] == 'CWD ':
                    dir_name = recieveData[4:]

                    cwd = os.getcwd()
                    conn.sendall(cwd.encode())

                    if os.path.isdir(dir_name):
                        new_path = cwd + '/' + dir_name
                        os.chdir(new_path)
                        msg = "true"
                        conn.sendall(msg.encode())
                    else:
                        msg = "false"
                        conn.sendall(msg.encode())



                    # try:
                    #     os.chdir(dir_path)
                    #     msg = "true"
                    #     conn.sendall(msg.encode())
                    # except:
                    #     print(sys.exc_info)
                    #     error = sys.exc_info()[0]
                    #     msg = "Some wrong with specified directory. Exception - " + error
                    #     conn.sendall(msg.encode())
                    #     msg = "Path restored to the original one"
                    #     conn.sendall(msg.encode())
                    #     os.chdir(cwd)
                        

                        




                elif recieveData[:5] == 'STOR ':
                    response = conn.recv(2048).decode()
                    if (response[:4] == 'true'):
                        filesize = int(response[4:])
                        packetAmmount = ceil(filesize / 2048)
                        filename = recieveData[5:]
                        if (os.path.isfile('client_file_' + filename)):
                            x = 1
                            while (os.path.isfile('client_file_' + str(x) + filename)):
                                x += 1
                            f = open('client_file_' + str(x) + filename, 'wb')

                        else:
                            f = open("client_file_" + filename, 'wb')

                        for x in range(0, packetAmmount):
                            data = conn2.recv(2048)
                            f.write(data)

                        f.close()

                elif recieveData[:6] == 'STORM ':
                    recieved_list = recieveData[6:].split(",")
                    for i in range(len(recieved_list)):
                        response = conn.recv(2048).decode()
                        if (response[:4] == 'true'):
                            filesize = int(response[4:])
                            packetAmmount = ceil(filesize / 2048)
                            filename = recieved_list[i]
                            if (os.path.isfile('client_file_' + filename)):
                                x = 1
                                while (os.path.isfile('client_file_' + str(x) + filename)):
                                    x += 1
                                f = open('client_file_' + str(x) + filename, 'wb')

                            else:
                                f = open("client_file_" + filename, 'wb')

                            for x in range(0, packetAmmount):
                                data = conn2.recv(2048)
                                f.write(data)

                            f.close()

                

                elif recieveData[:9] == 'COMPRESS ':
                    fileToCompress_list = recieveData[9:].split(",")
                    
                    compress_file = fileToCompress_list[0] + ".zip"
                    if(os.path.isfile(compress_file)):
                        x = 1
                        while(os.path.isfile(compress_file + str(x))):
                            x+=1
                        compress_file = fileToCompress_list[0] + str(x) + ".zip"

                    fileToZip = zipfile.ZipFile(compress_file, mode='w', compression=zipfile.ZIP_DEFLATED)
                    flag = 0
                    for file in fileToCompress_list:
                        if os.path.isfile(file):
                            fileToZip.write(file)
                        else:
                            flag = 1
                            msg = "false" + str(file)
                            conn.sendall(msg.encode())
                            fileToZip.close()
                            os.remove(compress_file)
                            break

                    fileToZip.close()

                    if(flag == 0):
                        msg = "true" + str(compress_file)
                        conn.sendall(msg.encode())
                    

                elif recieveData == 'quit':
                    x = -1
                    break
            conn.sendall("correct".encode())
            conn.close()
            print("Disconnected")
            break
        else:
            conn.sendall("incorrect".encode())



main()

