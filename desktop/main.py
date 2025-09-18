#!/usr/bin/env python3
import sys
import os
import traceback
from PySide6.QtWidgets import QApplication
from PySide6.QtQml import QQmlApplicationEngine
from PySide6.QtCore import (
    QObject,
    Slot,
    Signal,
    QAbstractListModel,
    Qt,
    QModelIndex,
    QThread,
)

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from shared.network_scan import scan_network


class DeviceModel(QAbstractListModel):
    Roles = {
        Qt.UserRole + 1: b"ip",
        Qt.UserRole + 2: b"hostname",
        Qt.UserRole + 3: b"mac",
        Qt.UserRole + 4: b"vendor",
        Qt.UserRole + 5: b"os",
    }

    def __init__(self):
        super().__init__()
        self.devices = []

    def rowCount(self, parent=QModelIndex()):
        return len(self.devices)

    def data(self, index, role=Qt.DisplayRole):
        if not index.isValid():
            return None
        device = self.devices[index.row()]
        if role == Qt.UserRole + 1:
            return str(device.get("ip", ""))
        if role == Qt.UserRole + 2:
            return str(device.get("hostname", ""))
        if role == Qt.UserRole + 3:
            return str(device.get("mac", ""))
        if role == Qt.UserRole + 4:
            return str(device.get("vendor", ""))
        if role == Qt.UserRole + 5:
            return str(device.get("os", ""))
        return None

    def roleNames(self):
        return self.Roles

    @Slot(list)
    def updateDevices(self, devices):
        self.beginResetModel()
        self.devices = devices or []
        self.endResetModel()


class ScanWorker(QThread):
    finished = Signal(list)
    error = Signal(str)

    def run(self):
        try:
            devices = scan_network()
            if devices is None:
                devices = []
            self.finished.emit(devices)
        except Exception:
            tb = traceback.format_exc()
            self.error.emit(tb)


class Main(QObject):
    errorOccurred = Signal(str)

    def __init__(self):
        super().__init__()
        self.worker = None
        self.devicesModel = DeviceModel()

    @Slot()
    def scanNetwork(self):
        if self.worker and self.worker.isRunning():
            return
        self.worker = ScanWorker()
        self.worker.finished.connect(self.onScanFinished)
        self.worker.error.connect(self.onScanError)
        self.worker.start()

    def onScanFinished(self, devices):
        print("Devices received:", devices)
        self.devicesModel.updateDevices(devices)

    def onScanError(self, message):
        self.errorOccurred.emit(message)
        try:
            if self.worker and self.worker.isRunning():
                self.worker.quit()
                self.worker.wait(2000)
        except Exception:
            pass


def main():
    app = QApplication(sys.argv)
    engine = QQmlApplicationEngine()

    main_obj = Main()
    engine.rootContext().setContextProperty("main", main_obj)
    engine.rootContext().setContextProperty("devicesModel", main_obj.devicesModel)

    qml_path = os.path.join(os.path.dirname(__file__), "ui_desktop", "main.qml")
    engine.load(qml_path)
    if not engine.rootObjects():
        print("QQmlApplicationEngine failed to load component")
        sys.exit(-1)
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
