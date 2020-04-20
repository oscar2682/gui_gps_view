"""
GUI para graficar series de tiempo de datos GPS
Oscar Castro Artola, Instituto de Geofisica, marzo 2015
"""

from PyQt5.QtGui import *
from PyQt5.QtWidgets import QDialog
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QGridLayout,QLabel,QGroupBox
from PyQt5.QtWidgets import QComboBox,QPushButton
from PyQt5.QtWidgets import QVBoxLayout,QLineEdit,QCheckBox,QHBoxLayout
from PyQt5.QtWidgets import QFileDialog
import matplotlib.pyplot as plt
#from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
#from matplotlib.backends.backend_qt4agg import NavigationToolbar2QTAgg as NavigationToolbar
from funcs_gps_gui import plot_one, plot_three

class MainWindow(QDialog):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setWindowTitle(self.tr("GPS PLOTER GUI"))

        # a figure instance to plot on
#        self.figure = plt.figure()
#        self.canvas = FigureCanvas(self.figure)
#        self.toolbar = NavigationToolbar(self.canvas, self)

        # LAYOUT
#        vbox = QVBoxLayout(self)
        grid = QGridLayout()
        self.setLayout(grid)
        
        # WIDGETS
        self.bot_one_comp = QPushButton("Plot one component")
        self.bot_three_comp = QPushButton("Plot three componentes")
        self.combo_1 = QComboBox()
        lista = ['vladi', 'sara' ,'cabral']
        for item in lista:
            self.combo_1.addItem(item)
        self.linea_estacion = QLineEdit()
        self.salirB = QPushButton("Salir")
        label_sta = QLabel("Station to plot three components: ", self)
        label_format = QLabel("Select data format: ", self)
        

        # ADD WIDGETS
#        grid.addWidget(self.canvas,1,0,10,1)
        grid.addWidget(self.bot_one_comp,1,1)
        grid.addWidget(self.bot_three_comp,1,2)
        grid.addWidget(label_sta,2,2)
        grid.addWidget(self.linea_estacion,2,3)
        grid.addWidget(self.combo_1,4,1)
        grid.addWidget(label_format,3,1)
        grid.addWidget(self.salirB,4,4)

        # CONECTIONS
        self.bot_one_comp.clicked.connect(self.una_componente)
        self.bot_three_comp.clicked.connect(self.tres_componentes)
        self.combo_1.currentIndexChanged.connect(lambda: self.combo_1.currentText())
        self.linea_estacion.textChanged.connect(lambda: self.linea_estacion.text())
        self.salirB.clicked.connect(self.close)

        # FUNCTIONS
    def una_componente(self):
        formato = str(self.combo_1.currentText())
        if formato == 'vladi':
            one_file = QFileDialog.getOpenFileName(self,"Abrir archivo",
            "/home/oscar/Doctorado/GPS/programas/python/datos_vladi")
        elif formato == 'sara':
            one_file = QFileDialog.getOpenFileName(self,"Abrir archivo",
            "/home/oscar/Doctorado/GPS/programas/python/datos_sara")
        elif formato == 'cabral':
            one_file = QFileDialog.getOpenFileName(self,"Abrir archivo",
            "/home/oscar/Doctorado/GPS/programas/python/datos_enrique_cabral")
        plot_one(one_file, formato)

    def tres_componentes(self):
        formato = str(self.combo_1.currentText())
        estacion = str(self.linea_estacion.text())
        plot_three(estacion, formato)

if __name__ == "__main__":
    import sys
    app = QApplication([])
    w = MainWindow()
    w.show()
    sys.exit(app.exec_())
