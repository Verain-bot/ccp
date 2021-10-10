import hashlib
import os
from pydrive.drive import GoogleDrive
from pydrive.auth import GoogleAuth
import time
import sys

if(len(sys.argv)<2):
    raise Exception("File name not specified!")

gauth = GoogleAuth()
gauth.LocalWebserverAuth()       
drive = GoogleDrive(gauth)
foldername = sys.argv[1]

def hash_file(file_path):
    h = hashlib.md5()

    with open(file_path, 'rb') as file:
        while True:
            chunk = file.read(h.block_size)
            if not chunk:
                break
            h.update(chunk)
    return h.hexdigest()



while True:
    logs = []
    with open('./log.txt','r') as logFile:
        for filename in os.listdir(foldername):
            line = logFile.readline().split('\t')
            newHash = hash_file(foldername + r'\\' + filename)
            oldHash = None if len(line) == 1 else line[1]

            if not newHash == oldHash:
                tta = [filename, newHash, time.asctime( time.localtime(time.time()) )]
                logs.append('\t'.join(tta) + '\n')

                f = drive.CreateFile({'title': filename})
                f.SetContentFile(os.path.join(foldername, filename))
                f.Upload()

                print(f"Uploaded {filename}.")
                f = None


            else:
                logs.append('\t'.join(line))

    with open('./log.txt','w') as logFile:
        for i in logs:
            logFile.write(i)
    

    time.sleep(10)
