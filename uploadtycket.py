#!/usr/bin/env python
# -*- coding: utf-8 -*-
import dropbox
import config
import gspread
import os
from oauth2client.service_account import ServiceAccountCredentials


def filename(timestamp):
    return str(round(timestamp))


def upload_file(file, file_to):
    """upload a file to Dropbox using API v2
    """
    dbx = dropbox.Dropbox(config.dropbox_accesstoken)
    dbx.files_upload(file, file_to)
    shared_url = dbx.sharing_create_shared_link_with_settings(file_to).url
    return shared_url

#Update multiple cell values using gspread
# use creds to create a client to interact with the Google Drive API
def update_google_sheet(filename, url):
    scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
    creds = ServiceAccountCredentials.from_json_keyfile_name(os.path.join(config.static_folder,
                                                                          '/tycket-sheet-update-151fce232bca.json'),
                                                                          scope)
    client = gspread.authorize(creds)
    wks= client.open('tycket-images').sheet1
    wks.append_row([filename, url])
