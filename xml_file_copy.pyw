import sys
import subprocess
import os
import os.path

import platform
import errno

osName = None  # nopep8
if platform.system() == 'Windows':  # nopep8
    osName = "win"
else:
    osName = "mac"

libdir = os.path.dirname(__file__)  # nopep8
sys.path.insert(0, os.path.join(libdir, "PythonLibs", osName))  # nopep8

if sys.version[0] == "3":   # nopep8
    import urllib.parse as urlparse
    import os.scandir as scandir
else:
    import urlparse
    from scandir import scandir

from PySide2.QtWidgets import *
from PySide2.QtGui import *
from PySide2.QtCore import *
from string import digits as sdigits
from xml.etree import ElementTree
from xml_file_copy_ui import Ui_MainWindow


class WorkerSignals(QObject):
    '''
    Defines the signals available from a running worker thread.

    Supported signals are:

    finished
        No data

    error
        `tuple` (exctype, value, traceback.format_exc() )

    result
        `object` data returned from processing, anything

    progress
        `int` indicating % progress

    '''
    finished = Signal()
    error = Signal(tuple)
    result = Signal(object)
    progress = Signal(int, object)


class Worker(QRunnable):
    '''
    Worker thread

    Inherits from QRunnable to handler worker thread setup, signals and wrap-up.

    :param callback: The function callback to run on this worker thread. Supplied args and
                     kwargs will be passed through to the runner.
    :type callback: function
    :param args: Arguments to pass to the callback function
    :param kwargs: Keywords to pass to the callback function

    '''

    def __init__(self, fn, *args, **kwargs):
        super(Worker, self).__init__()

        # Store constructor arguments (re-used for processing)
        self.fn = fn
        self.args = args
        self.kwargs = kwargs
        self.signals = WorkerSignals()

        # Add the callback to our kwargs
        self.kwargs['progress_callback'] = self.signals.progress

    @Slot()
    def run(self):
        '''
        Initialise the runner function with passed args, kwargs.
        '''

        # Retrieve args/kwargs here; and fire processing using them
        try:
            result = self.fn(*self.args, **self.kwargs)
        except:
            traceback.print_exc()
            exctype, value = sys.exc_info()[:2]
            self.signals.error.emit((exctype, value, traceback.format_exc()))
        else:
            # Return the result of the processing
            self.signals.result.emit(result)
        finally:
            self.signals.finished.emit()  # Done


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        self.threadpool = QThreadPool()
        # Set thread count to 1 so only one shot is synced
        self.threadpool.setMaxThreadCount(1)

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.auto_start_timer = QTimer()
        self.auto_start_timer.start(2000)
        self.amount_of_files = 0
        self.isTransfering = False
        self.cancelTransfer = False

        # TEMP #
        '''
        self.ui.path_xml.setText(
            "G:\\2019_004_Lost in the sky\\EDIT\\XML\\AKT03DEL01\\A03D01_S010.xml")
        self.ui.path_copy.setText("D:\\to")
        self.ui.path_external.setText(
            "G:\\2019_004_Lost in the sky\\Filmat material")
        # self.ui.path_root.setText("C:\\Users\\Ember\\Desktop\\from")
        '''
        # TEMP #

        # Data transfer variables
        self.ui.lb_datarate.setText("")
        self.sourceSize = 0
        self.destSize = 0
        self.METRIC_LABELS = ["B", "kB",
                              "MB", "GB", "TB", "PB", "EB", "ZB", "YB"]
        self.BINARY_LABELS = [
            "B", "KiB", "MiB", "GiB", "TiB", "PiB", "EiB", "ZiB", "YiB"]
        # PREDEFINED FOR SPEED.
        self.PRECISION_OFFSETS = [0.5, 0.05, 0.005, 0.0005]
        # PREDEFINED FOR SPEED.
        self.PRECISION_FORMATS = ["{}{:.0f} {}",
                                  "{}{:.1f} {}", "{}{:.2f} {}", "{}{:.3f} {}"]
        self.connectEvents()
        self.show()

    def __keyPressEvent(self, event):
        if event.matches(QKeySequence.Delete):
            self.__removeServer()
        elif event.matches(QKeySequence.Copy):
            clipboard = QApplication.clipboard()
            selected_cell = self.ui.tw_status.selectedItems()
            clipboard.setText(selected_cell[0].text())

    def __removeServer(self):
        self.ui.tw_status.removeRow(
            self.ui.tw_status.currentRow()
        )

    def connectEvents(self):
        self.ui.btn_xml.clicked.connect(
            lambda: self.browseXML(self.ui.path_xml))
        self.ui.btn_copy.clicked.connect(
            lambda: self.browsePath(self.ui.path_copy))

        self.ui.btn_external.clicked.connect(
            lambda: self.browsePath(self.ui.path_external,
                                    checkbox=self.ui.cb_external))
        self.ui.btn_root.clicked.connect(
            lambda: self.getBasePath(self.ui.path_root))

        self.ui.btn_check.clicked.connect(
            self.fileProcess)
        self.ui.btn_transfer.clicked.connect(
            self.startTransfer)
        self.ui.rb_filecopy.toggled.connect(self.radioSwitch)
        self.ui.tw_status.keyPressEvent = self.__keyPressEvent

    def radioSwitch(self):
        if self.ui.lb_copy.isEnabled() is True:
            self.ui.lb_copy.setEnabled(False)
            self.ui.path_copy.setEnabled(False)
            self.ui.btn_copy.setEnabled(False)

            self.ui.lb_root.setEnabled(False)
            self.ui.path_root.setEnabled(False)
            self.ui.btn_root.setEnabled(False)

            self.ui.cb_clone.setEnabled(False)
            self.ui.cb_overwrite.setEnabled(False)
        else:
            self.ui.lb_copy.setEnabled(True)
            self.ui.path_copy.setEnabled(True)
            self.ui.btn_copy.setEnabled(True)

            self.ui.lb_root.setEnabled(True)
            self.ui.path_root.setEnabled(True)
            self.ui.btn_root.setEnabled(True)

            self.ui.cb_clone.setEnabled(True)
            self.ui.cb_overwrite.setEnabled(True)

    def browseXML(self, textfield):
        fname = QFileDialog.getOpenFileName(self,
                                            'Pick XML File',
                                            textfield.text(),
                                            filter="XML files (*.xml)")
        if fname[0] != "":
            textfield.setText(os.path.abspath(fname[0]))

    def browsePath(self, textfield, checkbox=None):
        fname = QFileDialog.getExistingDirectory(self,
                                                 'Pick directory',
                                                 textfield.text(),
                                                 options=QFileDialog.ShowDirsOnly)
        if fname != "":
            textfield.setText(os.path.abspath(fname))
            if checkbox is not None:
                checkbox.setChecked(True)

    def getBasePath(self, textfield):
        files = self.fileProcess()
        if len(files) != 0:
            common_path = os.path.commonpath(files)
            if common_path != "":
                self.ui.cb_clone.setChecked(True)
                textfield.setText(os.path.abspath(common_path))

    def startTransfer(self):
        if self.ui.tw_status.rowCount() == 0:
            return

        if self.isTransfering is False:

            self.isTransfering = True
            self.ui.btn_transfer.setText("Cancel")

            self.totalProgress(0)
            self.ui.pb_file.setValue(0)
            self.sourceSize = 0
            self.destSize = 0

            worker = Worker(self.transfer)
            # Execute
            self.threadpool.start(worker)

            self.ui.pb_file.setValue(100)
            self.totalProgress(100)
            self.ui.lb_datarate.setText("")
            self.isTransfering = False
            self.cancelTransfer = False

            self.ui.btn_transfer.setText("Start Transfer")
        else:
            msg = QMessageBox(
                QMessageBox.Question,
                "XML File Copy",
                "Are you sure you want to cancel the transfer?"
            )
            msg.addButton("Yes", QMessageBox.YesRole)
            msg.addButton("No", QMessageBox.NoRole)
            action = msg.exec_()

            if action == 0:
                self.cancelTransfer = True

    def transfer(self, progress_callback):
        for row in range(self.ui.tw_status.rowCount()):
            if self.ui.tw_status.item(row, 1).text() == "Not Found":
                self.totalProgress(row + 1)
                self.updateInfoText(row + 1)
                continue

            file_from = self.ui.tw_status.item(row, 2).text()
            file_to = self.ui.tw_status.item(row, 3).text()

            self.ui.tw_status.setItem(
                row,
                0,
                QTableWidgetItem("Transfering")
            )

            if self.ui.rb_filecopy.isChecked() is True:
                self.copyfileobj(src=file_from,
                                 dst=file_to,
                                 row=row,
                                 callback_progress=self.fileProgress,
                                 callback_copydone=self.fileProgress)
            else:
                if platform.system() == 'Windows':
                    subprocess.Popen('cmd /K "' + file_from + '"')
                else:
                    subprocess.Popen(["open '" + file_from + "'"], shell=True)

                self.ui.tw_status.setItem(
                    row,
                    0,
                    QTableWidgetItem("Sync Started")
                )

            if self.cancelTransfer is True:
                break

            self.totalProgress(row + 1)
            self.updateInfoText(row + 1)

    def image_sequence_resolve_all(self, filepath):
        basedir, filename = os.path.split(filepath)
        # If resilio sync, remove the .rsls extension
        if self.ui.rb_resilio.isChecked() is True:
            filename = filename[:-5]
        filename_noext, ext = os.path.splitext(filename)

        seq_ext = self.ui.le_sequence.text().lower().replace(' ', '').split(",")
        if ext.lower()[1:] in seq_ext:
            digits = sdigits
            if isinstance(filepath, bytes):
                digits = sdigits.encode()
            filename_nodigits = filename_noext.rstrip(digits)

            if len(filename_nodigits) == len(filename_noext):
                # input isn't from a sequence
                return []

            if self.ui.rb_resilio.isChecked() is True:
                filename_noext = filename_noext + ext
                ext = ext + ".rsls"

            return [
                f.path
                for f in scandir(basedir)
                if f.is_file()
                and f.name.startswith(filename_nodigits)
                and f.name.endswith(ext)
                and f.name[len(filename_nodigits):-len(ext)
                           if ext else -1].isdigit()
            ]
        else:
            return [filepath]

    def fileProcess(self):
        self.ui.pb_file.setValue(0)
        self.ui.pb_total.setValue(0)

        if self.ui.path_xml.text() == "" or os.path.isfile(self.ui.path_xml.text()) is False:
            return

        dom = ElementTree.parse(self.ui.path_xml.text())
        xml_files = dom.iter('pathurl')
        video_files = []
        for file in xml_files:
            filename = self.adapt_path(file.text)
            if self.ui.rb_resilio.isChecked() is True:
                filename = filename + ".rsls"
            video_files.append(filename)

        found_files = []
        not_found = []
        self.ui.tw_status.setRowCount(0)
        # searching in selected directory only
        for file in video_files:
            if self.ui.cb_external.isChecked() is True:
                if self.ui.cb_subdirs.isChecked() is True:
                    oldname = (os.path.split(file))[1]
                    found = False
                    for root, dirs, files in os.walk(self.ui.path_external.text()):
                        for fname in files:
                            if oldname == fname:
                                found = os.path.join(root, fname)
                                break
                        if found is not False:
                            break
                    if found is not False:
                        found_files.append(found)
                    else:
                        not_found.append(file)
                else:
                    newpath = self.ui.path_external.text() + \
                        (os.path.split(file))[1]

                    if os.path.isfile(newpath):
                        found_files.append(newpath)
                    else:
                        not_found.append(newpath)
            else:
                if os.path.isfile(file):
                    found_files.append(file)
                else:
                    not_found.append(file)

        if self.ui.cb_sequence.isChecked() is True:
            extra_files = []
            for file in found_files:
                sequence = self.image_sequence_resolve_all(file)
                if len(sequence) != 0:
                    extra_files.extend(sequence)
            found_files = extra_files

        # Report back
        if len(found_files) > 0:
            for file in found_files:
                self.addToList(file, "Found")

        if len(not_found) > 0:
            for file in not_found:
                self.addToList(file, "Not Found")

        self.amount_of_files = len(found_files)
        self.ui.tw_status.resizeColumnsToContents()
        self.updateInfoText(0)
        return found_files

    def addToList(self, file, found):
        status = "Ready"
        copy_from = os.path.abspath(file)
        copy_to = "-"
        if self.ui.rb_filecopy.isChecked() is True:
            if (self.ui.cb_clone.isChecked() is True
                    and self.ui.path_root.text() != ""):
                to_text = os.path.join(
                    os.path.abspath(self.ui.path_copy.text()),
                    copy_from.replace(
                        os.path.abspath(self.ui.path_root.text()) + os.sep,
                        ''
                    )
                )
                copy_to = to_text
            else:
                copy_to = os.path.join(
                    os.path.abspath(self.ui.path_copy.text()),
                    (os.path.split(file))[1]
                )

        extension = os.path.splitext(file)[1]
        row = self.ui.tw_status.rowCount()
        self.ui.tw_status.setRowCount(row + 1)

        self.ui.tw_status.setItem(
            row,
            0,
            QTableWidgetItem(status)
        )
        self.ui.tw_status.setItem(
            row,
            1,
            QTableWidgetItem(found)
        )
        self.ui.tw_status.setItem(
            row,
            2,
            QTableWidgetItem(copy_from)
        )
        self.ui.tw_status.setItem(
            row,
            3,
            QTableWidgetItem(copy_to)
        )
        self.ui.tw_status.setItem(
            row,
            4,
            QTableWidgetItem(extension)
        )

    def generateFromToList(self, video_files):
        # generate from and to list
        copyList = []
        for i, file in enumerate(video_files):
            copyList.append({})
            copyList[i]["from"] = file
            if self.ui.cb_clone.isChecked() is True and self.ui.path_root.text() != "":
                to_text = os.path.join(
                    os.path.abspath(self.ui.path_copy.text()),
                    file.replace(
                        os.path.abspath(self.ui.path_root.text()) + os.sep,
                        ''
                    )
                )
                copyList[i]["to"] = to_text
            else:
                copyList[i]["to"] = os.path.join(
                    os.path.abspath(self.ui.path_copy.text()),
                    (os.path.split(file))[1]
                )
        return copyList

    def totalProgress(self, curIndex):
        percentage = int((curIndex / self.amount_of_files) * 100)
        try:
            self.ui.pb_total.setValue(percentage)
        except:
            pass

        app.processEvents()

    def fileProgress(self, size_src, size_dst):
        float_src = float(size_src)
        float_dst = float(size_dst)

        self.ui.lb_datarate.setText(self.HumanBytes(size_src)
                                    + "/"
                                    + self.HumanBytes(size_dst))

        percentage = int(float_dst / float_src * 100)

        try:
            self.ui.pb_file.setValue(percentage)
        except:
            pass

        app.processEvents()

    def HumanBytes(self, num, metric = False, precision = 2):
        """
        Human-readable formatting of bytes, using binary (powers of 1024)
        or metric (powers of 1000) representation.
        """

        assert isinstance(num, (int, float)), "num must be an int or float"
        assert isinstance(metric, bool), "metric must be a bool"
        assert isinstance(
            precision, int) and precision >= 0 and precision <= 3, "precision must be an int (range 0-3)"

        unit_labels = self.METRIC_LABELS if metric else self.BINARY_LABELS
        last_label = unit_labels[-1]
        unit_step = 1000 if metric else 1024
        unit_step_thresh = unit_step - self.PRECISION_OFFSETS[precision]

        is_negative = num < 0
        if is_negative:  # Faster than ternary assignment or always running abs().
            num = abs(num)

        for unit in unit_labels:
            if num < unit_step_thresh:
                # VERY IMPORTANT:
                # Only accepts the CURRENT unit if we're BELOW the threshold where
                # float rounding behavior would place us into the NEXT unit: F.ex.
                # when rounding a float to 1 decimal, any number ">= 1023.95" will
                # be rounded to "1024.0". Obviously we don't want ugly output such
                # as "1024.0 KiB", since the proper term for that is "1.0 MiB".
                break
            if unit != last_label:
                # We only shrink the number if we HAVEN'T reached the last unit.
                # NOTE: These looped divisions accumulate floating point rounding
                # errors, but each new division pushes the rounding errors further
                # and further down in the decimals, so it doesn't matter at all.
                num /= unit_step

        return self.PRECISION_FORMATS[precision].format("-" if is_negative else "", num, unit)

    def updateInfoText(self, curIndex):
        self.ui.lb_info.setText(
            str(curIndex)
            + " out of "
            + str(self.amount_of_files)
            + " files copied"
        )

    def copyfileobj(self, src, dst, row, callback_progress, callback_copydone, length=8 * 1024):

        # Prevent progress callback from being made each cycle
        c = 0
        c_max = 50

        if self.ui.cb_overwrite.isChecked() is False:
            if os.path.isfile(dst) is True:
                self.ui.tw_status.setItem(
                    row,
                    0,
                    QTableWidgetItem("Already exist on destination")
                )
                return

        try:
            with open(src, 'rb') as fsrc:
                size_src = os.stat(fsrc.name).st_size
                with self.safe_open_w(dst) as fdst:
                    size_dst = 0
                    while True:
                        if self.cancelTransfer is True:
                            break

                        buf = fsrc.read(length)
                        if not buf:
                            break
                        fdst.write(buf)
                        size_dst += len(buf)
                        c += 1
                        if c == c_max:
                            callback_progress(
                                size_src=size_src, size_dst=size_dst)
                            c = 0
            fdst.close()
        except OSError as exc:
            self.ui.tw_status.setItem(
                row,
                0,
                QTableWidgetItem("Error: " + str(exc))
            )
            raise

        if self.cancelTransfer is True:
            self.ui.tw_status.setItem(
                row,
                0,
                QTableWidgetItem("Canceled")
            )
            file = os.path.split(dst)[1]
            # check if dst exist. If so if we want to delete the file.
            msg = QMessageBox(
                QMessageBox.Question,
                "XML File Copy",
                file
                + " didn't transfer completely?\n"
                + "Do you want to delete the file?\n"
                + dst
            )
            msg.addButton("Yes", QMessageBox.YesRole)
            msg.addButton("No", QMessageBox.NoRole)
            action = msg.exec_()

            if action == 0:
                if os.path.exists(dst):
                    os.remove(dst)
                else:
                    msg = QMessageBox(
                        QMessageBox.Question,
                        "XML File Copy",
                        "Couldn't delete the file.\n"
                        + "Please try and delete it manually."
                    )
                    action = msg.exec_()
        else:
            self.ui.tw_status.setItem(
                row,
                0,
                QTableWidgetItem("Done")
            )

    # Taken from https://stackoverflow.com/a/600612/119527
    def mkdir_p(self, path):
        try:
            os.makedirs(path)
        except OSError as exc:  # Python >2.5
            if exc.errno == errno.EEXIST and os.path.isdir(path):
                pass
            else:
                raise

    def safe_open_w(self, path):
        ''' Open "path" for writing, creating any parent directories as needed.
        '''
        self.mkdir_p(os.path.dirname(path))
        return open(path, 'wb')

    def adapt_path(self, value):  # works in Windows for mapped drives and unc paths On Mac?
        if platform.system() == 'Windows':
            value = value.replace('file://localhost/', '')
            value = value.replace('file:', '')
            value = urlparse.unquote(value)
        # par_value = os.path.abspath(par_value)
        return value

    def print_info(self, text, reset=False):
        if reset is True:
            self.ui.txt_filelist.setPlainText("")
        else:
            self.ui.txt_filelist.setPlainText(
                self.ui.txt_filelist.toPlainText() + text + "\n"
            )

    def closeEvent(self, event):
        if self.isTransfering is True:
            msg = QMessageBox(
                QMessageBox.Question,
                "XML File Copy",
                "Are you sure you want to cancel the transfer?"
            )
            msg.addButton("Yes", QMessageBox.YesRole)
            msg.addButton("No", QMessageBox.NoRole)
            action = msg.exec_()

            if action == 0:
                event.accept()
            else:
                event.ignore()
        else:
            event.accept()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    MainWindow()
    sys.exit(app.exec_())
