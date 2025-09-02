import ftplib
import threading
import os
import multiprocessing
import psutil
from time import time

SERVER_IP="SERVER_IP" # change to your server IP
PORT=2121
REMOTE_FILE="kali.iso" # change to any file
LOCAL_FILE="kali.iso"

cpu_count=multiprocessing.cpu_count()
free_ram=psutil.virtual_memory().available

THREADS=max(1,min(8,cpu_count//2))
if free_ram>4*1024**3:
    BLOCK_SIZE=1024*1024
elif free_ram>2*1024**3:
    BLOCK_SIZE=512*1024
else:
    BLOCK_SIZE=256*1024

def download_chunk(start,end,thread_num):
    ftp=ftplib.FTP()
    ftp.connect(SERVER_IP,PORT,timeout=60)
    ftp.login()
    ftp.voidcmd("TYPE I")
    with open(LOCAL_FILE,"r+b") as f:
        f.seek(start)
        def write_data(data):
            f.write(data)
        ftp.retrbinary(f"RETR {REMOTE_FILE}",write_data,blocksize=BLOCK_SIZE,rest=start)
    ftp.quit()

def adaptive_download():
    ftp=ftplib.FTP()
    ftp.connect(SERVER_IP,PORT,timeout=60)
    ftp.login()
    total_size=ftp.size(REMOTE_FILE)
    ftp.quit()

    with open(LOCAL_FILE,"wb") as f:
        f.truncate(total_size)

    chunk_size=total_size//THREADS
    threads=[]
    start_time=time()
    for i in range(THREADS):
        start=i*chunk_size
        end=start+chunk_size-1
        if i==THREADS-1:
            end=total_size-1
        t=threading.Thread(target=download_chunk,args=(start,end,i+1))
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

    elapsed=time()-start_time
    speed=(total_size/1024/1024)/elapsed
    print(f"Download complete: {total_size/1024/1024:.2f} MB in {elapsed:.2f}s ({speed:.2f} MB/s)")

if __name__=="__main__":
    adaptive_download()
