#!/usr/bin/python
import goto
import uisp
import json
import sys

"""
SMS BLASTER
- Bulk SMS text messaging dispatcher for Lavalink outage and maintenance notices

Usage:
    python3 smsblaster.py --message "<sms_message>" --site <site_name>
    -OR-
    python3 smsblaster.py -m "<sms_message>"

    TO GET SITE LIST
    python3 smsblaster.py --get-sites

Flags:
    --site

For GoTo developer information: https://developer.goto.com/guides/HowTos/03_HOW_accessToken
"""
def main():

    # Load recipients list
    #recipients = []
    #for line in sys.stdin:
    #    recipients.append(line.replace('\n','').replace('\r',''))

    # Load arguments
    site = ''
    message = ''
    for idx, arg in enumerate(sys.argv):
        if arg in ['-m', '--message']:
            message = sys.argv[idx+1]
        elif arg in ['-s', '--site']:
            site = sys.argv[idx+1]
        elif arg in ['--get-sites']:
            sites = uisp.find_sites(site_type='site',query=site)
            site_names = []
            for site in sites:
                print(site['identification']['name'])
            quit()
        elif arg in ['--init']:
            client = goto.GoToClient()
            quit()

    # Initialize goto session
    client = goto.GoToClient()

    # Get contact numbers for site(s)
    sites = uisp.find_sites(site_type='site',query=site)
    customer_count = 0
    active_customers = 0
    recipients = []
    for site in sites:

        customers = site['description']['endpoints']

        print(f"""{site['identification']['name'].upper()}
        ID: {site['id']}
        Address: {site['description']['address']}
        Customers: {len(customers)}""")
        customer_count += len(customers)

        for customer in customers:

            customer_site = uisp.get_site(id=customer['id'],ucrm=True)

            # If customer is active and linked to UCRM, retrieve primary phone number
            if customer_site['identification']['status'] != 'inactive' and customer_site is not None and 'ucrm' in customer_site and customer_site['ucrm'] is not None and 'client' in customer_site['ucrm'] and 'id' in customer_site['ucrm']['client']:
                ucrm_id = customer_site['ucrm']['client']['id']
                customer_phone = uisp.get_primary_phone(ucrm_id)
                active_customers += 1
                #print(f"""          {customer['name']} {customer['id']} {customer_phone}""")
                if customer_phone not in recipients:
                    recipients.append(customer_phone)
            else:
                #print(f"        ! {customer['name']} NO UCRM INFO... SKIPPING!")
                pass

        print('')

    print(f'{len(sites)} sites found')
    print(f'{active_customers} active customers')
    print(f'{customer_count} total customers')

    # Send message to all recipients
    for recipient in recipients:
        resp_status = client.send_sms(message, recipient)
        print(f"Attempted message to {recipient} - HTTP response {resp_status}")

if __name__ == '__main__':
    main()