import string
import PySimpleGUI as sg
import os
from codelib import convert_csv
from mpfigshow  import show_fig
from pca_kmeans import pca_initial

sg.theme('SystemDefault')
sg.SetOptions(element_padding=(0, 0))


layout = [[sg.Text('STEP 1: File processing', font=('Lato', 13, 'bold'))],
          [sg.Text('Select file for processing', font=('Lato', 10, 'bold'), size=(30, 2))],
          [sg.In(visible=False),
           sg.Input(key='-DIR-', enable_events=True, visible=False),
           sg.Text('                             ', key='-FILENAME-', size=(20, 1)),
           sg.FileBrowse('Browse', target='-DIR-', size=(15, 1),
                         file_types=(("Text Files", "*.txt"), ("CSV Files", "*.csv"))),
           sg.Button('Open', button_color=('white', 'red'), size=(10, 1), key='_OPEN_', disabled=True)],
          [sg.In(visible=False),
           sg.Input(key='_PCSV_', enable_events=True, visible=False),
           sg.Text('                             ', key='-FN_2-', size=(20, 1)),
           sg.FileSaveAs("Save File As", target='_PCSV_', size=(15, 1)),
           sg.Button('Save', button_color=('white', 'green'), size=(10, 1), key='_SAVECSV_')],
          [sg.Text('_' * 100, justification='center', text_color='gray', size=(100, 1))],  # horizontal separator
          [sg.Text('STEP 2: Run Principal Component Analysis', font=('Lato', 13, 'bold'))],
          [sg.Text('Initial PCA Run (20 components)', font=('Lato', 10, 'bold'), size=(30, 2))],
          [sg.Button('Initial PCA', button_color=('white', 'green'), key='_PCA1_', size=(15, 1)), sg.Button('Open Fig', key='_FIG_OPEN1_', disabled=True)],
          [sg.Button('Exit')], ]



main_window = sg.Window('EZ PCA KMeans Processor', layout, grab_anywhere=False, size=(500, 500),
                        return_keyboard_events=True,
                        finalize=True)

main_window['_SAVECSV_'].update(disabled=True)
save_handl = False

while True:
    event, values = main_window.read()

    fn_1 = os.path.basename(values['-DIR-'])
    fn_2 = os.path.basename(values['_PCSV_'])
    print(event, values, fn_1, fn_2)
    main_window.element('-FILENAME-').Update(fn_1)
    main_window.element('-FN_2-').Update(fn_2)

    if save_handl and not fn_2 == '':
        main_window['_SAVECSV_'].update(disabled=False)
    if not fn_1 == '':
        main_window['_OPEN_'].update(disabled=False)

    # window event handling
    if event == sg.WIN_CLOSED or event == 'Exit':
        exit()
    if event == '_OPEN_':
        new_csv = convert_csv(values['-DIR-'])
        save_handl = True
    if event == '_PCA1_':
        pca1_fig = pca_initial(new_csv)
        main_window['_FIG_OPEN1_'].update(disabled=False)
    if event == '_SAVECSV_':
        new_csv.to_csv(values['_PCSV_'])
    if event == '_FIG_OPEN1_':
        show_fig(pca1_fig)


        # In older code you'll find it written using FindElement or Element
        # window.FindElement('-OUTPUT-').Update(values['-IN-'])
        # A shortened version of this update can be written without the ".Update"
        # window['-OUTPUT-'](values['-IN-'])
