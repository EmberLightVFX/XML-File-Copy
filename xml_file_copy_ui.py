# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'xml_file_copy_ui.ui'
##
## Created by: Qt User Interface Compiler version 5.15.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################
from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *
            
class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(786, 549)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.centralwidget.setEnabled(True)
        sizePolicy = QSizePolicy(QSizePolicy.Maximum, QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.centralwidget.sizePolicy().hasHeightForWidth())
        self.centralwidget.setSizePolicy(sizePolicy)
        self.verticalLayout_2 = QVBoxLayout(self.centralwidget)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.horizontalLayout_5 = QHBoxLayout()
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.rb_filecopy = QRadioButton(self.centralwidget)
        self.rb_filecopy.setObjectName(u"rb_filecopy")
        self.rb_filecopy.setChecked(True)

        self.horizontalLayout_5.addWidget(self.rb_filecopy)

        self.rb_resilio = QRadioButton(self.centralwidget)
        self.rb_resilio.setObjectName(u"rb_resilio")

        self.horizontalLayout_5.addWidget(self.rb_resilio)

        self.horizontalSpacer_3 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_5.addItem(self.horizontalSpacer_3)


        self.verticalLayout_2.addLayout(self.horizontalLayout_5)

        self.gridLayout = QGridLayout()
        self.gridLayout.setObjectName(u"gridLayout")
        self.btn_xml = QPushButton(self.centralwidget)
        self.btn_xml.setObjectName(u"btn_xml")

        self.gridLayout.addWidget(self.btn_xml, 0, 3, 1, 1)

        self.lb_xml = QLabel(self.centralwidget)
        self.lb_xml.setObjectName(u"lb_xml")

        self.gridLayout.addWidget(self.lb_xml, 0, 0, 1, 1)

        self.path_xml = QLineEdit(self.centralwidget)
        self.path_xml.setObjectName(u"path_xml")

        self.gridLayout.addWidget(self.path_xml, 0, 2, 1, 1)

        self.lb_copy = QLabel(self.centralwidget)
        self.lb_copy.setObjectName(u"lb_copy")

        self.gridLayout.addWidget(self.lb_copy, 1, 0, 1, 1)

        self.path_copy = QLineEdit(self.centralwidget)
        self.path_copy.setObjectName(u"path_copy")

        self.gridLayout.addWidget(self.path_copy, 1, 2, 1, 1)

        self.btn_copy = QPushButton(self.centralwidget)
        self.btn_copy.setObjectName(u"btn_copy")

        self.gridLayout.addWidget(self.btn_copy, 1, 3, 1, 1)


        self.verticalLayout_2.addLayout(self.gridLayout)

        self.line = QFrame(self.centralwidget)
        self.line.setObjectName(u"line")
        self.line.setFrameShape(QFrame.HLine)
        self.line.setFrameShadow(QFrame.Sunken)

        self.verticalLayout_2.addWidget(self.line)

        self.gridLayout_2 = QGridLayout()
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.cb_external = QCheckBox(self.centralwidget)
        self.cb_external.setObjectName(u"cb_external")

        self.gridLayout_2.addWidget(self.cb_external, 1, 0, 1, 1)

        self.lb_root = QLabel(self.centralwidget)
        self.lb_root.setObjectName(u"lb_root")

        self.gridLayout_2.addWidget(self.lb_root, 4, 0, 1, 1)

        self.path_root = QLineEdit(self.centralwidget)
        self.path_root.setObjectName(u"path_root")
        self.path_root.setEnabled(True)

        self.gridLayout_2.addWidget(self.path_root, 4, 1, 1, 1)

        self.cb_clone = QCheckBox(self.centralwidget)
        self.cb_clone.setObjectName(u"cb_clone")

        self.gridLayout_2.addWidget(self.cb_clone, 5, 1, 1, 1)

        self.path_external = QLineEdit(self.centralwidget)
        self.path_external.setObjectName(u"path_external")

        self.gridLayout_2.addWidget(self.path_external, 1, 1, 1, 1)

        self.cb_subdirs = QCheckBox(self.centralwidget)
        self.cb_subdirs.setObjectName(u"cb_subdirs")
        self.cb_subdirs.setChecked(True)

        self.gridLayout_2.addWidget(self.cb_subdirs, 3, 1, 1, 1)

        self.btn_root = QPushButton(self.centralwidget)
        self.btn_root.setObjectName(u"btn_root")

        self.gridLayout_2.addWidget(self.btn_root, 4, 2, 1, 1)

        self.btn_external = QPushButton(self.centralwidget)
        self.btn_external.setObjectName(u"btn_external")

        self.gridLayout_2.addWidget(self.btn_external, 1, 2, 1, 1)


        self.verticalLayout_2.addLayout(self.gridLayout_2)

        self.tw_status = QTableWidget(self.centralwidget)
        if (self.tw_status.columnCount() < 5):
            self.tw_status.setColumnCount(5)
        __qtablewidgetitem = QTableWidgetItem()
        self.tw_status.setHorizontalHeaderItem(0, __qtablewidgetitem)
        __qtablewidgetitem1 = QTableWidgetItem()
        self.tw_status.setHorizontalHeaderItem(1, __qtablewidgetitem1)
        __qtablewidgetitem2 = QTableWidgetItem()
        self.tw_status.setHorizontalHeaderItem(2, __qtablewidgetitem2)
        __qtablewidgetitem3 = QTableWidgetItem()
        self.tw_status.setHorizontalHeaderItem(3, __qtablewidgetitem3)
        __qtablewidgetitem4 = QTableWidgetItem()
        self.tw_status.setHorizontalHeaderItem(4, __qtablewidgetitem4)
        self.tw_status.setObjectName(u"tw_status")
        self.tw_status.setAlternatingRowColors(True)
        self.tw_status.setSelectionMode(QAbstractItemView.SingleSelection)
        self.tw_status.setHorizontalScrollMode(QAbstractItemView.ScrollPerPixel)
        self.tw_status.setWordWrap(False)

        self.verticalLayout_2.addWidget(self.tw_status)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.cb_overwrite = QCheckBox(self.centralwidget)
        self.cb_overwrite.setObjectName(u"cb_overwrite")

        self.horizontalLayout.addWidget(self.cb_overwrite)

        self.cb_sequence = QCheckBox(self.centralwidget)
        self.cb_sequence.setObjectName(u"cb_sequence")

        self.horizontalLayout.addWidget(self.cb_sequence)

        self.le_sequence = QLineEdit(self.centralwidget)
        self.le_sequence.setObjectName(u"le_sequence")

        self.horizontalLayout.addWidget(self.le_sequence)


        self.verticalLayout_2.addLayout(self.horizontalLayout)

        self.pb_file = QProgressBar(self.centralwidget)
        self.pb_file.setObjectName(u"pb_file")
        self.pb_file.setValue(0)

        self.verticalLayout_2.addWidget(self.pb_file)

        self.pb_total = QProgressBar(self.centralwidget)
        self.pb_total.setObjectName(u"pb_total")
        self.pb_total.setValue(0)
        self.pb_total.setTextVisible(True)
        self.pb_total.setOrientation(Qt.Horizontal)
        self.pb_total.setInvertedAppearance(False)

        self.verticalLayout_2.addWidget(self.pb_total)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.lb_info = QLabel(self.centralwidget)
        self.lb_info.setObjectName(u"lb_info")

        self.horizontalLayout_3.addWidget(self.lb_info)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Fixed, QSizePolicy.Minimum)

        self.horizontalLayout_3.addItem(self.horizontalSpacer)

        self.lb_datarate = QLabel(self.centralwidget)
        self.lb_datarate.setObjectName(u"lb_datarate")

        self.horizontalLayout_3.addWidget(self.lb_datarate)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_3.addItem(self.horizontalSpacer_2)


        self.verticalLayout_2.addLayout(self.horizontalLayout_3)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.btn_check = QPushButton(self.centralwidget)
        self.btn_check.setObjectName(u"btn_check")

        self.horizontalLayout_2.addWidget(self.btn_check)

        self.btn_transfer = QPushButton(self.centralwidget)
        self.btn_transfer.setObjectName(u"btn_transfer")

        self.horizontalLayout_2.addWidget(self.btn_transfer)


        self.verticalLayout_2.addLayout(self.horizontalLayout_2)

        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"XML File Copy", None))
        self.rb_filecopy.setText(QCoreApplication.translate("MainWindow", u"File copy", None))
        self.rb_resilio.setText(QCoreApplication.translate("MainWindow", u"Resilio Selective Sync", None))
        self.btn_xml.setText(QCoreApplication.translate("MainWindow", u"Browse", None))
        self.lb_xml.setText(QCoreApplication.translate("MainWindow", u"XML", None))
        self.lb_copy.setText(QCoreApplication.translate("MainWindow", u"Copy to", None))
        self.btn_copy.setText(QCoreApplication.translate("MainWindow", u"Browse", None))
        self.cb_external.setText(QCoreApplication.translate("MainWindow", u"External path", None))
        self.lb_root.setText(QCoreApplication.translate("MainWindow", u"Root path", None))
        self.cb_clone.setText(QCoreApplication.translate("MainWindow", u"Clone tree-structure", None))
        self.cb_subdirs.setText(QCoreApplication.translate("MainWindow", u"Search subdirs", None))
        self.btn_root.setText(QCoreApplication.translate("MainWindow", u"Get from XML", None))
        self.btn_external.setText(QCoreApplication.translate("MainWindow", u"Browse", None))
        ___qtablewidgetitem = self.tw_status.horizontalHeaderItem(0)
        ___qtablewidgetitem.setText(QCoreApplication.translate("MainWindow", u"Status", None));
        ___qtablewidgetitem1 = self.tw_status.horizontalHeaderItem(1)
        ___qtablewidgetitem1.setText(QCoreApplication.translate("MainWindow", u"Found", None));
        ___qtablewidgetitem2 = self.tw_status.horizontalHeaderItem(2)
        ___qtablewidgetitem2.setText(QCoreApplication.translate("MainWindow", u"Copy From", None));
        ___qtablewidgetitem3 = self.tw_status.horizontalHeaderItem(3)
        ___qtablewidgetitem3.setText(QCoreApplication.translate("MainWindow", u"Copy To", None));
        ___qtablewidgetitem4 = self.tw_status.horizontalHeaderItem(4)
        ___qtablewidgetitem4.setText(QCoreApplication.translate("MainWindow", u"Extension", None));
        self.cb_overwrite.setText(QCoreApplication.translate("MainWindow", u"Overwrite existing files", None))
        self.cb_sequence.setText(QCoreApplication.translate("MainWindow", u"Transfer sequenced files", None))
        self.le_sequence.setPlaceholderText(QCoreApplication.translate("MainWindow", u"Enter extensions that uses sequences. Seperate using \",\" Eg: R3D, png, jpg", None))
        self.lb_info.setText(QCoreApplication.translate("MainWindow", u"0 out of 0 files copied", None))
        self.lb_datarate.setText(QCoreApplication.translate("MainWindow", u"Datarate", None))
        self.btn_check.setText(QCoreApplication.translate("MainWindow", u"Check Files", None))
        self.btn_transfer.setText(QCoreApplication.translate("MainWindow", u"Start Transfer", None))
    # retranslateUi

