#FOR UPLOADING IMAGES TO REMOTE LOCAL SMB SERVER
#pip install pysmb
import socket
from dotenv import load_dotenv
from smb.SMBConnection import SMBConnection
import os

# Samba server configuration
load_dotenv()
server_name = os.getenv('FS_NAME'),
server_user = os.getenv('FS_USER'),
server_password = os.getenv('PASSWORD'),
share_name = os.getenv('SHARE_NAME'),


# Local file to upload
#local_file_path = "path/to/your/file.jpg"

# Destination path on the Samba share
#remote_file_path = "path/on/remote/share/file.jpg"


def upload_screenshot(filePath, fileServerPath):
    # Establish a connection to the Samba server
    conn = SMBConnection(server_user, server_password, "client", server_name, use_ntlm_v2=True)
    conn.connect(socket.gethostbyname(server_name), 445)

    # Open the local file in binary mode and upload it to the Samba share
    with open(filePath, "rb") as local_file:
        conn.storeFile(share_name, fileServerPath, local_file)

    # Close the connection
    conn.close()