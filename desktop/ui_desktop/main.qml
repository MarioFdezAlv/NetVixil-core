import QtQuick 2.15
import QtQuick.Controls 2.15
import QtQuick.Layouts 1.15
import QtQuick.Window 2.15

ApplicationWindow {
    id: window
    visible: true
    width: 1000
    height: 600
    title: "NetVixil Desktop"

    ColumnLayout {
        anchors.fill: parent
        anchors.margins: 10
        spacing: 8

        RowLayout {
            spacing: 10
            Button {
                text: "Scan Network"
                onClicked: main.scanNetwork()
            }
            Button {
                text: "Clear"
                onClicked: devicesModel.updateDevices([])
            }
            Text {
                text: "Click Scan to run nmap (may require privileges)."
                verticalAlignment: Text.AlignVCenter
            }
        }

        Rectangle {
            color: "#e8e8e8"
            radius: 4
            Layout.fillWidth: true
            height: 32
            RowLayout {
                anchors.fill: parent
                anchors.margins: 6
                spacing: 8
                Text {
                    text: "IP"
                    width: 120
                    font.bold: true
                }
                Text {
                    text: "Hostname"
                    width: 150
                    font.bold: true
                }
                Text {
                    text: "MAC"
                    width: 150
                    font.bold: true
                }
                Text {
                    text: "Vendor"
                    width: 150
                    font.bold: true
                }
                Text {
                    text: "OS"
                    width: 150
                    font.bold: true
                }
            }
        }

        ScrollView {
            Layout.fillWidth: true
            Layout.fillHeight: true
            clip: true
            ListView {
                id: deviceList
                model: devicesModel
                spacing: 2
                anchors.fill: parent
                delegate: Rectangle {
                    width: parent.width
                    height: 36
                    color: index % 2 === 0 ? "#ffffff" : "#fbfbfb"
                    border.color: "#e6e6e6"
                    RowLayout {
                        anchors.fill: parent
                        anchors.margins: 6
                        spacing: 8
                        Text {
                            text: model.ip
                            width: 120
                            elide: Text.ElideRight
                        }
                        Text {
                            text: model.hostname
                            width: 150
                            elide: Text.ElideRight
                        }
                        Text {
                            text: model.mac
                            width: 150
                            elide: Text.ElideRight
                        }
                        Text {
                            text: model.vendor
                            width: 150
                            elide: Text.ElideRight
                        }
                        Text {
                            text: model.os
                            width: 150
                            elide: Text.ElideRight
                        }
                    }
                }
            }
        }
    }

    Dialog {
        id: errorDialog
        title: "Error"
        modal: true
        standardButtons: Dialog.Ok
        width: parent ? Math.min(parent.width * 0.75, 1000) : 600
        ColumnLayout {
            anchors.fill: parent
            anchors.margins: 10
            spacing: 8
            Text {
                text: "An error occurred during scan. You can copy the details below:"
                wrapMode: Text.Wrap
            }
            TextArea {
                id: errorText
                readOnly: true
                wrapMode: TextArea.Wrap
                selectByMouse: true
                text: ""
                Layout.fillWidth: true
                Layout.preferredHeight: 300
            }
        }
    }

    Connections {
        target: main
        function onErrorOccurred(message) {
            errorText.text = message;
            errorDialog.open();
        }
    }
}
