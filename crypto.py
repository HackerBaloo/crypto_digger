#!/usr/bin/python3
import os
import requests
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import datetime


def print_currency(c):
    print('{:<14}{:>10}'.format('"%s",' % c['name'], '$' + c['price_usd']))


def get_symbols(sheet):
    values = sheet.row_values(1)
    symbols = []
    for value in values[1:]:
        if not value:
            continue
        symbols.append(value)
    return symbols


def get_value(c):
    return c['price_usd']

def get_currencies(symbols):
    r = requests.get('https://api.coinmarketcap.com/v1/ticker/')
    json = r.json()
    currencies = {}

    for c in json:
        if c['symbol'] in symbols:
            currencies[c['symbol']] = c

    return currencies


# use creds to create a client to interact with the Google Drive API
scope = ['https://spreadsheets.google.com/feeds']
home_dir = os.path.expanduser('~')
credential_dir = os.path.join(home_dir, 'Dropbox', '.credentials')
credential_path = os.path.join(credential_dir, 'client_secret.json')
creds = ServiceAccountCredentials.from_json_keyfile_name(credential_path, scope)
client = gspread.authorize(creds)

sheet = client.open("Coins").worksheets()[1]

time = datetime.datetime.now().isoformat(sep=' ')
values = [time]

symbols = get_symbols(sheet)
print(symbols)
currencies = get_currencies(symbols)
for sym in symbols:
    c = currencies[sym]
    values.append(get_value(c))
print('adding: ', values)
sheet.append_row(values)

