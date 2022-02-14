# lavalink-smsblaster
A tool for sending maintenance and outage alerts via SMS

# Setup
1. For first time use, you *MUST* execute smsblaster.py independently. You will be prompted to authorize your SMS app access (supports GoTo at this time) at the provided URL. Once authenticated with the SMS provider, the session should be headlessly renewable.
2. Once SMS provider access has been established, you may run the node web server from within the root directory using
> npm start
