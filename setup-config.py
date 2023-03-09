#!/usr/bin/python3
import os.path
import sys
import lib.libcfg as libcfg
import lib.librcon as librcon
import lib.libapi as libapi

cfg = libcfg.CFG('config.json')

if os.path.isfile('config.json'):
    print('config file exists, showing content')
    cfg.read_config()
    print('config.json:')
    print('  database path      : {}'.format(cfg.db_path))
    print('  vote decay in days : {}'.format(cfg.db_vote_decay))
    print('  rcon address       : {}'.format(cfg.rcon_addr))
    print('  rcon port          : {}'.format(cfg.rcon_port))
    print('  rcon password      : {}'.format(cfg.rcon_pwd))
    print('  reward item id     : {}'.format(cfg.rcon_item_id))
    print('  reward item count  : {}'.format(cfg.rcon_item_count))
    print('  api key            : {}'.format(cfg.api_key))
    sys.exit(1)

print('''
This tiny program will help you setting up the configuration file.
After you have given some parameters, we will test the RCON connection by
sending a broadcast message ingame.
Then we will display some serverdata from conan-exiles.com to check the API.
''')

# get all data needed
cfg.db_path         = 'database.db'
cfg.db_vote_decay   = int(input('Vote decay (days) = '))
cfg.rcon_addr       = str(input('RCON address      = '))
cfg.rcon_port       = int(input('RCON port         = '))
cfg.rcon_pwd        = str(input('RCON password     = '))
cfg.rcon_item_id    = int(input('RCON item ID      = '))
cfg.rcon_item_count = int(input('RCON item count   = '))
cfg.api_key         = str(input('API key           = '))

# test RCON
rcon = librcon.RCON(cfg.rcon_addr, cfg.rcon_port, cfg.rcon_pwd)
rcon.broadcast('This is a testmessage from the new vote reward system. You can close this message. Thanks')

# test API
api = libapi.API(cfg.api_key)
adata = api.get_server_data()
print('Server data on conan-exiles.com')
print(str(adata))

# ask if everything worked
response = None
while response == None:
    response = input('Worked everything as intended? [y/n]: ')
    if response == 'y':
        cfg.write_config()
        print('All done. Writing config.json.')
    elif response == 'n':
        print('Something went wrong? Not writing config.json.')
    else:
        response = None

