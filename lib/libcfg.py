#!/usr/bin/python3

import json

class CFG():
    def __init__(self, path):
        self._cfg_path        = path
        self._db_path         = None
        self._db_vote_decay   = None
        self._rcon_addr       = None
        self._rcon_port       = None
        self._rcon_pwd        = None
        self._rcon_item_id    = None
        self._rcon_item_count = None
        self._api_key         = None

    @property
    def db_path(self):
        return self._db_path
    @db_path.setter
    def db_path(self, value):
        self._db_path = value

    @property
    def db_vote_decay(self):
        return self._db_vote_decay
    @db_vote_decay.setter
    def db_vote_decay(self, value):
        self._db_vote_decay = value

    @property
    def rcon_addr(self):
        return self._rcon_addr
    @rcon_addr.setter
    def rcon_addr(self, value):
        self._rcon_addr = value

    @property
    def rcon_port(self):
        return self._rcon_port
    @rcon_port.setter
    def rcon_port(self, value):
        self._rcon_port = value

    @property
    def rcon_pwd(self):
        return self._rcon_pwd
    @rcon_pwd.setter
    def rcon_pwd(self, value):
        self._rcon_pwd = value

    @property
    def rcon_item_id(self):
        return self._rcon_item_id
    @rcon_item_id.setter
    def rcon_item_id(self, value):
        self._rcon_item_id = value

    @property
    def rcon_item_count(self):
        return self._rcon_item_count
    @rcon_item_count.setter
    def rcon_item_count(self, value):
        self._rcon_item_count = value

    @property
    def api_key(self):
        return self._api_key
    @api_key.setter
    def api_key(self, value):
        self._api_key = value


    def read_config(self):
        f = open(self._cfg_path)
        cfg = json.load(f)
        f.close()
        self._db_path         = str(cfg['db_path'])
        self._db_vote_decay   = int(cfg['db_vote_decay'])
        self._rcon_addr       = str(cfg['rcon_addr'])
        self._rcon_port       = int(cfg['rcon_port'])
        self._rcon_pwd        = str(cfg['rcon_pwd'])
        self._rcon_item_id    = int(cfg['rcon_item_id'])
        self._rcon_item_count = int(cfg['rcon_item_count'])
        self._api_key         = str(cfg['api_key'])


    def write_config(self):
        x  = '{\n'
        x += '  "db_path"         : "{db_path}",\n'.format(db_path=self._db_path)
        x += '  "db_vote_decay"   : {db_vote_decay},\n'.format(db_vote_decay=self._db_vote_decay)
        x += '  "rcon_addr"       : "{rcon_addr}",\n'.format(rcon_addr=self._rcon_addr)
        x += '  "rcon_port"       : {rcon_port},\n'.format(rcon_port=self._rcon_port)
        x += '  "rcon_pwd"        : "{rcon_pwd}",\n'.format(rcon_pwd=self._rcon_pwd)
        x += '  "rcon_item_id"    : {rcon_item_id},\n'.format(rcon_item_id=self._rcon_item_id)
        x += '  "rcon_item_count" : {rcon_item_count},\n'.format(rcon_item_count=self._rcon_item_count)
        x += '  "api_key"         : "{api_key}"\n'.format(api_key=self._api_key)
        x += '}\n'
        f = open(self._cfg_path, "w")
        f.write(x)
        f.close()

