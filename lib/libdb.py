#!/usr/bin/python3

import sqlite3

class DB:
    def __init__(self, path):
        self.path = path
        self.conn = sqlite3.connect(path)

    def __del__(self):
        self.conn.close()

    def insert_vote(self, steamid, ts_voted):
        res = self.conn.execute('SELECT steamid FROM votes WHERE steamid = {steamid} AND ts_voted = {ts_voted}'.format(steamid=steamid, ts_voted=ts_voted))
        rows = res.fetchall()
        if len(rows) == 0:
            self.conn.execute('INSERT INTO votes (steamid, ts_voted) VALUES ({steamid}, {ts_voted})'.format(steamid=steamid, ts_voted=ts_voted))
        self.conn.commit()

    def get_votes_unclaimed(self):
        res = self.conn.execute('SELECT steamid, ts_voted FROM votes WHERE ts_redeemed IS NULL')
        rows = res.fetchall()
        votes = []
        for row in rows:
            votes.append( {'steamid':row[0], 'ts_voted':row[1]} )
        return votes

    def set_vote_claimed(self, steamid, ts_voted, ts_now):
        self.conn.execute("UPDATE votes SET ts_redeemed = {ts_redeemed} WHERE steamid = {steamid} AND ts_voted = {ts_voted}".format(ts_redeemed=ts_now, steamid=steamid, ts_voted=ts_voted))
        self.conn.commit()

    # mark all votes as claimed older than timestamp ts_older, useful for first setup or periodic cleanup
    def set_votes_decayed(self, ts_older):
        self.conn.execute("UPDATE votes SET ts_redeemed = 0 WHERE ts_redeemed IS NULL AND ts_voted < {ts_older}".format(ts_older=ts_older))
        self.conn.commit()

    # insert names from API (voters) if not already in database
    def insert_api_name(self, steamid, nickname):
        res = self.conn.execute('SELECT steamid FROM names_api WHERE steamid = {steamid} AND nickname = "{nickname}"'.format(steamid=steamid, nickname=nickname))
        rows = res.fetchall()
        if len(rows) == 0:
            self.conn.execute('INSERT INTO names_api (steamid, nickname) VALUES ({steamid}, "{nickname}")'.format(steamid=steamid, nickname=nickname))
        self.conn.commit()
        
    # insert names from rcon (active players) if not already in database
    def insert_rcon_name(self, steamid, charname, playername, playerid):
        res = self.conn.execute('SELECT charname FROM names_server WHERE steamid = {steamid} AND charname = "{charname}"'.format(steamid=steamid, charname=charname))
        rows = res.fetchall()
        if len(rows) == 0:
            self.conn.execute('INSERT INTO names_server (steamid, charname, playername, playerid) VALUES ({steamid}, "{charname}", "{playername}", "{playerid}")'.format(steamid=steamid, charname=charname, playername=playername, playerid=playerid))
        self.conn.commit()

    # create tables for database initialisation
    def write_init_database(self):
        self.conn.execute('CREATE TABLE votes (steamid INTEGER, ts_voted INTEGER, ts_redeemed INTEGER, PRIMARY KEY (steamid, ts_voted))')
        self.conn.execute('CREATE TABLE names_api (steamid INTEGER, nickname TEXT)')
        self.conn.execute('CREATE TABLE names_server (steamid INTEGER, charname TEXT, playername TEXT, playerid TEXT)')
        self.conn.commit()

