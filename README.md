# lavalink-smsblaster
A tool for sending maintenance and outage alerts via SMS

## Prerequisites
python3
nodejs (with express module)

## Setup
For first time use, you *MUST* execute smsblaster.py independently using the --init flag.
> python3 smsblaster.py --init

You will be prompted to authorize your SMS app access (supports GoTo at this time) at the provided URL. Once authenticated with the SMS provider, the session should be headlessly renewable.

Once SMS provider access has been established, you may start the node web server from within the root directory using
> npm start
