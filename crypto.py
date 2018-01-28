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


def get_total(sym_count, currencies):
    total = 0
    for key, value in sym_count.items():
        currency = currencies[key]
        total = total + get_value(sym_count, currency)
    return total


def get_value(sym_count, currency):
    count = sym_count[currency['symbol']]
    return count * float(get_price(currency))


def get_price(c):
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
prices_sheet = client.open("Coins").worksheets()[1]
totals_sheet = client.open("Coins").worksheets()[2]

time = datetime.datetime.now().isoformat(sep=' ')
prices = [time]
totals = [time]

symbols, sym_count = get_symbols(input_sheet)
print(symbols)
currencies = get_currencies(symbols)
for sym in symbols:
    c = currencies[sym]
    prices.append(get_price(c))
    totals.append(get_value(sym_count, c))
total = get_total(sym_count, currencies)
totals.insert(1, total)
print('prices: ', prices)
prices_sheet.append_row(prices)
print('totals: ', totals)
totals_sheet.append_row(totals)

