![Lavalink Logo](https://lavalink.us/wp-content/uploads/2017/09/g4638.png)

# SMS Blaster
A tool for sending maintenance and outage alerts via SMS

## API docs
- UISP-NMS: https://unms.lavalink.us/nms/api-docs/#/
- UISP-CRM: https://unmscrm.docs.apiary.io/#
- GoTo/Jive: https://developer.goto.com/GoToConnect#tag/Messaging-Overview

## Prerequisites
- python3
- nodejs w/modules express, pm2

## Setup
For first time use, you *MUST*...

[1]==== Populate config.py with appropriate values ============================

goto_client_id, goto_client_secret, goto_redirect_uri, jive_owner_phone, uisp_token

*See config-example.py for a sample template with all required values*

[2]==== Execute smsblaster.py independently using the --init flag. ============

> python3 smsblaster.py --init

*You will be prompted to authorize your SMS app access (supports GoTo at this time) at the provided URL. Once authenticated with the SMS provider, the session should be headlessly renewable. At this point you may start the node server.*

[3]==== Install node prerequisite packages =================================================

> npm install express
> sudo npm install pm2@latest -g

[4]==== Sart the node web server from within the root directory ===============

You have two(2) options -- either run in current shell...

> npm start

...or daemonize with pm2...

> pm2 start app.js

See this guide for completing daemonized instance: https://www.digitalocean.com/community/tutorials/how-to-set-up-a-node-js-application-for-production-on-ubuntu-18-04
