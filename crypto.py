#!/usr/bin/python3
import os
import requests
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import datetime


def print_currency(c):
    print('{:<14}{:>10}'.format('"%s",' % c['name'], '$' + c['price_sek']))


def get_symbols(sheet):
    values = sheet.row_values(1)
    counts = sheet.row_values(2)
    sym_count = {}
    symbols = []
    i = 1
    for value in values[1:]:
        if value:
            symbols.append(value)
            sym_count[value] = float(counts[i])
        i = i + 1
    return symbols, sym_count


def get_total(symbols, currencies):
    total = 0
    for key, value in symbols.items():
        count = symbols[key]
        total = total + count * float(get_value(currencies[key]))
    return total

def get_value(c):
    return c['price_sek']

def get_currencies(symbols):
    r = requests.get('https://api.coinmarketcap.com/v1/ticker/?convert=SEK&limit=20')
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

input_sheet = client.open("Coins").worksheets()[0]
output_sheet = client.open("Coins").worksheets()[1]

time = datetime.datetime.now().isoformat(sep=' ')
values = [time]

symbols, sym_count = get_symbols(input_sheet)
print(symbols)
currencies = get_currencies(symbols)
for sym in symbols:
    c = currencies[sym]
    values.append(get_value(c))
total = get_total(sym_count, currencies)
values.insert(1, total)
print('adding: ', values)
output_sheet.append_row(values)

