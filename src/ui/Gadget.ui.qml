// src/ui/Gadget.ui.qml
import QtQuick 2.15
import QtQuick.Controls 2.15
import QtQuick.Layouts 1.15

Rectangle {
    id: root
    width: 400
    height: 250
    color: "#f5f5f5"

    ColumnLayout {
        anchors.fill: parent
        anchors.margins: 20
        spacing: 15

        Label {
            text: "Выберите кассу"
            font.pixelSize: 16
            font.bold: true
        }

        ComboBox {
            id: comboBox
            Layout.fillWidth: true
            Layout.preferredHeight: 40

            model: kkt_controller ? kkt_controller.kktList : []

            displayText: currentIndex === -1 ? "Выберите кассу..." : currentText

            onActivated: function(index) {
                if (kkt_controller) {
                    kkt_controller.select_kkt(model[index])
                }
            }

            delegate: ItemDelegate {
                width: comboBox.width
                text: modelData

                contentItem: Text {
                    text: modelData
                    color: "black"
                    leftPadding: 10
                    verticalAlignment: Text.AlignVCenter
                }
            }

            background: Rectangle {
                color: "white"
                border.color: "#c0c0c0"
                border.width: 1
                radius: 5
            }
        }

        BusyIndicator {
            Layout.alignment: Qt.AlignHCenter
            running: kkt_controller ? kkt_controller.isLoading : false
            visible: running
        }

        Rectangle {
            Layout.fillWidth: true
            height: 50
            color: "#e8f5e8"
            radius: 5
            visible: kkt_controller ? kkt_controller.selectedKkt !== "" : false

            Label {
                anchors.centerIn: parent
                text: "Выбрано: " + (kkt_controller ? kkt_controller.selectedKkt : "")
                color: "#2c5e2c"
            }
        }

        Button {
            Layout.alignment: Qt.AlignHCenter
            text: "Обновить список"
            onClicked: {
                if (kkt_controller) {
                    kkt_controller.refresh_kkt_list()
                }
            }
        }
    }

    Connections {
        target: kkt_controller
        onKktListChanged: {
            comboBox.currentIndex = -1
        }
        onSelectedKktChanged: {
            var selected = kkt_controller.selectedKkt
            if (selected) {
                var index = comboBox.find(selected)
                if (index !== -1) {
                    comboBox.currentIndex = index
                }
            }
        }
    }

    Component.onCompleted: {
        if (kkt_controller) {
            kkt_controller.refresh_kkt_list()
        }
    }
}