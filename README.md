# FTP-Implementataion-in-Python
FTP is implementated using socket programming. It enable to transfer any type of file. 
Commands implemented are:
1. LIST: To list all files and folder of server
2. PWD: To display name of current working directory server
3. RETR <file_name>: To download a file
4. STOR <file_name>: To upload a file
5. MKD <directory_name>: To make a new directory at server
6. DELE <file_name> : To delete a file from server
7. RMD <directory_name>: To delete a directory and its contents
8. RNFR <file_name>: To identify a file to be renamed
9. CDUP: To change to parent directory
10. CWD <directory_name>: To change to another directory
11. STORM <file_names>: To store multiple files (Separate names by comma)
12. COMPRESS <file_names>: To make a zip file
