#Import PySimpleGUI
import PySimpleGUI as psg

def main():

	layout = [
	   [psg.Text('Select a file',font=('Arial Bold', 20), expand_x=True, justification='center')],
	   [psg.Input(enable_events=True, key='-IN-',font=('Arial Bold', 12),expand_x=True),psg.FileBrowse()],
	   [psg.Button('Submit')]
	]
	window = psg.Window('FileChooser Demo', layout,
	size=(1000,700))
	while True:
	   event, values = window.read()
	   if event == psg.WIN_CLOSED or event == 'Exit':
	      break
	window.close()

def open_window():
    layout = [[sg.Text("New Window", key="new")]]
    window = sg.Window("Second Window", layout, modal=True)
    choice = None
    while True:
        event, values = window.read()
        if event == "Exit" or event == sg.WIN_CLOSED:
            break
    window.close()

if __name__ == "__main__":
    main()