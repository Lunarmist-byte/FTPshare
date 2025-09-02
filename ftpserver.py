import os
import psutil
from pyftpdlib.servers import FTPServer
from pyftpdlib.handlers import FTPHandler, ThrottledDTPHandler
from pyftpdlib.authorizers import DummyAuthorizer
from io import BytesIO

FTP_FOLDER=os.path.abspath("./ftp_root")
ISO_FILENAME="kali.iso" # change to any file
PORT=2121
MAX_CLIENTS=20
MAX_CLIENTS_PER_IP=10

free_ram=psutil.virtual_memory().available
if free_ram>4*1024**3:
    BLOCK_SIZE=1024*1024
elif free_ram>2*1024**3:
    BLOCK_SIZE=512*1024
else:
    BLOCK_SIZE=256*1024

os.makedirs(FTP_FOLDER,exist_ok=True)
iso_path=os.path.join(FTP_FOLDER,ISO_FILENAME)
if not os.path.isfile(iso_path):
    raise FileNotFoundError(f"Put {ISO_FILENAME} inside {FTP_FOLDER} first!")

iso_size=os.path.getsize(iso_path)
load_in_ram=free_ram>iso_size+200*1024**2
if load_in_ram:
    with open(iso_path,"rb") as f:
        ISO_DATA=f.read()
else:
    ISO_DATA=None

authorizer=DummyAuthorizer()
authorizer.add_anonymous(FTP_FOLDER,perm="elr")

class AdaptiveFTPHandler(FTPHandler):
    def ftp_RETR(self,file):
        if ISO_DATA and file==ISO_FILENAME:
            stream=BytesIO(ISO_DATA)
            self.push_dtp_data(stream,isproducer=True,cmd="RETR "+file)
        else:
            super().ftp_RETR(file)

dtp_handler=ThrottledDTPHandler
dtp_handler.read_limit=0
dtp_handler.write_limit=0
dtp_handler.blocksize=BLOCK_SIZE

handler=AdaptiveFTPHandler
handler.authorizer=authorizer
handler.dtp_handler=dtp_handler
handler.banner="Adaptive RAM FTP Server"
handler.max_cons=MAX_CLIENTS
handler.max_cons_per_ip=MAX_CLIENTS_PER_IP

server_address=("0.0.0.0",PORT)
server=FTPServer(server_address,handler)
server.serve_forever()
