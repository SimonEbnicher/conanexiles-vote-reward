# vote-reward
Reward voters on conan-exiles.com with ingame items

## setup
Prerequisites for these scripts:
- Python3 (with standard libraries: sqlite3, requests, json, requests)
- Python3 library for Valve RCON protocol ("pip3 install python-valve")

### setup-config.py
Use this helper script to setup the configuration file. Keep ready the following data.

- DB vote decay: This paramater is the number of days a vote is considered valid for redeeming by the player. Older votes will be marked decayed to limit system load.
- RCON address: IP address of the RCON connection of the Conan Server
- RCON port: Port of the RCON connection of the Conan Server
- RCON password: Password of the RCON connection of the Conan Server
- RCON item id: Ingame ID (numerical) of the item given out to the players as voting reward
- RCON item count: How many times the item is given out for each vote
- API key: API key of the server on conan-exiles.com

### setup-database.py
After creating the configuration file, use this script to initialize the database.
All votes that the API allows to read will be written into the database. The API allows only for the last 1000 votes to be read in this way.
Lastly the script will ask you to decay older votes than a given date. This is useful to start at a specified point.
Example: If you have manually given out the votes from February 2023 and wish to start from March 2023 with this system, enter "2023-03-01"

### intermediary checks
If you do not trust this script, examine the database with the SQLITE3 database browser of your choice. Please note that all timestamp will be unix-timestamps measured as seconds, starting from the epoch "1970-01-01 00:00:00"

### vote-worker.py
This script needs to be run periodically to read the API for new votes, check for online players and give out the rewards. Suggested period is between 5 to 15 minutes. Vote reward will only be given out when this script is run.
IMPORTANT: WHEN EXECUTING THIS SCRIPT MAKE SURE THE EXECUTION DIRECTORY IS THE ONE WHERE THE SCRIPT RESIDES! OTHERWISE IT WILL NOT WORK AND NO LOGGING CAN BE DONE! CHECK THIS!

