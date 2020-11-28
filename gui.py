import PySimpleGUI as sg
import os

sg.theme('SystemDefault')

layout = [[sg.Text('STEP 1: File processing', font=('Lato', 13, 'bold'))],
          [sg.Text('Select file for processing')],
          [sg.In(visible=False),
           sg.Input(key='-DIR-', size=(1, None), font=('Arial', 10), enable_events=True, visible=False),
           sg.FileBrowse('Browse', target='-DIR-',
                         file_types=(("Text Files", "*.txt"), ("CSV Files", "*.csv"))),
           sg.Text('                             ', key='-FILENAME-')],
          [sg.Button('Exit')],]

# [[sg.Text('Date to Start Summing', key='-CALOUTPUT-', font=('Arial', 10, 'bold')), sg.Text(key='-CAL-', size=(10, None), font=('Arial', 10, 'bold'))],
#       [sg.CalendarButton('Calendar', target='-CAL-', pad=None, font=('Arial', 10, 'bold'), format='%m/%d/%Y')],
#       [sg.Text('Filename', key='-FOUTPUT-', font=('Arial', 10, 'bold'))],
#       [sg.In( visible=False),
#        sg.Input(key='-DIR-', size=(20, None), font=('Arial', 10, 'bold')),
#        sg.FileBrowse('Browse', target='-DIR-', font=('Arial', 10, 'bold'), file_types=(("Text Files", "*.txt"),("CSV Files","*.csv")))],
#       [sg.OK(), sg.Cancel()]]

window = sg.Window('EZ PCA KMeans Processor', layout, grab_anywhere=False, size=(500, 500), return_keyboard_events=True,
                   finalize=True)

while True:
    event, values = window.read()

    fn = os.path.basename(values['-DIR-'])
    print(event, values, fn)
    window.element('-FILENAME-').Update(fn)

    if event == sg.WIN_CLOSED or event == 'Exit':
        exit()
    if event == '':
        print('hello')
    if event == 'Show':
        # Update the "output" text element to be the value of "input" element
        window['-OUTPUT-'].update(values['-IN-'])

        # In older code you'll find it written using FindElement or Element
        # window.FindElement('-OUTPUT-').Update(values['-IN-'])
        # A shortened version of this update can be written without the ".Update"
        # window['-OUTPUT-'](values['-IN-'])



event, values = window.read()
