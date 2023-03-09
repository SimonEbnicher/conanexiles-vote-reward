#!/usr/bin/python3

### IMPORT ###
import logging
import os
import sys
import time
import lib.libcfg as libcfg
import lib.libdb as libdb
import lib.librcon as librcon
import lib.libapi as libapi

# init
logging.basicConfig(level=logging.INFO, filename='log/vote-reward.log', encoding='utf-8', format='%(asctime)s %(levelname)s: %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
cfg  = libcfg.CFG('config.json')
cfg.read_config()
db   = libdb.DB(cfg.db_path)
api  = libapi.API(cfg.api_key)
rcon = librcon.RCON(cfg.rcon_addr, cfg.rcon_port, cfg.rcon_pwd)

# get timestamp now
timestamp_now = int(time.time())

# get votes from api of conanexiles.com and insert into database if new
# also insert any new nicknames from votes an insert into database
avotes = api.get_votes()
logging.info('got votes from API: {0}'.format(len(avotes)))
for avote in avotes:
    db.insert_vote(avote['steamid'], avote['ts_voted'])
    db.insert_api_name(avote['steamid'],  avote['name'])
    logging.debug('crunched api vote: steamid={0}, ts_voted={1}, name={2}'.format(avote['steamid'], avote['ts_voted'], avote['name']))

# decay votes older than db_vote_decay (older than UNIX Timestamp Seconds)
delta_seconds = cfg.db_vote_decay * 86400
db.set_votes_decayed(timestamp_now - delta_seconds)
logging.info('decay votes older than: {0} days'.format(cfg.db_vote_decay))

# get unclaimed votes from database
uvotes = db.get_votes_unclaimed()
logging.info('got unclaimed votes from DB: {0}'.format(len(uvotes)))

# get current online players from rcon
players = rcon.get_players_online()
logging.info('got online players from RCON: {0}'.format(len(players)))

# check each user for unclaimed votes, insert name into DB, give out item and set claimed in DB
for player in players:
    # insert any new charnames from votes into database
    db.insert_rcon_name(player['steamid'], player['charname'], player['playername'], player['playerid'])
    # check for unredeemed votes
    for uvote in uvotes:
        if int(uvote['steamid']) == int(player['steamid']):
            logging.info('found unredeemed vote for online player: {0}'.format(player['charname']))
            res = rcon.give_items_to_player(player['playername'], cfg.rcon_item_id, cfg.rcon_item_count)
            if res == True:
                db.set_vote_claimed(uvote['steamid'], uvote['ts_voted'], timestamp_now)
                logging.info('successfully redeemed vote for online player: {0}'.format(player['charname']))

# run complete
logging.info('--> run completed')
