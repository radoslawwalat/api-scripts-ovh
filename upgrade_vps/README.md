# CLI VPS upgrade/downgrade script

This script allows you to see all available upgrade models for your VPSes. Then you are automatically prompted to specify a vps to upgrade, followed by the plan for an upgrade and confirmation. 

# Example of use
## Step one
Download the script using: 
```
curl https://raw.githubusercontent.com/radoslawwalat/api-scripts-ovh/main/upgrade_vps/upgrade_vps.py -O
```
## Step two
Get API keys to allow the script make changes on your account. 

Use this link to generate required permissions:
https://api.ovh.com/createToken/index.cgi?GET=/vps*&GET=/order*&POST=/order/upgrade/vps*

## Step three
Edit 'xxx' at the begining of the script with your credentials:
```
client = ovh.Client(
    endpoint='ovh-eu',
    application_key='your_application_key',
    application_secret='your_application_secret',
    consumer_key='your_consumer_key',
)
```
## Step four
Make sure you have ovh package installed and run the script:
```
pip3 install ovh
```
```
python3 upgrade_vps.py
```

## Step five 
Follow the prompts on the terminal.
You can exit the script using: ctrl + c
