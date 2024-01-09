# OptiSafe Camera Service
This

## Packages needed 
pip install psycopg2-binary
pip install python-dotenv
pip install datetime
pip install opencv-python 
pip install ultralytics --no-cache-dir
pip install pysmb

### DEV TO DO LIST:
- Create Shell Script to deploy OptiSafe Camera Service
    - assign ip address via shell argument
    - move .service file to /etc/systemd/system
    - check if ntp is setup to main local server
    - move whole python program folder to /opt