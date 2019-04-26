from kivy.app import App
from kivy.uix.button import Button
from kivy.garden.graph import Graph, MeshLinePlot

class TestApp(App):
    def build(self):
        plot = MeshLinePlot(color=next(colors))
        graph = Graph(
            xlabel='Iteration',
            ylabel='Value',
            x_ticks_minor=1,
            x_ticks_major=5,
            y_ticks_major=1,
            y_grid_label=True,
            x_grid_label=True,
            padding=5,
            xlog=False,
            ylog=False,
            x_grid=True,
            y_grid=True,
            ymin=0,
            ymax=11,
            **graph_theme)
        return graph

TestApp().run()
