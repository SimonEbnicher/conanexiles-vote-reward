#!/usr/bin/python3
import os.path
import sys
import logging
from datetime import datetime
import lib.libcfg as libcfg
import lib.libdb as libdb
import lib.libapi as libapi

logging.basicConfig(level=logging.INFO, filename='log/setup-database.log', encoding='utf-8', format='%(asctime)s %(levelname)s: %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
cfg = libcfg.CFG('config.json')
cfg.read_config()

db = None
if os.path.isfile(cfg.db_path):
    print('Database already existing. Abort.')
    logging.critical('Database already existing. Abort.')
    sys.exit(1)
else:
    db = libdb.DB(cfg.db_path)
    db.write_init_database()
    print('Empty DB written')
    logging.info('Empty RB written')

# fill with votes and names from api
api = libapi.API(cfg.api_key)
votes = api.get_votes()
logging.info('got votes from API: {0}'.format(len(votes)))
for vote in votes:
    db.insert_vote(vote['steamid'], vote['ts_voted'])
    db.insert_api_name(vote['steamid'], vote['name'])
    logging.info('vote inserted: steamid={0}, ts_voted={1}, name={2}'.format(vote['steamid'], vote['ts_voted'], vote['name']))

# decay vote older than given date
datestr = input('Decay votes older than [YYYY-MM-DD] = ')
date = datetime.timestamp(datetime.strptime(datestr, '%Y-%m-%d'))
print('ts_decay = '+str(date))
logging.info('decayed votes older than: {0}'.format(date))
db.set_votes_decayed(date)

# run complete
logging.info('--> run completed')
