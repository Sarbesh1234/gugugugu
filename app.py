#Import PySimpleGUI
import PySimpleGUI as sg
 
#Draw the button
layout = [[sg.Button('Hello, New Stack', size=(30,4))]]
 
#Draw the window
window = sg.Window('GUI SAMPLE', layout, size=(1000,700))
 
#Define what happens when the button is clicked
event, values = window.read()