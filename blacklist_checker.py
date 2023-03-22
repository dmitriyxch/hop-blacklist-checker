import requests
import re
from loguru import logger

git_list = ["https://raw.githubusercontent.com/hop-protocol/hop-airdrop/master/src/data/blacklists/blacklist.ts",
"https://raw.githubusercontent.com/hop-protocol/hop-airdrop/master/src/data/blacklists/contractBlacklist.ts",
"https://raw.githubusercontent.com/hop-protocol/hop-airdrop/master/src/data/blacklists/connectionBlacklist.ts",
"https://raw.githubusercontent.com/hop-protocol/hop-airdrop/master/src/data/blacklists/depositAddressBlacklist.ts",
"https://raw.githubusercontent.com/hop-protocol/hop-airdrop/master/src/data/blacklists/exchangeBlacklist.ts",
"https://raw.githubusercontent.com/hop-protocol/hop-airdrop/master/src/data/blacklists/fundraisingBlacklist.ts",
"https://raw.githubusercontent.com/hop-protocol/hop-airdrop/master/src/data/blacklists/gitcoinGrantsBlacklist.ts",
"https://raw.githubusercontent.com/hop-protocol/hop-airdrop/master/src/data/blacklists/givethBlacklist.ts",
"https://raw.githubusercontent.com/hop-protocol/hop-airdrop/master/src/data/blacklists/nftPowerUserBlacklist.ts"]


def checker_address():
    address_lists = []
    for git in git_list:
        req = requests.get(git)
        if req.status_code == 200:
            address_list = re.findall(r'\b0x[0-9a-z]{40}\b', req.text)
            [address_lists.append(address) for address in address_list]
        else:
            logger.info(f'Invalid {git}')
    with open('blacklist.txt', 'r+') as file:
        for address in file:
            address = address.split('\n')[0]
            if len(address) and address in address_lists:
                address_lists.remove(address)
        file.writelines(s + "\n" for s in address_lists)

    coincidence_addr = []
    lines = open("blacklist.txt", "r").read().split('\n')
    with open("mywallets.txt", "r") as file:
        for address in file:
            address = address.split('\n')[0]
            if address in lines:
                coincidence_addr.append(address)
        print(*coincidence_addr, sep="\n")
        [logger.info(addr) for addr in coincidence_addr]
        with open('coincidence_blacklist.txt', 'r+') as coincidence_file:
            for address in coincidence_file:
                address = address.split('\n')[0]
                if len(address) and (address in coincidence_addr or address.lower() in coincidence_addr):
                    coincidence_addr.remove(address)
            coincidence_file.writelines(s + "\n" for s in coincidence_addr)


if __name__ == '__main__':
    checker_address()