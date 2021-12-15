#  Philsoft  (c) 2021.

import PySimpleGUIQt as sg
import os
import asyncio

from PySimpleGUIQt import FillFormWithValues
from dotenv import load_dotenv
from supabase import create_client, Client

from func import removeFileSelectFromDict

load_dotenv()

url: str = os.environ.get("SUPABASE_URL")
key: str = os.environ.get("SUPABASE_KEY")
supabase: Client = create_client(url, key)
files = supabase.storage().StorageFileAPI('files')
loop = asyncio.get_event_loop()

sg.theme('SystemDefault')  # Add a touch of color
# All the stuff inside your window.
layout = [[sg.Text('ID', size=(15, 1)), sg.InputText(key='ID', tooltip='Bei neuen Clickboards freilassen!'), sg.Button('Abrufen'), sg.Button('Loeschen')],
          [sg.Text('Name', size=(15, 1)), sg.InputText(key='NAME')],
          [sg.Text('Ersteller', size=(15, 1)), sg.InputText(key='AUTHOR', default_text='Helmut Strasser')],
          [sg.Text('Kurzbeschreibung', size=(15, 1)), sg.Multiline(key='SHORT_DESCRIPTION')],
          [sg.Text('Bild-URL', size=(15, 1)), sg.InputText(key='IMG_URL'), sg.FileBrowse(key='FILE_IMG', file_types=(('Bilddateien', '*.jpg; *.jpeg; *.png'),('Alle Dateitypen','*.*')), button_text='Auswählen')],
          [sg.Text('Dokumentation-URL', size=(15, 1)), sg.InputText(key='DOK_URL'), sg.FileBrowse(key='FILE_DOK', file_types=(('Dokumente', '*.pdf; *.doc; *.docx; *.otd'),('Alle Dateitypen','*.*')), button_text='Auswählen')],
          [sg.Text('Schaltplan-URL', size=(15, 1)), sg.InputText(key='SCH_URL'), sg.FileBrowse(key='FILE_SCH', file_types=(('Schaltplan-Dateien', '*.sch;'),('Alle Dateitypen','*.*')), button_text='Auswählen')],
          [sg.Text('Board-URL', size=(15, 1)), sg.InputText(key='BRD_URL'), sg.FileBrowse(key='FILE_BRD', file_types=(('Board-Dateien', '*.brd;'),('Alle Dateitypen','*.*')), button_text='Auswählen')],
          [sg.Text('3D-URL', size=(15, 1)), sg.InputText(key='STP_URL'), sg.FileBrowse(key='FILE_STP', file_types=(('3D-Dateien', '*.stp; *.step; *.3d'),('Alle Dateitypen','*.*')), button_text='Auswählen')],
          [sg.Button('Erstellen', size=(20, 1)), sg.Button('Updaten', size=(20, 1)), sg.Exit('Beenden', size=(20, 1))]]

# Create the Window
window = sg.Window('FTKL-Clickboards Admin Tool', layout)
# Event Loop to process "events" and get the "values" of the inputs
while True:
	event, values = window.read()
	if event == sg.WIN_CLOSED or event == 'Beenden':  # if user closes window or clicks cancel
		break
	if event == 'Erstellen':
		del values['ID']
		values = removeFileSelectFromDict(values)
		response = supabase.table('CLICKBOARDS').insert(values).execute()
		if response['status_code'] == 201:
			sg.popup_ok('Clickboard wurde erstellt erfolgreich erstellt.')

	if event == 'Updaten':
		values = removeFileSelectFromDict(values)

		def uploadFile(osFilePath: str, clkbrdId: str, mimeType: str = 'file/xml'):
			if osFilePath.startswith('http'):
				return osFilePath
			else:
				# Get filename->(path[0]) & file-extention->(path[1])
				path = osFilePath.split('/')[-1].split('.')

				#                eg.  4       /     sch      /     schaltplan .    sch
				onlinePath: str = clkbrdId + '/' + path[1] + '/' + path[0] + '.' + path[1]

				# Upload File to the Storage Bucket
				files.upload(onlinePath, osFilePath, file_options={'contentType': mimeType})

				# Get Public URL of the uploaded item
				publicUrl = files.get_public_url(onlinePath)

				return publicUrl


		if values['IMG_URL']:
			# Upload IMG (JPG / PNG)
			values['IMG_URL'] = uploadFile(
				osFilePath=values['IMG_URL'],
				clkbrdId=values['ID'],
				mimeType='image/' + values['IMG_URL'].split('/')[-1].split('.')[1].lower()
			)

		if values['DOK_URL']:
			# Upload DOK (PDF) File
			values['DOK_URL'] = uploadFile(
				osFilePath=values['DOK_URL'],
				clkbrdId=values['ID'],
				mimeType='application/' + values['DOK_URL'].split('/')[-1].split('.')[1].lower()
			)

		if values['SCH_URL']:
			# Upload SCH File (default file/xml mimeType)
			values['SCH_URL'] = uploadFile(
				osFilePath=values['SCH_URL'],
				clkbrdId=values['ID'],
			)

		if values['BRD_URL']:
			# Upload BRD File (default file/xml mimeType)
			values['BRD_URL'] = uploadFile(
				osFilePath=values['BRD_URL'],
				clkbrdId=values['ID'],
			)

		if values['STP_URL']:
			# Upload 3D File
			values['STP_URL'] = uploadFile(
				osFilePath=values['STP_URL'],
				clkbrdId=values['ID'],
				mimeType='application/octet-stream'
			)

		response = supabase.table('CLICKBOARDS').insert(values, upsert=True).execute()
		print(response)
		if response['status_code'] == 201:
			sg.popup_ok('Clickboard wurde erfolgreich aktualisiert.')
	if event == 'Abrufen':
		response = supabase.table('CLICKBOARDS').select('*').eq('ID', values['ID']).execute()
		if response['status_code'] == 200:
			if response['data']:
				FillFormWithValues(window, response['data'][0])
			else:
				sg.popup_error('Clickboard nicht gefunden :/')
		print(response)

	if event == 'Loeschen':
		response = supabase.table('CLICKBOARDS').delete().eq('ID', values['ID']).execute()
		if response['status_code'] == 200:
			sg.popup_ok('Clickboard mit der ID: ' + values['ID'] + ' wurde erfolgreich gelöscht')

	print('You entered ', values)

window.close()