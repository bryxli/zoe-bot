# Note: this is not a production build, current production build can be found in old branch

## Useful commands

 * `cdk bootstrap`   initialize assets before deploy
 * `cdk synth`       emits the synthesized CloudFormation template
 * `cdk deploy`      deploy this stack to your default AWS account/region
 * `aws ssm start-session --target i-xxxxxxxxx` remote session for shell access

### Start session

 * `aws ssm start-session --target i-0a101426d1196d08d`

### Install system dependencies

 * `sudo yum update -y`
 * `sudo yum install -y gcc openssl-devel bzip2-devel libffi-devel git`
 * `cd /opt`
 * `sudo wget https://www.python.org/ftp/python/3.7.4/Python-3.7.4.tgz`
 * `sudo tar xzf Python-3.7.4.tgz`
 * `cd Python-3.7.4`
 * `sudo ./configure -enable-optimizations`
 * `sudo make altinstall`
 * `sudo rm ../Python-3.7.4.tgz`
 * `pip3.7 install --upgrade --user --force pip`

### Install project dependencies

 * `cd ~/zoe-bot/src/`
 * `pip3.7 install -r requirements.txt`
 * `sudo git clone https://github.com/bryxli/zoe-bot`

need to install >=Python3.8