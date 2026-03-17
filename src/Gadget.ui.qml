import QtQuick 2.15
import QtQuick.Controls 2.15
import QtQuick.Layouts 1.15

ApplicationWindow {
    visible: true
    width: 400
    height: 250
    title: "Выбор кассы"

    // Основной контейнер
    ColumnLayout {
        anchors.fill: parent
        anchors.margins: 20
        spacing: 20

        // Заголовок
        Label {
            text: "Выберите кассу из списка:"
            font.pixelSize: 16
            font.bold: true
        }

        // Выпадающий список (ComboBox)
        ComboBox {
            id: comboBox
            Layout.fillWidth: true
            Layout.preferredHeight: 40

            // Модель данных из Python
            model: kkt_controller.kktList

            // Текст по умолчанию, когда ничего не выбрано
            displayText: currentIndex === -1 ? "Выберите кассу..." : currentText

            // Доступен только когда не идет загрузка
            enabled: !kkt_controller.isLoading

            // Обработчик изменения выбора
            onActivated: function(index) {
                kkt_controller.select_kkt(model[index])
            }

            // Делегат для отображения элементов в выпадающем списке
            delegate: ItemDelegate {
                width: comboBox.width
                text: modelData
                highlighted: comboBox.highlightedIndex === index

                contentItem: Text {
                    text: modelData
                    color: highlighted ? "white" : "black"
                    font.pixelSize: 14
                    leftPadding: 10
                    verticalAlignment: Text.AlignVCenter
                }

                background: Rectangle {
                    color: highlighted ? "#0078d4" : "transparent"
                }
            }

            // Индикатор выпадающего списка
            indicator: Image {
                source: "qrc:/qt-project.org/imports/QtQuick/Controls.2/images/down.png"
                width: 20
                height: 20
                anchors.right: parent.right
                anchors.rightMargin: 10
                anchors.verticalCenter: parent.verticalCenter
                visible: !kkt_controller.isLoading
            }

            // Фон для закрытого состояния
            background: Rectangle {
                implicitWidth: 200
                implicitHeight: 40
                color: "white"
                border.color: comboBox.pressed ? "#0078d4" : "#c0c0c0"
                border.width: 1
                radius: 5
            }
        }

        // Разделитель
        Rectangle {
            Layout.fillWidth: true
            height: 2
            color: "#c0c0c0"
        }

        // Отображение выбранного элемента
        Rectangle {
            Layout.fillWidth: true
            height: 60
            color: "#e8f5e8"
            border.color: "#90a090"
            radius: 5

            ColumnLayout {
                anchors.fill: parent
                anchors.margins: 10
                spacing: 5

                Label {
                    text: "Выбранная касса:"
                    font.pixelSize: 14
                    font.bold: true
                    color: "#404040"
                }

                Label {
                    text: kkt_controller.selectedKkt || "ничего не выбрано"
                    font.pixelSize: 16
                    color: kkt_controller.selectedKkt ? "#2c5e2c" : "gray"
                    font.bold: kkt_controller.selectedKkt !== ""
                    font.italic: kkt_controller.selectedKkt === ""

                    // Анимация появления текста
                    Behavior on color {
                        ColorAnimation { duration: 200 }
                    }
                }
            }
        }

        // Кнопка для сброса выбора
        Button {
            Layout.alignment: Qt.AlignHCenter
            text: "Сбросить выбор"
            visible: kkt_controller.selectedKkt !== ""

            onClicked: {
                comboBox.currentIndex = -1
                kkt_controller.clear_selection()
            }

            background: Rectangle {
                color: parent.hovered ? "#f0f0f0" : "white"
                border.color: "#c0c0c0"
                radius: 5
            }
        }

        // Кнопка обновления списка
        Button {
            Layout.alignment: Qt.AlignHCenter
            text: "Обновить список"
            enabled: !kkt_controller.isLoading

            onClicked: {
                kkt_controller.refresh_kkt_list()
            }

            background: Rectangle {
                color: parent.hovered ? "#e0e0e0" : "#f0f0f0"
                border.color: "#c0c0c0"
                radius: 5
            }
        }

        // Индикатор загрузки
        BusyIndicator {
            Layout.alignment: Qt.AlignHCenter
            running: kkt_controller.isLoading
            visible: running
        }
    }

    // Обработка начального состояния
    Component.onCompleted: {
        console.log("QML: Component.onCompleted, загружаем список касс")
        kkt_controller.refresh_kkt_list()

        // Если в Python уже есть выбранный элемент, синхронизируем ComboBox
        var selected = kkt_controller.selectedKkt
        if (selected) {
            var index = comboBox.find(selected)
            if (index !== -1) {
                comboBox.currentIndex = index
            }
        }
    }

    // Следим за изменениями выбранного элемента из Python
    Connections {
        target: kkt_controller
        onSelectedKktChanged: {
            console.log("QML: selectedKktChanged, новое значение:", kkt_controller.selectedKkt)
            var selected = kkt_controller.selectedKkt
            if (selected) {
                var index = comboBox.find(selected)
                if (index !== -1 && comboBox.currentIndex !== index) {
                    comboBox.currentIndex = index
                }
            } else {
                comboBox.currentIndex = -1
            }
        }

        onKktListChanged: {
            console.log("QML: kktListChanged, новый размер списка:", kkt_controller.kktList.length)
            // Сбрасываем выбор при обновлении списка
            comboBox.currentIndex = -1
        }

        onLoadingChanged: {
            console.log("QML: loadingChanged, isLoading =", kkt_controller.isLoading)
        }
    }
}