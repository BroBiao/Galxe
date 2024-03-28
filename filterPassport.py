import requests
import json
import os
import sys
from teleBot import sendMsg
from loguru import logger
import galxeAPI as galxe


logger.remove()
logger.add(sys.stderr, format='<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | '
                              '<level>{level: ^7}</level> | '
                              '<level>{message}</level>')
logger.info('Starting.......')


debug_mode = True
if debug_mode == True:
    proxies = {
    'https': 'http://127.0.0.1:7890/',
    'http': 'http://127.0.0.1:7890/'
    }
else:
    proxies = None


import csv

all_spaces = []
with open('all_spaces.csv', 'r') as file:
    reader = csv.reader(file)
    for row in reader:
        all_spaces += row

def check_space(i):
    try:
        result = galxe.get_campaign_collections(all_spaces[i], proxies)
        campaign_collection_id_list = [each['id'] for each in result['data']['space']['campaigns']['list']]
        for campaign_id in campaign_collection_id_list:
            result = galxe.get_campaign_details(campaign_id, proxies)
            if result['data']['campaign']['childrenCampaigns'] == None:
                children_campaign_list = [result['data']['campaign']]
            else:
                children_campaign_list = result['data']['campaign']['childrenCampaigns']
            for campaign in children_campaign_list:
                credentialGroups = campaign['credentialGroups']
                for credentialGroup in credentialGroups:
                    credentials = credentialGroup['credentials']
                    for credential in credentials:
                        cond1 = 'assport' in credential['name']
                        # cond2 = 'passport' in credential['name']
                        # cond3 = 'Gitcoin' in credential['name']
                        if cond1:
                            # print(credential['name'])
                            print(all_spaces[i])
                            with open('passport.txt', 'a') as f:
                                f.write(all_spaces[i]+'\n')
                                return
                        else:
                            pass
    except Exception as e:
        print(e)

for i in range(len(all_spaces)):
    print(f'{i}/{len(all_spaces)}')
    check_space(i)

# with open('passport.txt', 'r') as file:
#     passport_spaces = file.read()

# print(list(set(passport_spaces.split('\n'))))