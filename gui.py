# last edited: 02/17/2021

import PySimpleGUI as sg
import os
import threading
from mpfigshow import show_fig
from filehndl import convert_csv
from pca_kmeans import pca_initial_ as pca_i
from pca_kmeans import pca_final_ as pca_f
from pca_kmeans import cluster_variance as kgraph_
from pca_kmeans import kmeans_
from pca_kmeans import gen_map
from pca_kmeans import res_vbose
from pca_kmeans import clavg_fig

sg.theme('SystemDefault')
sg.SetOptions(element_padding=(1, 1))

headFont = ('Helvetica', 15, 'bold')
head2Font = ('Helvetica', 12)

sg.set_options(font=('Helvetica', 11))


def open_and_convert(window):  # worker thread convert csv
    global new_csv
    new_csv, stat = convert_csv(values['-DIR-'])
    if stat == 0:
        window.write_event_value('-THREAD-', "** DONE **")
    elif stat == 1:
        window.write_event_value('-THREAD-', "Error 1")
        print('Invalid File')


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
           sg.Button('Open Scree Plot', button_color=('white', '#e7b416'), key='_PCA1_', size=(23, 1), disabled=True),
           sg.Button('Open Scree Plot', key='_FIG_OPEN1_', disabled=True, size=(15, 1), visible=False)],
          [sg.Text('Number of Principal Components:', font=head2Font, size=(25, 1)),
           sg.Combo(list(range(2, 11)), size=(5, 2), key='_NCOM_', enable_events=True),
           sg.Button('Run PCA', button_color=('white', 'green'), key='_PCA2_', size=(15, 1), disabled=True),
           sg.Button('Open Fig', key='_FIG_OPEN2_', disabled=True, size=(10, 1), visible=False)],
          [sg.Text('_' * 100, justification='center', text_color='gray', size=(100, 2))],  # horizontal separator
          [sg.Text('STEP 3: Cluster using K-Means', font=headFont)],
          [sg.Text('Identify the optimal value for k using the total distance vs k value graph.')],
          [sg.Button('Show Graph', key='-KGRAPH-', size=(15, 1), disabled=True, button_color=('white', 'green'))],
          [sg.Text('                             ', size=(20, 1)), ],
          [sg.Text('K-Value:', font=head2Font, size=(7, 1)),
           sg.Combo(list(range(1, 11)), size=(6, 2), key='_KVAL_', enable_events=True)],
          [sg.Button('Run K-Means', key='-KMEANS-', size=(15, 1), disabled=True, button_color=('white', 'green')),
           sg.Button('Open Clustered Figure', key='_FIG_OPEN3_', disabled=True, size=(20, 1)),
           sg.Button('Show Cluster Averages', key='_FIG_OPEN4_', disabled=True, size=(20, 1))],
          [sg.ColorChooserButton('Pick Color', key='color')],
          [sg.Input(key='-DIR_RES-', enable_events=True, visible=False),
           sg.FileSaveAs("Save Result As", target='-DIR_RES-', size=(15, 1)),
           sg.Button('Save', button_color=('white', 'green'), size=(10, 1), key='_SAVERES_', disabled=True)],
          [sg.Text('                             ', size=(20, 1)), ],
          [sg.Text('                             ', size=(20, 1)), ],
          [sg.Text('                             ', size=(20, 1)), ],
          [sg.Button('Exit')], ]

main_window = sg.Window('EZ PCA KMeans Processor', layout, grab_anywhere=False, size=(500, 530),
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
    if event == '-THREAD-' and values['-THREAD-'] == "** DONE **":
        save_handl = True
        main_window['_PCA1_'].update(disabled=False)
        main_window['_PCA2_'].update(disabled=False)
    if event == '-THREAD-' and values['-THREAD-'] == "Error 1":
        sg.popup_ok('Invalid File!', font=headFont)
    if event == '_PCA1_':
        pca1_fig = pca_i(new_csv)
        pca1_fig.show()
    if event == '_PCA2_':
        scores = pca_f(new_csv, values['_NCOM_'])
        main_window['_FIG_OPEN2_'].update(disabled=False)
        main_window['_FIG_OPEN1_'].update(disabled=True)
        main_window['-KMEANS-'].update(disabled=False)
        main_window['-KGRAPH-'].update(disabled=False)
    if event == '-KGRAPH-':
        kgraph_fig = kgraph_(scores)
        kgraph_fig.show()
    if event == '-KMEANS-':
        res_, clc_ = kmeans_(values['_KVAL_'], scores)
        result_csv = res_vbose(new_csv, res_)
        main_window['_SAVECSV_'].update(disabled=False)
        main_window['_FIG_OPEN3_'].update(disabled=False)
        main_window['_FIG_OPEN4_'].update(disabled=False)
    if event == '_FIG_OPEN3_':
        km_fig = gen_map(new_csv, res_, ['gray', 'blue', 'green', 'pink'], 100)
        km_fig.show()
    if event == '_FIG_OPEN4_':
        cl_avg = clavg_fig(result_csv, values['_KVAL_'], 100)
        cl_avg.show()
    if event == '_SAVECSV_':
        new_csv.to_csv(values['_PCSV_'], index=False)
    if event == '_SAVERES_':
        result_csv.to_csv(values['_PCSV_'], index=False)

    if event == '_FIG_OPEN1_':
        pca1_fig.show()
        # show_fig(pca1_fig)
    # if event == '_FIG_OPEN2_':
    #   pca2_fig.show()
    #   show_fig(pca2_fig)

    # In older code you'll find it written using FindElement or Element
    # window.FindElement('-OUTPUT-').Update(values['-IN-'])
    # A shortened version of this update can be written without the ".Update"
    # window['-OUTPUT-'](values['-IN-'])
