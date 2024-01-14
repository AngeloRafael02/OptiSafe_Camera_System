# OptiSafe Camera Service
This is daemon Program run by SystemD that uses a Camera to monitor 
and detect certain Personal Protective Equipment in the manufacturing Industry

## Packages needed 
pip install psycopg2-binary
pip install python-dotenv
pip install datetime
pip install opencv-python 
pip install ultralytics --no-cache-dir
pip install subprocess

### DEV TO DO LIST:
- Possible Switch from Postgres to mongoDB for Log Database 
- Create Shell Script to deploy OptiSafe Camera Service
    - assign ip address via shell argument
    - move .service file to /etc/systemd/system
    - check if ntp is setup to main local server
    - move whole python program folder to /opt