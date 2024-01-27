#FOR UPLOADING IMAGES TO REMOTE LOCAL SMB SERVER
from dotenv import load_dotenv
import subprocess
import os

load_dotenv()

def mkdirSamba(folder_name:str):
    """Create a Directory on the OptiSafe File Server, folder name may also be an address"""
    # Construct the smbclient command
    command = f"smbclient {os.getenv('FS_SERVER')} --user {os.getenv('FS_USER_PASSWORD')} -c 'mkdir {folder_name}'"
    try:
        process = subprocess.Popen(command, shell=True)
        process.wait()
        print(f"Folder '{folder_name}' successfully created.")
    except subprocess.CalledProcessError as e:
        print(f"Error: {e}")

def putSamba(local_file:str, dir_and_name:str):
    """Uploads a File from the local Machine to the OptiSafe File Server"""
    # Construct the smbclient command
    command = f"smbclient {os.getenv('FS_SERVER')} --user {os.getenv('FS_USER_PASSWORD')} -c 'put {local_file} {dir_and_name}'"
    try:
        process = subprocess.Popen(command, shell=True)
        process.wait()
        print(f"File '{dir_and_name}' successfully moved to '{dir_and_name}'.")
    except subprocess.CalledProcessError as e:
        print(f"Error: {e}")
