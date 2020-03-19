import os
import sys
import re
import uuid
import requests
import shutil as fs
import PySimpleGUI as gui
from PySimpleGUI import Text, InputText, Button, Checkbox, PopupOK, Radio


def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


GAME_ID = {
    'Steam': '1843',
    'UPlay': '635'
}
DATA_PATH = resource_path('1.save')
print(DATA_PATH)
SAVE_DIR = 'C:\\Program Files (x86)\\Ubisoft\\Ubisoft Game Launcher\\savegames'
LICENSE_SERVER = 'http://eliteskins-license-server.herokuapp.com/verify/'  # POST
DEVICE_MAC = (':'.join(re.findall('..', '%012x' % uuid.getnode()))) + f'[RAW:{hex(uuid.getnode())}]'


def install(method: str):
    os.system('taskkill -f -im upc.exe & taskkill -f -im UplayWebCore.exe')
    accounts = os.listdir(SAVE_DIR)
    for account_id in accounts:
        path = f'{SAVE_DIR}\\{account_id}'
        if GAME_ID[method] not in os.listdir(path):
            continue
        path += f'\\{GAME_ID[method]}\\1.save'
        fs.copyfile(DATA_PATH, path)


# Start UI
gui.theme('DarkBlue')
layout = [
    [Text('EliteSkins Rainbow Six Siege Skins Installer\n')],
    [Text('Please ensure you have disabled Ubisoft Cloud Save and have recently opened Rainbow 6 Siege.')],
    [Text('Enter your License Key:'), InputText()],
    [Text('I installed Rainbow Six Siege using: '), Radio('Steam', 'install_method'), Radio('UPlay', 'install_method')],
    [Checkbox('I understand that the creators of this installer are not responsible for any damage caused by its use.')],
    [Button('Install'), Button('Cancel')]
]


window = gui.Window('EliteSkins Installer', layout)
while True:
    event, values = window.read()
    if event in (None, 'Cancel'):
        break

    if event == 'Install':
        key = values[0]
        confirm = values[3]
        if not (values[1] or values[2]):
            PopupOK('You must select either Steam or UPlay')
            continue
        install_method = 'Steam' if values[1] else 'UPlay'
        if confirm != 1:
            PopupOK('You must check the box to confirm the installation.')
            continue

        res = requests.post(LICENSE_SERVER, {'key': key, 'machine_id': DEVICE_MAC}).json()
        if not res['success']:
            PopupOK('The specified license key is invalid.')
            continue
        install(install_method)
        PopupOK('Installation Successful!')
        break

window.close()
