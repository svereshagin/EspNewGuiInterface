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
            text: "Выберите кассу (серийный номер)"
            font.pixelSize: 16
            font.bold: true
        }

        // Выпадающий список с серийными номерами касс
        ComboBox {
            id: comboBox
            Layout.fillWidth: true
            Layout.preferredHeight: 40

            // Модель данных - список серийных номеров из kktList
            model: {
                if (kktController && kktController.kktList) {
                    // Если kktList уже содержит строки с номерами
                    return kktController.kktList
                }
                return []
            }

            displayText: currentIndex === -1 ? "Выберите серийный номер..." : currentText

            onActivated: function(index) {
                if (kktController) {
                    kktController.select_kkt(model[index])
                }
            }

            delegate: ItemDelegate {
                width: comboBox.width
                text: modelData

                contentItem: Text {
                    text: modelData
                    color: "black"
                    font.pixelSize: 14
                    font.family: "Courier" // моноширинный для номеров
                    leftPadding: 10
                    verticalAlignment: Text.AlignVCenter
                }

                background: Rectangle {
                    color: comboBox.highlightedIndex === index ? "#e0e0e0" : "transparent"
                }
            }

            background: Rectangle {
                color: "white"
                border.color: comboBox.pressed ? "#2196F3" : "#c0c0c0"
                border.width: 1
                radius: 5
            }
        }

        // Индикатор загрузки
        BusyIndicator {
            Layout.alignment: Qt.AlignHCenter
            running: kktController ? kktController.isLoading : false
            visible: running
        }

        // Информация о выбранной кассе
        Rectangle {
            Layout.fillWidth: true
            height: 50
            color: "#e8f5e8"
            radius: 5
            border.color: "#90a090"
            visible: kktController ? kktController.selectedKkt !== "" : false

            ColumnLayout {
                anchors.fill: parent
                anchors.margins: 10
                spacing: 2

                Label {
                    text: "Выбран серийный номер:"
                    font.pixelSize: 10
                    color: "#666666"
                }

                Label {
                    text: kktController ? kktController.selectedKkt : ""
                    font.pixelSize: 14
                    font.bold: true
                    color: "#2c5e2c"
                    font.family: "Courier"
                }
            }
        }

        // Кнопка обновления
        Button {
            Layout.alignment: Qt.AlignHCenter
            text: "Обновить список"
            implicitWidth: 150
            implicitHeight: 36

            onClicked: {
                if (kktController) {
                    kktController.refresh_kkt_list()
                }
            }

            background: Rectangle {
                color: parent.hovered ? "#e0e0e0" : "#f0f0f0"
                border.color: "#c0c0c0"
                radius: 5
            }

            contentItem: Text {
                text: "↻ " + parent.text
                color: "#333333"
                horizontalAlignment: Text.AlignHCenter
                verticalAlignment: Text.AlignVCenter
            }
        }

        // Отладочная информация
        Label {
            text: "Всего касс: " + (kktController ? kktController.kktList.length : 0)
            font.pixelSize: 10
            color: "#999999"
            Layout.alignment: Qt.AlignHCenter
        }
    }

    // Связи с контроллером
    Connections {
        target: kktController

        function onKktListChanged() {
            console.log("QML: список обновлен, касс:", kktController.kktList.length)
            comboBox.currentIndex = -1
        }

        function onSelectedKktChanged() {
            console.log("QML: выбрана касса:", kktController.selectedKkt)
            var selected = kktController.selectedKkt
            if (selected) {
                var index = comboBox.find(selected)
                if (index !== -1) {
                    comboBox.currentIndex = index
                }
            }
        }
    }

    // Загрузка при старте
    Component.onCompleted: {
        console.log("QML: загружен, запрашиваем список")
        if (kktController) {
            kktController.refresh_kkt_list()
        }
    }
}