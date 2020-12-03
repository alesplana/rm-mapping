import PySimpleGUI as sg
import os
import threading
from codelib import convert_csv
from mpfigshow import show_fig
from pca_kmeans import pca_initial
from pca_kmeans import pca_final

sg.theme('SystemDefault')
sg.SetOptions(element_padding=(1, 1))

headFont = ('Helvetica', 15, 'bold')
head2Font = ('Helvetica', 12)

sg.set_options(font=('Helvetica', 11))

def open_and_convert(window):  # worker thread
    global new_csv
    new_csv = convert_csv(values['-DIR-'])
    window.write_event_value('-THREAD-', "** DONE **")


layout = [[sg.Text('STEP 1: File processing', font=headFont)],
          [sg.Text('Select file for processing', font=head2Font, size=(30, 2))],
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
          [sg.Text('_' * 100, justification='center', text_color='gray', size=(100, 2))],  # horizontal separator
          [sg.Text('STEP 2: Run Principal Component Analysis', font=headFont)],
          [sg.Text('Initial PCA Run (20 components)', font=head2Font, size=(25, 1)),
           sg.Button('Initial PCA', button_color=('white', '#e7b416'), key='_PCA1_', size=(15, 1), disabled=True),
           sg.Button('Open Fig', key='_FIG_OPEN1_', disabled=True, size=(10, 1))],
          [sg.Text('Number of Principal Components:', font=head2Font, size=(25, 1)),
           sg.Combo(list(range(2, 4)), size=(5, 2), key='_NCOM_', enable_events=True),
           sg.Button('Run PCA', button_color=('white', 'green'), key='_PCA2_', size=(15, 1), disabled=True),
           sg.Button('Open Fig', key='_FIG_OPEN2_', disabled=True, size=(10, 1))],
          [sg.Text('_' * 100, justification='center', text_color='gray', size=(100, 2))],  # horizontal separator
          [sg.Text('STEP 3: Cluster using K-Means', font=headFont)],
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
    print(event, values, values['_NCOM_'])
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
        # new_csv = convert_csv(values['-DIR-'])
        # save_handl = True
        threading.Thread(target=open_and_convert, args=(main_window,), daemon=True).start()
    if event == '-THREAD-':
        save_handl = True
        main_window['_PCA1_'].update(disabled=False)
        main_window['_PCA2_'].update(disabled=False)
    if event == '_PCA1_':
        pca1_fig = pca_initial(new_csv)
        main_window['_FIG_OPEN1_'].update(disabled=False)
    if event == '_PCA2_':
        scores, pca2_fig = pca_final(new_csv, values['_NCOM_'])
        main_window['_FIG_OPEN2_'].update(disabled=False)
        main_window['_FIG_OPEN1_'].update(disabled=True)
    if event == '_SAVECSV_':
        new_csv.to_csv(values['_PCSV_'])
    if event == '_FIG_OPEN1_':
        pca1_fig.show()
        # show_fig(pca1_fig)
    if event == '_FIG_OPEN2_':
        pca2_fig.show()
        # show_fig(pca2_fig)

        # In older code you'll find it written using FindElement or Element
        # window.FindElement('-OUTPUT-').Update(values['-IN-'])
        # A shortened version of this update can be written without the ".Update"
        # window['-OUTPUT-'](values['-IN-'])
