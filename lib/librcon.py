#!/usr/bin/python3

import valve.rcon as rcon

class RCON:
    def __init__(self, address, port, password):
        self.address  = address
        self.port     = port
        self.password = password

    def get_players_online(self):
        cmd = 'listplayers'
        resp = rcon.execute(address=(self.address, self.port), password=self.password, command=cmd)
        lines = resp.splitlines()
        players = []
        for line in lines:
            fields = line.split('|')
            if fields[0].strip(' ').isdigit():
                charname   = fields[1].strip(' ')
                playername = fields[2].strip(' ')
                playerid   = fields[3].strip(' ')
                steamid    = fields[4].strip(' ')
                players.append( {'charname': charname, 'playername': playername, 'playerid': playerid, 'steamid': steamid} )
        return players

    def give_items_to_player(self, playername, itemid, itemcount):
        cmd = 'con {playername} SpawnItem {itemid} {itemcount}'.format(playername=playername, itemid=itemid, itemcount=itemcount)
        resp = rcon.execute(address=(self.address, self.port), password=self.password, command=cmd)
        #print(str(resp))
        if 'Successfully executed: '+cmd in str(resp):
            return True
        else:
            return False
        # Successfully executed: con WachtelKing#70344 SpawnItem 11066 10

    def broadcast(self, message):
        cmd = 'broadcast {message}'.format(message=message)
        resp = rcon.execute(address=(self.address, self.port), password=self.password, command=cmd)
        #print(str(resp))
        if 'Message has been broadcast' in str(resp):
            return True
        else:
            return False
        # Message has been broadcast.

    def restart(self):
        cmd = 'restart'
        resp = rcon.execute(address=(self.address, self.port), password=self.password, command=cmd)
        #print(str(resp))
        if 'Successfully executed: '+cmd in str(resp):
            return True
        else:
            return False
        # Successfully executed: restart 

