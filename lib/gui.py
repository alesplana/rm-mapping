# last edited: 04/01/2021

import PySimpleGUI as sg
import os
import threading
import random
from pathlib import Path
from lib import convert_csv
from lib import pca_initial_ as pca_i
from lib import pca_final_ as pca_f
from lib import cluster_variance as kgraph_
from lib import kmeans_
from lib import gen_map
from lib import res_vbose
from lib import clavg_fig

colors = []
err_win1 = 0
new_csv = []
sg.theme('SystemDefault')
sg.SetOptions(element_padding=(1, 1))

headFont = ('Helvetica', 15, 'bold')
head2Font = ('Helvetica', 12)

sg.set_options(font=('Helvetica', 11))


def open_and_convert(window, loc):  # worker thread convert csv
    # global new_csv
    globals()['new_csv'], stat = convert_csv(loc)
    if stat == 0:
        window.write_event_value('-THREAD-', "** DONE **")
    elif stat == 1:
        window.write_event_value('-THREAD-', "Error 1")
        print('Invalid File')


def color_picker(k):
    # global colors, err_win1
    layout = [[sg.Text('Color Picker for ' + str(k) + ' cluster/s:', size=(20, 1))]]

    for i in range(k):
        layout.append([sg.Text('Cluster ' + str(i) + ': ', size=(8, 1)),
                       sg.Input(visible=True, enable_events=True, key='color' + str(i), size=(8, 1), readonly=True),
                       sg.Text(' '),
                       sg.ColorChooserButton('Pick Color', target='color' + str(i))])

    layout.append([sg.Ok(), sg.Cancel()])

    window = sg.Window('Color Picker', layout, grab_anywhere=False, size=(220, 80 + (k * 20)),
                       return_keyboard_events=False,
                       finalize=True,
                       modal=True)

    while True:
        event, values = window.read()
        print(event, values)
        if event in ('Exit', sg.WIN_CLOSED, 'Cancel'):
            globals()['err_win1'] = 1
            break
        if event == 'Ok':
            globals()['colors'] = list(values.values())
            if globals()['colors'].count('') > 0:
                sg.Popup('Please pick all colors!', title='Error!')
            elif globals()['colors'].count('') == 0:
                print(globals()['colors'])
                globals()['err_win1'] = 0
                break

    window.close()


def main_process():
    layout = [[sg.Text('STEP 1: File processing', font=headFont)],
              [sg.Text('Select file for processing', font=head2Font, size=(30, 2))],
              [sg.In(visible=False),
               sg.Input(key='-DIR-', enable_events=True, visible=False),
               sg.Text('                             ', key='-FILENAME-', size=(20, 1)),
               sg.FileBrowse('Browse', target='-DIR-', size=(10, 1),
                             file_types=(("Text Files", "*.txt"), ("CSV Files", "*.csv"))),
               sg.Button('Open', button_color=('white', 'red'), size=(8, 1), key='_OPEN_', disabled=True)],
              [sg.In(visible=False),
               sg.Input(key='_PCSV_', enable_events=True, visible=False),
               sg.Text('                             ', key='-FN_2-', size=(20, 1)),
               sg.FileSaveAs("Save File As", target='_PCSV_', size=(20, 1),
                             button_color=('white', 'green'), disabled=True, key='-PCSV-'),
               sg.Button('Save', button_color=('white', 'green'), size=(10, 1), key='_SAVECSV_', visible=False)],
              [sg.Text('_' * 100, justification='center', text_color='gray', size=(100, 2))],  # horizontal separator
              [sg.Text('STEP 2: Run Principal Component Analysis', font=headFont)],
              [sg.Text('Initial PCA Run (20 components)', font=head2Font, size=(25, 1)),
               sg.Button('Open Scree Plot', button_color=('white', '#e7b416'), key='_PCA1_', size=(23, 1),
                         disabled=True),
               sg.Button('Open Scree Plot', key='_FIG_OPEN1_', disabled=True, size=(15, 1), visible=False)],
              [sg.Text('Number of Principal Components:', font=head2Font, size=(25, 1)),
               sg.Combo(list(range(2, 21)), size=(5, 2), key='_NCOM_', enable_events=True),
               sg.Button('Run PCA', button_color=('white', 'green'), key='_PCA2_', size=(15, 1), disabled=True),
               sg.Button('Open Fig', key='_FIG_OPEN2_', disabled=True, size=(10, 1), visible=False)],
              [sg.Text('_' * 100, justification='center', text_color='gray', size=(100, 2))],  # horizontal separator
              [sg.Text('STEP 3: Cluster using K-Means', font=headFont)],
              [sg.Text('Identify the optimal value for k using the total distance vs k value graph.')],
              [sg.Button('Show Graph', key='-KGRAPH-', size=(15, 1), disabled=True, button_color=('white', 'green'))],
              [sg.Text('                             ', size=(20, 1)), ],
              [sg.Text('K-Value:', font=head2Font, size=(7, 1)),
               sg.Combo(list(range(1, 11)), size=(6, 2), key='_KVAL_', enable_events=True),
               sg.Text(' '),
               sg.Button('Pick Colors', key='-COLORS-')],
              [sg.Button('Run K-Means', key='-KMEANS-', size=(15, 1), disabled=True, button_color=('white', 'green')),
               sg.Button('Open Clustered Figure', key='_FIG_OPEN3_', disabled=True, size=(20, 1)),
               sg.Button('Show Cluster Averages', key='_FIG_OPEN4_', disabled=True, size=(20, 1))],
              # [sg.ColorChooserButton('Pick Color', key='color')],
              [sg.Input(key='-DIR_RES-', enable_events=True, visible=False),
               sg.Button('Save Result', button_color=('white', 'green'), size=(15, 1), key='_SAVERES_', disabled=True)],
              [sg.Text('                             ', size=(20, 1)), ],
              [sg.Text('                             ', size=(20, 1)), ],
              [sg.Text('                             ', size=(20, 1)), ],
              [sg.Button('Exit')], ]

    main_window = sg.Window('EZ PCA KMeans Processor', layout, grab_anywhere=False, size=(500, 530),
                            return_keyboard_events=True,
                            finalize=True)

    main_window['_SAVECSV_'].update(disabled=True)
    save_handl = False

    reset = 0
    globals()['colors'] = []
    thread_run = 0

    while True:
        event, values = main_window.read()
        file_path = Path(values['-DIR-']).expanduser().resolve()
        fn_1 = os.path.basename(values['-DIR-'])
        fn_2 = os.path.basename(values['_PCSV_'])
        # print(event, values)
        main_window.element('-FILENAME-').Update(fn_1)
        main_window.element('-FN_2-').Update(fn_2)

        if save_handl and not fn_2 == '':
            main_window['_SAVECSV_'].update(disabled=False)
        if not fn_1 == '':
            main_window['_OPEN_'].update(disabled=False)
        # window event handling
        if event in (sg.WIN_CLOSED, 'Exit'):
            break
        if event == '-DIR-':
            reset = 1
        if event == '_OPEN_':
            reset = 1
            values['-THREAD-'] = '** WAIT **'
            thread_run = 1
            threading.Thread(target=open_and_convert, args=(main_window, values['-DIR-']), daemon=True).start()
        if event == '-THREAD-' and values['-THREAD-'] == "** DONE **":
            reset = 0
            thread_run = 0
            save_handl = True
            main_window['-PCSV-'].update(disabled=False)
            main_window['_PCA1_'].update(disabled=False)
            main_window['_PCA2_'].update(disabled=False)
        if event == '-THREAD-' and values['-THREAD-'] == "Error 1":
            reset = 0
            thread_run = 0
            sg.popup_ok('Invalid File!', font=headFont)
        if event == '_PCA1_':
            pca1_fig = pca_i(globals()['new_csv'])
            pca1_fig.show()
        if event == '_PCA2_':
            try:
                scores = pca_f(globals()['new_csv'], values['_NCOM_'])
                main_window['_FIG_OPEN2_'].update(disabled=False)
                main_window['_FIG_OPEN1_'].update(disabled=True)
                main_window['-KMEANS-'].update(disabled=False)
                main_window['-KGRAPH-'].update(disabled=False)
            except TypeError:
                sg.PopupOK('Specify number of principal components!', title='PCA error')
        if event == '_KVAL_':
            globals()['colors'] = ''
        if event == '-KGRAPH-':
            kgraph_fig = kgraph_(scores)
            kgraph_fig.show()
        if event == '-KMEANS-':
            try:
                res_, clc_, dist = kmeans_(values['_KVAL_'], scores)
                res = res_.join(dist)
                print('Cluster Centers: ' + str(clc_))
                result_csv_ = res_vbose(globals()['new_csv'], res)
                result_csv = res_vbose(globals()['new_csv'], res_)
                main_window['_SAVERES_'].update(disabled=False)
                main_window['_FIG_OPEN3_'].update(disabled=False)
                main_window['_FIG_OPEN4_'].update(disabled=False)
            except TypeError:
                sg.PopupOK('Set number of clusters!', title='K-Means error')
        if event == '-COLORS-':
            try:
                color_picker(values['_KVAL_'])
            except TypeError:
                sg.PopupOK('Specify number of clusters!', title='Error!')
        if event == '_FIG_OPEN3_':
            if globals()['colors'].count('') > 0 or globals()['colors'] == [] or globals()['colors'].count('None') > 0:
                sg.PopupOK('No color set. Click Pick Color button first!', title='No Colors Passed')
            else:
                km_fig = gen_map(globals()['new_csv'], res_, globals()['colors'], 100)
                km_fig.show()
                km_fig.savefig(file_path.with_suffix('.map-k' + str(values['_KVAL_']) + '.svg'), transparent=True)
                km_fig.savefig(file_path.with_suffix('.map-k' + str(values['_KVAL_']) + '-transparent.png'), transparent=True)
        if event == '_FIG_OPEN4_':
            if globals()['colors'].count('') > 0 or globals()['colors'] == [] or globals()['colors'].count(None) > 0:
                color_temp = []
                for i in range(values['_KVAL_']):
                    color = '#{:02x}{:02x}{:02x}'.format(random.randint(0,255), random.randint(0,255), random.randint(0,255))
                    color_temp.append(color)
                cl_avg = clavg_fig(result_csv, values['_KVAL_'], color_temp, 50)
            else:
                cl_avg = clavg_fig(result_csv, values['_KVAL_'], globals()['colors'], 100)
            cl_avg.show()
            cl_avg.savefig(file_path.with_suffix('.map-k' + str(values['_KVAL_']) + '-avg.svg'))
        if event == '_PCSV_' and not values['_PCSV_'] in ('', None):
            globals()['new_csv'].to_csv(values['_PCSV_'], index=False)
        if event == '_SAVERES_':
            result_csv_.to_csv(file_path.with_suffix('.map-k' + str(values['_KVAL_']) + '.csv'), index=False)
        if event == '_FIG_OPEN1_':
            pca1_fig.show()

        if reset == 1:  # window reset
            main_window['-PCSV-'].update(disabled=True)
            main_window['_PCA1_'].update(disabled=True)
            main_window['_PCA2_'].update(disabled=True)
            main_window['-KMEANS-'].update(disabled=True)
            main_window['-KGRAPH-'].update(disabled=True)
            main_window['_FIG_OPEN3_'].update(disabled=True)
            main_window['_FIG_OPEN4_'].update(disabled=True)
        if thread_run == 1:
            sg.PopupAnimated(sg.DEFAULT_BASE64_LOADING_GIF, background_color='white', time_between_frames=1)
        elif thread_run == 0:
            sg.PopupAnimated(None)

    main_window.close()


if __name__ == "__main__":
    main_process()
