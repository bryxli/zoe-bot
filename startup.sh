sudo yum update -y
sudo yum groupinstall "Development Tools" -y
sudo yum install python38-pip -y
sudo python3 -m pip install --upgrade pip
cd /home/ssm-user
sudo git clone https://github.com/bryxli/zoe-bot
cd /home/ssm-user/zoe-bot/src
sudo python3 -m pip install -r requirements.txt