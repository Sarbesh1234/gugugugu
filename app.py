#Import PySimpleGUI
import PySimpleGUI as psg

import essential
from essential import *

def min():

    layout = [
       [psg.Text('Select a file',font=('Arial Bold', 20), expand_x=True, justification='center')],
       [psg.Input(enable_events=True, key='-IN-',font=('Arial Bold', 12),expand_x=True),psg.FileBrowse()],
       [psg.Button('Male')],
       [psg.Button('Female')]
    ]
    window = psg.Window('FileChooser Demo', layout,size=(1000,700))
    while True:
        event, values = window.read()
        if event == psg.WIN_CLOSED or event == 'Male' or event == 'Female':
            window.close()
            file_path = values
            essential.some_shit(str(file_path['-IN-']),str(event))



    window.close()

def open_window():
    layout = [[psg.Text("New Window", key="new")]]
    window = psg.Window('Results', layout,size=(1000,700))
    choice = None
    while True:
        event, values = window.read()
        if event == "Exit" or event == psg.WIN_CLOSED:
            break
    window.close()

if __name__ == "__main__":
    min()