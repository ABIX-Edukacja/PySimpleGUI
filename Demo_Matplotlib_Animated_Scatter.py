from random import randint
import PySimpleGUI as sg
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, FigureCanvasAgg
from matplotlib.figure import Figure
import matplotlib.backends.tkagg as tkagg
import tkinter as tk


def main():
    canvas_elem = sg.Canvas(size=(640, 480))  # get the canvas we'll be drawing on
    # define the form layout
    layout = [[sg.Text('Animated Matplotlib', size=(40, 1), justification='center', font='Helvetica 20')],
              [canvas_elem],
              [sg.ReadFormButton('Exit', size=(10, 2), pad=((280, 0), 3), font='Helvetica 14')]]

    # create the form and show it without the plot
    form = sg.FlexForm('Demo Application - Embedding Matplotlib In PySimpleGUI')
    form.Layout(layout)
    form.ReadNonBlocking()

    canvas = canvas_elem.TKCanvas

    while True:
        button, values = form.ReadNonBlocking()
        if button is 'Exit' or values is None:
            exit(69)

        def PyplotScatterWithLegend():
            import matplotlib.pyplot as plt
            from numpy.random import rand

            fig, ax = plt.subplots()
            for color in ['red', 'green', 'blue']:
                n = 750
                x, y = rand(2, n)
                scale = 200.0 * rand(n)
                ax.scatter(x, y, c=color, s=scale, label=color,
                           alpha=0.3, edgecolors='none')

            ax.legend()
            ax.grid(True)
            return fig

        fig = PyplotScatterWithLegend()

        figure_x, figure_y, figure_w, figure_h = fig.bbox.bounds
        figure_w, figure_h = int(figure_w), int(figure_h)
        photo = tk.PhotoImage(master=canvas, width=figure_w, height=figure_h)

        canvas.create_image(640/2, 480/2, image=photo)

        figure_canvas_agg = FigureCanvasAgg(fig)
        figure_canvas_agg.draw()

        # Unfortunately, there's no accessor for the pointer to the native renderer
        tkagg.blit(photo, figure_canvas_agg.get_renderer()._renderer, colormode=2)

        # time.sleep(.1)


if __name__ == '__main__':
    main()
