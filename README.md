# Note: this is not a production build, current production build can be found in old branch

## Useful commands

 * `cdk bootstrap`   initialize assets before deploy
 * `cdk synth`       emits the synthesized CloudFormation template
 * `cdk deploy`      deploy this stack to your default AWS account/region
 * `aws ssm start-session --target i-xxxxxxxxx` remote session for shell access

Current: i-071d01299a803f279

aws ssm start-session --target i-071d01299a803f279
sudo yum update
sudo yum install git
sudo yum install screen -y
python3 -m pip install --upgrade pip
screen -S zoe-bot

cd ~
sudo git clone https://github.com/bryxli/zoe-bot
cd zoe-bot/src/

IMPORTANT: downgrade to Python 3.7.16 packages