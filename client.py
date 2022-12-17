import socket
import os
from math import ceil
from getpass import getpass  # Library used for entering password
from time import sleep



def main():
    PORT = 12000 #COMMAND PORT: To send commands and acknowledgements
    HOST = '127.0.0.1'
    s = socket.socket()
    s.connect((HOST, PORT))

    PORT2 = 12001 #DATA PORT: To send file
    s2 = socket.socket()
    s2.connect((HOST,PORT2))

    loginAttempts = 0
    while loginAttempts < 3:
        message = s.recv(2048).decode()
        print(message)

        username = input("Enter your username: ")
        s.sendall(username.encode())

        password = getpass(prompt="Enter your password: ", stream=None)
        s.send(password.encode())

        answer = s.recv(2048).decode()

        if answer == 'correct':
            print("230 Login Successful")
            print("\t\tCOMMANDS")
            print("1. LIST: To list all files and folder of server")
            print("2. PWD: To display name of current working directory server")
            print("3. RETR <file_name>: To download a file")
            print("4. STOR <file_name>: To upload a file")
            print("5. MKD <directory_name>: To make a new directory at server")
            print("6. DELE <file_name> : To delete a file from server")
            print("7. RMD <directory_name>: To delete a directory and its contents")
            print("8. RNFR <file_name>: To identify a file to be renamed")
            print("9. CDUP: To change to parent directory")
            print("10. CWD <directory_name>: To change to another directory")
            print("11. STORM <file_names>: To store multiple files (Separate names by comma)")
            print("12. COMPRESS <file_names>: To make a zip file")
            print("\n6. quit - To Logout of the System")
            while True:
                string = input("\nftp> ")
                s.sendall(string.encode())

                if string == 'LIST':
                    y = s.recv(2048).decode()
                    print(y)
                    sleep(0.5)
                    x = s2.recv(2048).decode()
                    print(x)

                elif string == 'PWD':
                    x = s2.recv(2048).decode()
                    print(x)

                elif string[:5] == 'DELE ':
                    x = s.recv(2048).decode()
                    if x == "true":
                        print(f"File {string[5:]} deleted successfully")
                    else:
                        print(f"File {string[5:]} does not exist")
                
                elif string[:4] == 'RMD ':
                    x = s.recv(2048).decode()
                    if x == "true":
                        print(f"Directory {string[4:]} deleted successfully")
                    else:
                        print(f"Directory {string[4:]} does not exist")
                        

                elif string[:5] == 'RETR ':
                    response = s.recv(2048).decode()
                    print(response + ' bytes')
                    if (response[:4] == 'file'):
                        filename = string[5:]
                        filesize = int(response[27:])
                        packetAmmount = ceil(filesize / 2048)
                        if (os.path.isfile('server_file_' + filename)):
                            x = 1
                            while (os.path.isfile('server_file_' + str(x) + filename)):
                                x += 1
                            f = open('server_file' + str(x) + filename, 'wb')

                        else:
                            f = open("server_file_" + filename, 'wb')

                        for x in range(0, packetAmmount):
                            data = s2.recv(2048)
                            f.write(data)

                        f.close()
                        print("Download completed")
                    else:
                        print("File does not exist...")

                elif string[:6] == 'RETRM ':
                    file_list = string[6:].split(",")
                    print(file_list)
                    for i in range(len(file_list)):
                        response = s.recv(2048).decode()
                        if (response[:4] == 'file'):
                            print(response + ' bytes')
                            filename = file_list[i]
                            filesize = int(response[27:])
                            packetAmmount = ceil(filesize / 2048)
                            if (os.path.isfile('server_file_' + filename)):
                                x = 1
                                while (os.path.isfile('server_file_' + str(x) + filename)):
                                    x += 1
                                f = open('server_file' + str(x) + filename, 'wb')

                            else:
                                f = open("server_file_" + filename, 'wb')

                            for k in range(0, packetAmmount):
                                data = s.recv(2048)
                                print(data)
                                f.write(data)

                            f.close()
                            print(f"File {filename} Download completed")
                        else:
                            print("File does not exist")


                
                elif string[:5] == 'RNFR ':
                    x = s.recv(2048).decode()
                    if x == "true":
                        new_name = input("Enter new file name: ")
                        s.sendall(new_name.encode())
                        print(f"File {string[:5]} renamed to {new_name} sucessfully!!")
                    else:
                        print(f"File {string[:5]} doesn't exist on server")
                
                elif string == 'CDUP':
                    x1 = s.recv(2048).decode()
                    x2 = s.recv(2048).decode()
                    #print(x1,"\n", x2)
                    print(f"Directory change from {x1} to parent directory {x2}")
                
                elif string[:4] == 'CWD ':
                    cwd = s.recv(2048).decode()
                    x = s.recv(2048).decode()
                    if x == "true":
                        print(f"Directory changed to {string[4:]}")
                    else:
                        print(f"Directory {string[4:]}doesn't exist")
            



                elif string[:5] == 'STOR ':
                    filename = string[5:]
                    if os.path.isfile(filename):
                        filesize = int(os.path.getsize(filename))
                        s.sendall(('true' + str(filesize)).encode())
                        with open(filename, 'rb') as f:
                            packetAmmount = ceil(filesize / 2048)
                            for x in range(0, packetAmmount):
                                bytesToSend = f.read(2048)
                                s2.send(bytesToSend)
                        print("File sent!")
                    else:
                        s.sendall('false'.encode())
                        print("File does not exist")

                elif string[:6] == 'STORM ':
                    file_list = string[6:].split(",")

                    for x in file_list:
                        if os.path.isfile(x):
                            filename = x
                            filesize = int(os.path.getsize(filename))
                            s.sendall(('true' + str(filesize)).encode())
                            with open(filename, 'rb') as f:
                                packetAmmount = ceil(filesize / 2048)
                                for y in range(0, packetAmmount):
                                    bytesToSend = f.read(2048)
                                    s2.send(bytesToSend)
                            print(f"File {filename} sent")
                        else:
                            print(f"File {x} does not exist")



                elif string[:9] == 'COMPRESS ':
                    x = s.recv(2048).decode()
                    if x[:4] == "true":
                        print(f"Zip file created with name {x[4:]}")
                    else:
                        print(f"Zip file not created as File {x[5:]} missing")



                elif string[:4] == 'MKD ':
                    x = s.recv(2048).decode()
                    if x == "true":
                        print(f"Directory {string[4:]} created ")
                    else:
                        print(x)
                

                elif string == 'quit':
                    print("221 Goodbye")
                    s.close()
                    loginAttempts = 4
                    break

        elif answer == 'disconnect':
            break
        loginAttempts += 1
    print("You have been disconnected...")


main()
