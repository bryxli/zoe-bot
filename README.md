# Running the bot

## Startup commands

 * `cdk bootstrap`   initialize assets before deploy
 * `cdk synth`       emits the synthesized CloudFormation template
 * `cdk deploy`      deploy this stack to your default AWS account/region
 * `aws ssm start-session --target i-xxxxxxxxx` remote session for shell access

## Start session

```
aws ssm start-session --target i-089afc155a2e07d22
```

## Install system dependencies

```
sudo yum update -y
sudo yum groupinstall "Development Tools" -y
sudo yum install openssl-devel libffi-devel bzip2-devel python38-pip -y
sudo python3 -m pip install --upgrade pip
```

## Install project dependencies

```
cd /home/ssm-user
sudo git clone https://github.com/bryxli/zoe-bot
cd /home/ssm-user/zoe-bot/src
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

# Extras

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

## Example [template.json](src/template.json)

Template to give Zoe custom responses! Responses are picked randomly based on game outcome.
```
{
    "win": ["you","can","have","an","arbitrary"],
    "lose": ["amount","of"],
    "response": ["string","values","in","each","list","of","bot","responses"]
}
```

## Python-3.10.4

I have included the commands to install python 3.10. I have no idea if it will work as intended.
```
sudo wget https://www.python.org/ftp/python/3.10.4/Python-3.10.4.tgz
sudo tar -xf Python-3.10.4.tgz
sudo rm Python-3.10.4.tgz
cd Python-3.10.4/
sudo ./configure --enable-optimizations
sudo make -j $(nproc)
sudo make altinstall
```
