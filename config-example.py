#!/usr/bin/python

# GoTo
goto_client_id = ''
goto_client_secret = ''
goto_redirect_uri = 'https://lavalink.us'
goto_auth_url = f'https://api.getgo.com/oauth/v2/authorize?client_id={goto_client_id}&response_type=code&redirect_uri={goto_redirect_uri}'
goto_access_url = 'https://api.getgo.com/oauth/v2/token'

# Jive
## Phone number with GoTo/Jive that SMS messages will be sourced from. This MUST be in international format (i.e. +1XXXXXXXXXX)
jive_owner_phone = ''

# UISP
uisp_unms_url = 'https://unms.lavalink.us/nms/api/v2.1'
uisp_ucrm_url = 'https://unms.lavalink.us/crm/api/v1.0'
uisp_token = ''