#FOR UPLOADING IMAGES TO REMOTE LOCAL SMB SERVER
from dotenv import load_dotenv
import subprocess
import os

load_dotenv()

def mkdirSamba(remote_url, folder_name, samba_username):
    # Construct the smbclient command
    command = f"smbclient {remote_url} --user {samba_username} -c 'mkdir {folder_name}'"
    try:
        print(command)
        subprocess.Popen(command, shell=True)
        print(f"Folder '{folder_name}' successfully created on Samba server at '{remote_samba_path}'.")
    except subprocess.CalledProcessError as e:
        print(f"Error: {e}")

def putSamba(remote_url, samba_username, local_file, dir_and_name):
    # Construct the smbclient command
    command = f"smbclient {remote_url} --user {samba_username} -c 'put {local_file} {dir_and_name}'"
    try:
        print(command)
        subprocess.Popen(command, shell=True)
        print(f"File '{dir_and_name}' successfully moved to '{dir_and_name}'.")
    except subprocess.CalledProcessError as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    # Replace these variables with your actual values for testing
    remote_samba_path = os.getenv('FS_SERVER')
    folder_name = "testa"
    username = os.getenv('FS_USER_PASSWORD')
    local_file_path = "/home/angelorecio/Documents/VSCODE/OptiSafe_Camera_System/testFile.txt"
    filename = f"testa/testFile.txt"

    mkdirSamba(remote_samba_path, folder_name, username)
    putSamba(remote_samba_path, username, local_file_path, filename)
