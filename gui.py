# import PySimpleGUI as sg
#
# layout = [[sg.Text("Hello from PySimpleGUI")], [sg.Button("OK")]]
#
# # Create the window
# window = sg.Window("Demo", layout)
#
# # Create an event loop
# while True:
#     event, values = window.read()
#     # End program if user closes window or
#     # presses the OK button
#     if event == "OK" or event == sg.WIN_CLOSED:
#         break
#
# window.close()
#
#
import PySimpleGUI as sg

layout = [[sg.Text('STEP 1: File processing',font=('Arial', 13, 'bold'))],
          [sg.Text('Select file for processing',font=('Arial', 10, 'bold'))],
          [sg.In(visible=False),
           sg.Input(key='-DIR-', size=(20, None), font=('Arial', 10, 'bold')),
           sg.FileBrowse('Browse', target='-DIR-', font=('Arial', 10, 'bold'),
                         file_types=(("Text Files", "*.txt"), ("CSV Files", "*.csv")))],]

    # [[sg.Text('Date to Start Summing', key='-CALOUTPUT-', font=('Arial', 10, 'bold')), sg.Text(key='-CAL-', size=(10, None), font=('Arial', 10, 'bold'))],
    #       [sg.CalendarButton('Calendar', target='-CAL-', pad=None, font=('Arial', 10, 'bold'), format='%m/%d/%Y')],
    #       [sg.Text('Filename', key='-FOUTPUT-', font=('Arial', 10, 'bold'))],
    #       [sg.In( visible=False),
    #        sg.Input(key='-DIR-', size=(20, None), font=('Arial', 10, 'bold')),
    #        sg.FileBrowse('Browse', target='-DIR-', font=('Arial', 10, 'bold'), file_types=(("Text Files", "*.txt"),("CSV Files","*.csv")))],
    #       [sg.OK(), sg.Cancel()]]


window = sg.Window('EZ PCA KMeans Processor', layout, grab_anywhere=False, size=(500, 500), return_keyboard_events=True,
                   finalize=True)

event, values = window.read()