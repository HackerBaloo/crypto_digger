#!/usr/bin/python3
import os
import gspread
from oauth2client.service_account import ServiceAccountCredentials


def main():
    # use credentials to create a client to interact with the Google Drive API
    scope = ['https://spreadsheets.google.com/feeds']
    home_dir = os.path.expanduser('~')
    credential_dir = os.path.join(home_dir, 'Dropbox', '.credentials')
    credential_path = os.path.join(credential_dir, 'client_secret.json')
    credentials = ServiceAccountCredentials.from_json_keyfile_name(credential_path, scope)
    client = gspread.authorize(credentials)

    sheet = client.open("GSpread_test").worksheets()[0]
    sheet.append_row([1234.1234, '1234.1234', '1234,1234', '1 234,1234'])

    # In the spreadsheet with swedish locale it results in this:
    #     A      |     B      |    C      |    D
    # 1254.34.00 | 1254.34.00 | 1234,1234 | 1234,1234
    # column C & D are correct but A & B very strange
    # swedish number format has comma as decimal delimiter and no space
    # for 1000 delimiter
    # I think it would be reasonable that col A should be right, since
    # the input is a Python float
    # perhaps some optional parameter should be needed to make it work


main()
