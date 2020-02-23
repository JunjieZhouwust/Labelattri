import sys, math
from PyQt5.QtWidgets import (QApplication, QMainWindow, QPushButton,
                             QLabel, QWidget, QHBoxLayout, QVBoxLayout,
                             QListWidget, QFileDialog, QGroupBox,
                             QRadioButton)
from PyQt5.QtGui import QIcon, QPixmap, QImage , QPainter,QBrush, QPen, QFont, QPalette, QColor
from PyQt5.QtCore import Qt, QRect, QPoint, QTimer, QObject
from cv2 import imread, resize, cvtColor, COLOR_BGR2RGB
from Libs.data import *
from Libs.util import *
import os

label_item_len=11
statue = [False for i in range(label_item_len)]


class human_attrition_ui(QWidget):
    def __init__(self, parent=None):
        super(human_attrition_ui, self).__init__(parent)
        self.face_attri = ["Blackhair", "Blury", "Eyeglass", "Male", "Smile", "Younge"]
        self.huamn_attri = ["gender", "hat", "backpack", "bag", "age"]
        self.sum_attribute = self.face_attri + self.huamn_attri
        self.huamn_attri_buttons = []
        self.label_item_len = len(self.face_attri) + len(self.huamn_attri)

        self.initUI()

    def initUI(self):
        self.face_layput = QVBoxLayout()

        palette = QPalette()
        palette.setColor(QPalette.WindowText, QColor(128, 0, 0))
        face = QLabel("Face Attribute:")
        face.setFont(QFont("Face", 10, QFont.Bold))
        face.setPalette(palette)

        human = QLabel("Body Attribute")
        human.setFont(QFont("Face", 10, QFont.Bold))
        human.setPalette(palette)

        self.face_layput.addWidget(face)

        for i in self.face_attri:
            group = QGroupBox()
            # group.setTitle(i)
            flayer = QHBoxLayout(group)
            button1 = QRadioButton('1')
            button2 = QRadioButton('2')
            button1.setChecked(True)

            button1.setObjectName("{}_1".format(i))
            button2.setObjectName("{}_2".format(i))
            button1.toggled.connect(self.toogle_deal)
            button2.toggled.connect(self.toogle_deal)

            flayer.addWidget(QLabel(i))
            flayer.addStretch()
            flayer.addWidget(button1)
            flayer.addWidget(button2)
            flayer.setAlignment(Qt.AlignRight)
            self.face_layput.addWidget(group)

            self.huamn_attri_buttons.append(button1)
            self.huamn_attri_buttons.append(button2)

        self.huamn_layput = QVBoxLayout()
        self.huamn_layput.addWidget(human)

        for j in self.huamn_attri:
            group = QGroupBox()
            # group.setTitle(j)
            hlayer = QHBoxLayout(group)
            hbutton1 = QRadioButton('1')
            hbutton2 = QRadioButton('2')
            hbutton1.setChecked(True)

            hbutton1.setObjectName("{}_1".format(j))
            hbutton2.setObjectName("{}_2".format(j))

            hbutton1.toggled.connect(self.toogle_deal)
            hbutton2.toggled.connect(self.toogle_deal)

            hlayer.addWidget(QLabel(j))
            hlayer.addStretch()
            hlayer.addWidget(hbutton1)
            hlayer.addWidget(hbutton2)
            hlayer.setAlignment(Qt.AlignRight)
            self.huamn_layput.addWidget(group)

            self.huamn_attri_buttons.append(hbutton1)
            self.huamn_attri_buttons.append(hbutton2)

        self.mainlayout = QVBoxLayout(self)

        self.mainlayout.addLayout(self.face_layput)
        self.mainlayout.addSpacing(30)
        self.mainlayout.addLayout(self.huamn_layput)

        timer = QTimer(self)
        timer.setInterval(20)
        timer.timeout.connect(self.timerEven)
        timer.start(20)

    def timerEven(self):
        self.updates()

    def updates(self):
        for i in range(label_item_len):
            if statue[i] == False:
                self.huamn_attri_buttons[i * 2].setChecked(True)
            else:
                self.huamn_attri_buttons[i * 2+1].setChecked(True)


    def toogle_deal(self):
        sender, num = self.sender().objectName().split('_')

        if num == '1':
            index = self.sum_attribute.index(sender)
            if self.huamn_attri_buttons[index*2].isChecked() == True:
                statue[index] = False
            else:
                statue[index] = True


class Labelattr(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.points = [QPoint(0, 0)]
        self.coordinates = []
        self.attri = []
        self.clickbox = 0
        self.initUI()

    def change_coordinate_display(self, coor):
        self.coordinates.clear()
        self.attri.clear()
        self.img_size = coor['size']
        self.widget_size = self.size()
        for instance in coor['coor']:
            instance_coor = []
            for box in instance:
                xmin = box[0] * (self.widget_size.width() / self.img_size[0])
                ymin = box[1] * (self.widget_size.height() / self.img_size[1])
                xmax = box[2] * (self.widget_size.width() / self.img_size[0])
                ymax = box[3] * (self.widget_size.height() / self.img_size[1])
                instance_coor.append((QPoint(xmin, ymin), QPoint(xmax, ymax)))
            self.coordinates.append((instance_coor[0], instance_coor[1]))
            self.attri.append([False for i in range(11)])
        self.update()

    def initUI(self):
        self.setMinimumSize(1000, 800)
        self.img = QImage(cvtColor(resize(imread("./icons/logo.jpg"), (1000, 800)), COLOR_BGR2RGB), 1000, 800, QImage.Format_RGB888)
        self.counter=0

    def update_display(self, filename):
        self.img = QImage(cvtColor(resize(imread(filename), (1000, 800)), COLOR_BGR2RGB), 1000, 800, QImage.Format_RGB888)
        self.update()

    def timer_event(self):
        # self.show()
        self.counter = self.counter+1


    def paintEvent(self, event):

        qp = QPainter()
        qp.begin(self)
        self.drawPoints(qp)
        qp.end()


    def drawPoints(self, qp):
        color = [Qt.red, Qt.green, Qt.blue, Qt.yellow]
        qp.drawImage(QRect(0, 0, 1000, 800), self.img)

        qp.setBrush(QBrush(Qt.black, Qt.BDiagPattern))

        for item1, coordinate in enumerate(self.coordinates):
            qp.setPen(color[item1%4])
            for item2, coor in enumerate(coordinate):
                qp.drawRect(QRect(coor[0], coor[1]))

        if len(self.coordinates) >=1:
            for coor in self.coordinates[self.clickbox]:
                qp.setPen(color[self.clickbox % 4])
                qp.setBrush(QBrush(Qt.green, Qt.BDiagPattern))
                qp.drawRect(QRect(coor[0], coor[1]))

        if len(self.points) % 2 == 0:
            qp.drawRect(QRect(self.points[-1], self.points[0]))

    def mousePressEvent(self, mousePress_even):
        pos = mousePress_even.pos()
        candidate = []
        global statue

        self.attri[self.clickbox] = statue
        for item1, coordinate in enumerate(self.coordinates):
            if coordinate[1][0].x() < pos.x() and coordinate[1][0].y() < pos.y() and \
                     coordinate[1][1].x()>pos.x() and coordinate[1][1].y()>pos.y():
                candidate.append(item1)
                break
        if len(candidate) == 0:
            return

        self.clickbox = candidate[0]
        statue = self.attri[self.clickbox]
        print(statue)
        print()
        self.update()


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.cwd = os.getcwd()
        self.Image_list = []
        self.saveDirectory = "./Annotations"


    def Label_load_xml(self, filename):
        self.display.update_display(filename)
        label = Label_get_instance(os.path.splitext(filename)[0]+'.xml')
        faces = []
        bodys_t = []
        bodys = []
        for instance in label['instance']:
            if instance['name'] == 'head':
                faces.append(instance['bndbox'])
            elif instance['name'] == 'human':
                bodys_t.append(instance['bndbox'])
            else:
                print("label type unknow")
                exit()
        for item, face in enumerate(faces):
            for body_t in bodys_t:
                if compute_iou(face, body_t)>0.85 and abs(body_t[1]- face[1]) < 50:
                    bodys.append(body_t)
                    break
        self.coor = list(zip(faces, bodys))

        self.display.change_coordinate_display({"size":label['size'], "coor":self.coor})

    def Label_save_xml(self):
        attri = self.display.attri
        box = self.display.coordinates
        size =self.display.img_size

        imgpath = os.path.join(self.ImagefilesDirectort, self.filelistwidget.currentItem().text())
        instances = zip(self.coor, attri)
        save_dir = os.path.join(self.saveDirectory, self.filelistwidget.currentItem().text().split('.')[0]+'.xml')
        Label_write_instance(imgpath, size, instances, save_dir)


    def initUI(self):
        openbutton = QPushButton("Open", )
        openbutton.setIcon(QIcon("icons/open.png"))
        openbutton.setMinimumSize(80, 80)

        opendbutton = QPushButton("Open Dir")
        opendbutton.setIcon(QIcon("icons/open.png"))
        opendbutton.setMinimumSize(80, 80)

        savebutton = QPushButton("Save")
        savebutton.setIcon(QIcon("icons/save.png"))
        savebutton.setMinimumSize(80, 80)

        saveasbutton = QPushButton("Save as")
        saveasbutton.setIcon(QIcon("icons/save.png"))
        saveasbutton.setMinimumSize(80, 80)

        nextbutton = QPushButton("next")
        nextbutton.setIcon(QIcon("icons/next.png"))
        nextbutton.setMinimumSize(80, 80)

        prebutton = QPushButton("pre")
        prebutton.setIcon(QIcon("icons/prev.png"))
        prebutton.setMinimumSize(80, 80)

        openbutton.clicked.connect(self.MessageClicked)
        opendbutton.clicked.connect(self.MessageClicked)
        savebutton.clicked.connect(self.MessageClicked)
        nextbutton.clicked.connect(self.MessageClicked)
        prebutton.clicked.connect(self.MessageClicked)

        toolhbox = QVBoxLayout()
        toolhbox.addWidget(openbutton)
        toolhbox.addWidget(opendbutton)
        toolhbox.addWidget(savebutton)
        toolhbox.addWidget(saveasbutton)

        toolhbox.addWidget(nextbutton)
        toolhbox.addWidget(prebutton)


        mydraw = QVBoxLayout()
        self.display = Labelattr()
        mydraw.addWidget(self.display)
        self.filelistwidget = QListWidget()
        self.filelistwidget.doubleClicked.connect(self.list_doubleclick)

        self.myradio = human_attrition_ui()

        mainlayout = QHBoxLayout(self)

        mainlayout.addLayout(toolhbox)
        mainlayout.addLayout(mydraw)
        mainlayout.addWidget(self.myradio)
        mainlayout.addWidget(self.filelistwidget)

        self.setLayout(mainlayout)

        # self.setGeometry(200, 200, 1000, 800)
        self.setWindowTitle("Labelattri")
        self.setWindowIcon(QIcon("./icons/huaji.png"))



# 消息框处理队列
    def MessageClicked(self, event):
        sender = self.sender()
        message_type = sender.text()
        Support_image_format = ["bmp","jpg", "jpeg", "png", "tif"]
        if message_type == "Open":
            filename, filetype = QFileDialog.getOpenFileName(self,
                                        "Image file",
                                        self.cwd,
                                        "Image Files(*.bmp *.jpg *.jpeg *.png *.tif)"
                                        )
            # self.display.update_display(filename)

        elif message_type == "Open Dir":
            self.ImagefilesDirectort = QFileDialog.getExistingDirectory(self,
                                             "Image files",
                                             self.cwd
                                             )
            self.Image_list.clear()
            self.filelistwidget.clear()
            for file in os.listdir(self.ImagefilesDirectort):
                if file.split('.')[-1] in Support_image_format:
                    self.Image_list.append(file)
                    self.filelistwidget.addItem(file)
            self.Label_load_xml(os.path.join(self.ImagefilesDirectort, self.Image_list[0]))

        elif message_type == "Save":
            # self.saveDirectory = QFileDialog.getSaveFileName(self,
            #                                             'Save as',
            #                                             self.cwd,
            #                                             "Label Files(*.txt *.json *.xml )"
            #
            #                                             )
            self.Label_save_xml()
        elif message_type == "Save as":
            self.saveDirectory = QFileDialog.getSaveFileName(self,
                                        'Save as',
                                        self.cwd,
                                        "Label Files(*.txt *.json *.xml )"
                                        )
        elif message_type == "next":
            self.Label_load_xml(os.path.join(self.ImagefilesDirectort, self.Image_list[0]))

        # elif message_type == "pre":


    def list_doubleclick(self):
        self.Label_load_xml(os.path.join(self.ImagefilesDirectort, self.filelistwidget.currentItem().text()))


if __name__ == "__main__":
    app = QApplication(sys.argv)
    labeltool = MainWindow()
    labeltool.show()
    # print(labeltool.size())
    sys.exit(app.exec_())

# ui转py
# 1
#  python -m PyQt5.uic.pyuic demo.ui -o demo.py




