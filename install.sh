#!/bin/bash

distro=$(lsb_release -si 2>/dev/null || cat /etc/os-release | grep -oP '(?<=ID=)\w+' 2>/dev/null || echo "Unknown")

case $distro in
    Debian)
        sudo apt update
        sudo apt -y upgrade
        sudo mkdir -p /opt/OptiSafe_Camera
        sudo mv * /opt/OptiSafe_Camera
        cd /opt/OptiSafe_Camera
        sudo cp optisafe.service /etc/systemd/system/optisafe.service
        if command -v python3 &>/dev/null; then
            sudo apt install python3-pip -y
            sudo pip install virtualenv
            sudo python3 -m venv .venv
            sudo source .venv/bin/activate
            sudo pip install -r requirements.txt
            sudo chmod +x exec.sh
        else
            echo "Python 3 is not installed on this system. Install python3 first"
            exit 1
        fi
        ;;
    *)
        echo "Unsupported or unknown distribution: $distro"
        exit 1
        ;;
esac