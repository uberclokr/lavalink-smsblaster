#!/usr/bin/python
import requests
import config
import json
import re

uisp_unms_headers = {
    'Content-Type': 'application/json',
    'x-auth-token': config.uisp_token
}

uisp_ucrm_headers = {
    'Content-Type': 'application/json',
    'X-Auth-App-Key': config.uisp_token
}

def get_client_contacts(ucrm_id:int):

    url = config.uisp_ucrm_url + f'/clients/{ucrm_id}/contacts'
    r = requests.get(url, headers=uisp_ucrm_headers)

    return r.json()

def get_primary_phone(ucrm_id:int):

    contacts = get_client_contacts(ucrm_id)

    for contact in contacts:
        # If phone number exists for contact
        if contact['phone']:
            # Check if contact is tagged General
            for contact_type in contact['types']:
                if 'general' in contact_type['name'].lower():
                    # Contact is primary, cleanup and return this phone number
                    phone = contact['phone'].replace(' ','')
                    phone = re.sub(r'[^\w]', '', phone)
                    phone = re.sub(r'[a-zA-Z]', '', phone)
                    if re.match(r'\+\d{11}$', phone):
                        return phone # number is properly formatted as international +10000000000
                    elif re.match(r'', phone):
                        return f'+1{phone}' # number is formatted as 10-digit domestic, append US country code (+1)
                    else:
                        raise(f"Phone number format could not be determined: {phone}")


def get_sites(abbr=False):

    url = config.uisp_unms_url + '/sites'
    r = requests.get(url, headers=uisp_unms_headers)

    return r.json()

def find_sites(count:int=20, page:int=1, site_type:str='', query:str=''):

    url = config.uisp_unms_url + f'/sites/search?count={count}&page={page}&type={site_type}&query={query}'
    r = requests.get(url, headers=uisp_unms_headers)

    return r.json()

def get_site(id:str, ucrm:bool=False):
    # id : site identifier
    # ucrm : if details should be gathered from ucrm instead

    url = config.uisp_unms_url + f'/sites/{id}?ucrmDetails={ucrm}'
    r = requests.get(url, headers=uisp_unms_headers)

    return r.json()



def get_site_users():

    return uisp_clients
