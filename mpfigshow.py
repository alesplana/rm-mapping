import PySimpleGUI as sg
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib


def show_fig(fig):
    sg.theme('SystemDefault')
    matplotlib.use('TkAgg')

    def draw_figure(canvas, figure):
        figure_canvas_agg = FigureCanvasTkAgg(figure, canvas)
        figure_canvas_agg.draw()
        figure_canvas_agg.get_tk_widget().pack(side='top', fill='both', expand=1)
        return figure_canvas_agg

    plot_win = [[sg.Canvas(key='-CANVAS-')],
              [sg.Button('Ok', key='_AOK_')]]

    # create the form and show it without the plot
    fig_window = sg.Window('Figure', plot_win, finalize=True, element_justification='center', font='Helvetica 18')

    # add the plot to the window
    fig_canvas_agg = draw_figure(fig_window['-CANVAS-'].TKCanvas, fig)

    while True:
        event, values = fig_window.read()
        if event == sg.WIN_CLOSED:
            break
        if event == '_AOK_':
            fig_window.close()