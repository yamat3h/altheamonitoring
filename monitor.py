import json
import time
from typing import Dict, List, Any
import requests
import configparser

rpc_url = 'http://localhost:26657/'


def get_json(endpoint: str) -> Dict:
    time.sleep(0.01)
    get_ret = requests.get(endpoint, timeout=10)
    return json.loads(get_ret.content.decode('UTF-8'))['result']


def check_skip(block: str, address: str) -> str:
    data = get_json(rpc_url + f"validators?height={block}&per_page=100")
    validators = data['validators']
    check = 0
    for validator in validators:
        if validator['address'] == address:
            check = 1
            break
    if check == 0:
        return 'skip'
    else:
        return "ok"


def read_last_info():
    config = configparser.ConfigParser()
    config.read('last_info.ini')
    return int(config['info']['last_check_block']), int(config['info']['skipped_block'])


def save_last_info(last_check_block, skipped_block):
    config = configparser.ConfigParser()
    config['info'] = {'last_check_block': last_check_block,
                      'skipped_block': skipped_block}

    with open('last_info.ini', 'w') as configfile:
        config.write(configfile)


def main():
    try:
        last_check_block, skipped_block = read_last_info()
        info = {}
        data = get_json(rpc_url + 'status')
        last_commit_block = get_json(rpc_url + 'block')['block']['last_commit']['height']

        info['id'] = data['node_info']['id']
        info['network'] = data['node_info']['network']
        info['moniker'] = data['node_info']['moniker']
        info['address'] = data['validator_info']['address']
        info['voting_power'] = data['validator_info']['voting_power']
        info['latest_block_height'] = data['sync_info']['latest_block_height']
        info['last_commit_block'] = last_commit_block
        info['catching_up'] = data['sync_info']['catching_up']

        if last_check_block == 0:
            last_check_block = int(info['latest_block_height'])

        while last_check_block <= int(info['latest_block_height']):
            if check_skip(last_commit_block, info['address']) == 'skip':
                skipped_block += 1
            last_check_block += 1
        save_last_info(last_check_block, skipped_block)
        info['skipped_block'] = skipped_block

        info_str = f'''id="{info['id']}",network="{info['network']}",''' \
                   f'''moniker="{info['moniker']}",''' \
                   f'''address="{info['address']}",''' \
                   f'''voting_power={info['voting_power']},''' \
                   f'''latest_block_height={info['latest_block_height']},''' \
                   f'''last_commit_block={info['last_commit_block']},''' \
                   f'''catching_up="{info['catching_up']}",''' \
                   f'''skipped_block={info['skipped_block']}'''

        print(f'althea,name=althea_monitor status=1,{info_str}', '{:1.0f}'.format(time.time() * 1000000000))

    except:
        print(f'althea,name=althea_monitor status=0', '{:1.0f}'.format(time.time() * 1000000000))


main()
