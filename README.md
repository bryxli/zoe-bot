## Startup commands

 * `cdk bootstrap`   initialize assets before deploy
 * `cdk synth`       emits the synthesized CloudFormation template
 * `cdk deploy`      deploy this stack to your default AWS account/region
 * `aws ssm start-session --target i-xxxxxxxxx` remote session for shell access

## Start session

```
aws ssm start-session --target i-0a2e9ba8f6fa18ecc
```

## Install system dependencies

```
sudo yum update -y
sudo yum groupinstall "Development Tools" -y
sudo yum install openssl-devel libffi-devel bzip2-devel -y

cd opt/
sudo wget https://www.python.org/ftp/python/3.10.4/Python-3.10.4.tgz
sudo tar -xf Python-3.10.4.tgz
sudo rm Python-3.10.4.tgz

cd Python-3.10.4/
sudo ./configure --enable-optimizations
sudo make -j $(nproc)
sudo make altinstall
sudo yum install python38-pip -y
sudo python3 -m pip install --upgrade pip
```

## Install project dependencies

```
cd ~/
sudo git clone https://github.com/bryxli/zoe-bot
cd zoe-bot/src/
sudo python3 -m pip install -r requirements.txt
```

## Create config.json

```
sudo touch config.json
sudo vim config.json
```

Enter config.json, then `:wq`

## Run

```
python3 app.py
```

## Example config.json (put this file in [src/](src/))

```
{
    "prefix": "?",
    "token": "",
    "permissions": "2048",
    "application_id": "",
    "riot_key": ""
}
```
