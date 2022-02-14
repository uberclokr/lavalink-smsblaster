# lavalink-smsblaster
A tool for sending maintenance and outage alerts via SMS

## API docs
UISP-NMS: https://unms.lavalink.us/nms/api-docs/#/
UISP-CRM: https://unmscrm.docs.apiary.io/#
GoTo/Jive: https://developer.goto.com/GoToConnect#tag/Messaging-Overview

## Prerequisites
python3
nodejs (with express module)

## Setup
For first time use, you *MUST*...

[1]==== Populate config.py with appropriate values ============================

goto_client_id, goto_client_secret, goto_redirect_uri, jive_owner_phone, uisp_token

*See config-example.py for a sample template with all required values*

[2]==== Execute smsblaster.py independently using the --init flag. ============

> python3 smsblaster.py --init

*You will be prompted to authorize your SMS app access (supports GoTo at this time) at the provided URL. Once authenticated with the SMS provider, the session should be headlessly renewable. At this point you may start the node server.*

[3]==== Sart the node web server from within the root directory ===============

> npm start
