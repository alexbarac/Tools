import PySimpleGUI as sg

from connection.Connection import Connection

sg.theme('DarkAmber')   # Add a touch of color
# All the stuff inside your window.
layout = [  [sg.Text('Branch Name'), sg.InputText(default_text="cloud2-",size=(14, 0),focus=True),sg.InputCombo(['Beta', 'Dev'], size=(9, 0),default_value='Beta'), sg.Button('Save') ],
            [ sg.Text('Type Branch(v1/v2)'),sg.InputCombo(['v2', 'v1'], size=(5, 0),default_value='v2')]]
# Create the Window
window = sg.Window("Change Branch Credentials", layout, size=(500,100))
# Event Loop to process "events" and get the "values" of the inputs
while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED or event == 'Cancel': # if user closes window or clicks cancel
        break
    print('You entered ', values[0])
    client = Connection(values)
    client._connect()

window.close()