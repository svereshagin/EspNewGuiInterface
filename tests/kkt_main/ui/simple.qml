import QtQuick 2.15
import QtQuick.Controls 2.15
import QtQuick.Layouts 1.15

Rectangle {
    id: root
    width: 520
    height: 700  // Увеличил высоту для кнопки
    color: "#f5f5f7"

    ColumnLayout {
        anchors.fill: parent
        anchors.margins: 20
        spacing: 16

        // Заголовок
        Rectangle {
            Layout.fillWidth: true
            Layout.preferredHeight: 50
            color: "#2196F3"
            radius: 8

            Text {
                anchors.centerIn: parent
                text: "Управление кассами"
                font.pixelSize: 20
                font.bold: true
                color: "white"
            }
        }

        // Панель выбора кассы
        Rectangle {
            Layout.fillWidth: true
            Layout.preferredHeight: 70
            color: "white"
            radius: 8
            border.color: "#e0e0e0"
            border.width: 1

            RowLayout {
                anchors.fill: parent
                anchors.margins: 12
                spacing: 10

                Text {
                    text: "Касса:"
                    font.pixelSize: 14
                    font.bold: true
                    color: "#333"
                }

                ComboBox {
                    id: comboBox
                    Layout.fillWidth: true
                    Layout.preferredHeight: 36

                    model: kktController ? kktController.kktList : []

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
                            font.family: "Courier"
                            leftPadding: 12
                            verticalAlignment: Text.AlignVCenter
                        }

                        background: Rectangle {
                            color: comboBox.highlightedIndex === index ? "#e3f2fd" : "transparent"
                        }
                    }

                    background: Rectangle {
                        color: "white"
                        border.color: comboBox.pressed ? "#2196F3" : "#c0c0c0"
                        border.width: 1
                        radius: 5
                    }
                }

                Button {
                    Layout.preferredWidth: 40
                    Layout.preferredHeight: 36
                    text: "↻"

                    onClicked: {
                        if (kktController) {
                            kktController.refresh_kkt_list()
                        }
                    }

                    background: Rectangle {
                        color: parent.hovered ? "#e0e0e0" : "#f5f5f5"
                        border.color: "#c0c0c0"
                        border.width: 1
                        radius: 5
                    }

                    contentItem: Text {
                        text: parent.text
                        font.pixelSize: 18
                        color: "#333"
                        horizontalAlignment: Text.AlignHCenter
                        verticalAlignment: Text.AlignVCenter
                    }
                }
            }
        }

        // Индикатор загрузки
        BusyIndicator {
            Layout.alignment: Qt.AlignHCenter
            running: kktController ? kktController.isLoading : false
            visible: running
            Layout.preferredHeight: 40
        }

        // Карточка с информацией о кассе
        Rectangle {
            Layout.fillWidth: true
            Layout.preferredHeight: 340
            color: "white"
            radius: 8
            border.color: "#e0e0e0"
            border.width: 1
            visible: kktController && kktController.kktInfo !== null

            ColumnLayout {
                anchors.fill: parent
                anchors.margins: 16
                spacing: 12

                // Заголовок карточки со статусом
                RowLayout {
                    Layout.fillWidth: true

                    Text {
                        text: "Информация о кассе"
                        font.pixelSize: 16
                        font.bold: true
                        color: "#2196F3"
                    }

                    Item { Layout.fillWidth: true }

                    // Статус смены
                    Rectangle {
                        width: 90
                        height: 26
                        radius: 13
                        color: {
                            if (!kktController || !kktController.kktInfo) return "#9e9e9e"
                            switch(kktController.kktInfo.shiftState) {
                                case "Открыта": return "#4caf50"
                                case "Закрыта": return "#9e9e9e"
                                default: return "#ff9800"
                            }
                        }

                        Text {
                            anchors.centerIn: parent
                            text: kktController && kktController.kktInfo ?
                                  "Смена: " + kktController.kktInfo.shiftState : ""
                            color: "white"
                            font.pixelSize: 12
                            font.bold: true
                        }
                    }
                }

                // Разделитель
                Rectangle {
                    Layout.fillWidth: true
                    height: 1
                    color: "#e0e0e0"
                }

                // Сетка с информацией (2 колонки)
                GridLayout {
                    Layout.fillWidth: true
                    columns: 2
                    columnSpacing: 20
                    rowSpacing: 12

                    // Серийный номер ККТ
                    Text {
                        text: "Серийный номер ККТ:"
                        font.pixelSize: 12
                        color: "#666"
                    }
                    Text {
                        text: kktController && kktController.kktInfo ?
                              kktController.kktInfo.kktSerial : ""
                        font.pixelSize: 14
                        font.bold: true
                        font.family: "Courier"
                        color: "#333"
                        Layout.fillWidth: true
                        elide: Text.ElideRight
                    }

                    // Модель
                    Text {
                        text: "Модель:"
                        font.pixelSize: 12
                        color: "#666"
                    }
                    Text {
                        text: kktController && kktController.kktInfo ?
                              kktController.kktInfo.modelName : ""
                        font.pixelSize: 14
                        color: "#333"
                        Layout.fillWidth: true
                        elide: Text.ElideRight
                    }

                    // Серийный номер ФН
                    Text {
                        text: "Серийный номер ФН:"
                        font.pixelSize: 12
                        color: "#666"
                    }
                    Text {
                        text: kktController && kktController.kktInfo ?
                              kktController.kktInfo.fnSerial : ""
                        font.pixelSize: 14
                        font.family: "Courier"
                        color: "#333"
                        Layout.fillWidth: true
                        elide: Text.ElideRight
                    }

                    // Версия ДККТ
                    Text {
                        text: "Версия ДККТ:"
                        font.pixelSize: 12
                        color: "#666"
                    }
                    Text {
                        text: kktController && kktController.kktInfo ?
                              kktController.kktInfo.dkktVersion : ""
                        font.pixelSize: 14
                        color: "#333"
                        Layout.fillWidth: true
                        elide: Text.ElideRight
                    }

                    // ИНН
                    Text {
                        text: "ИНН:"
                        font.pixelSize: 12
                        color: "#666"
                    }
                    Text {
                        text: kktController && kktController.kktInfo ?
                              kktController.kktInfo.kktInn : ""
                        font.pixelSize: 14
                        font.family: "Courier"
                        color: "#333"
                        Layout.fillWidth: true
                        elide: Text.ElideRight
                    }

                    // РНМ ККТ
                    Text {
                        text: "РНМ ККТ:"
                        font.pixelSize: 12
                        color: "#666"
                    }
                    Text {
                        text: kktController && kktController.kktInfo ?
                              kktController.kktInfo.kktRnm : ""
                        font.pixelSize: 14
                        font.family: "Courier"
                        color: "#333"
                        Layout.fillWidth: true
                        elide: Text.ElideRight
                    }

                    // Производитель
                    Text {
                        text: "Производитель:"
                        font.pixelSize: 12
                        color: "#666"
                    }
                    Text {
                        text: kktController && kktController.kktInfo ?
                              kktController.kktInfo.manufacturer : ""
                        font.pixelSize: 14
                        color: "#333"
                        Layout.fillWidth: true
                        elide: Text.ElideRight
                    }

                    // Разработчик
                    Text {
                        text: "Разработчик:"
                        font.pixelSize: 12
                        color: "#666"
                    }
                    Text {
                        text: kktController && kktController.kktInfo ?
                              kktController.kktInfo.developer : ""
                        font.pixelSize: 14
                        color: "#333"
                        Layout.fillWidth: true
                        elide: Text.ElideRight
                    }
                }
            }
        }

        // Кнопка регистрации
        Rectangle {
            Layout.fillWidth: true
            Layout.preferredHeight: 70
            color: "transparent"
            visible: kktController && kktController.canRegister

            Button {
                anchors.centerIn: parent
                width: 250
                height: 50
                text: "📝 Зарегистрировать кассу"

                enabled: kktController && !kktController.isLoading

                background: Rectangle {
                    color: parent.enabled ?
                           (parent.pressed ? "#2e7d32" : (parent.hovered ? "#388e3c" : "#4caf50")) :
                           "#bdbdbd"
                    radius: 25
                }

                contentItem: Text {
                    text: parent.text
                    color: "white"
                    font.pixelSize: 16
                    font.bold: true
                    horizontalAlignment: Text.AlignHCenter
                    verticalAlignment: Text.AlignVCenter
                }

                onClicked: {
                    if (kktController) {
                        kktController.register_current_kkt()
                    }
                }
            }
        }

        // Сообщение о статусе регистрации
        Rectangle {
            Layout.fillWidth: true
            Layout.preferredHeight: 40
            color: "transparent"
            visible: kktController && !kktController.canRegister && kktController.selectedKkt

            Text {
                anchors.centerIn: parent
                text: "✅ Касса уже зарегистрирована"
                color: "#4caf50"
                font.pixelSize: 14
                font.bold: true
            }
        }

        // Сообщение, если касса не выбрана
        Rectangle {
            Layout.fillWidth: true
            Layout.preferredHeight: 100
            color: "#fafafa"
            radius: 8
            border.color: "#e0e0e0"
            border.width: 1
            visible: !kktController || kktController.kktInfo === null

            ColumnLayout {
                anchors.centerIn: parent
                spacing: 8
                Text {
                    text: "📋"
                    font.pixelSize: 32
                    Layout.alignment: Qt.AlignHCenter
                }
                Text {
                    text: "Выберите кассу из списка"
                    color: "#666"
                    font.pixelSize: 14
                    Layout.alignment: Qt.AlignHCenter
                }
                Text {
                    text: "для просмотра информации и регистрации"
                    color: "#999"
                    font.pixelSize: 12
                    Layout.alignment: Qt.AlignHCenter
                }
            }
        }

        // Статистика
        Rectangle {
            Layout.fillWidth: true
            height: 36
            color: "#e3f2fd"
            radius: 5
            visible: kktController && kktController.kktList.length > 0

            RowLayout {
                anchors.fill: parent
                anchors.margins: 10
                Text {
                    text: "📊 Всего касс: " + (kktController ? kktController.kktList.length : 0)
                    color: "#1976d2"
                    font.pixelSize: 13
                    font.bold: true
                }

                Item { Layout.fillWidth: true }

                Text {
                    text: "Выбрано: " + (kktController && kktController.selectedKkt ?
                                         kktController.selectedKkt : "—")
                    color: "#1976d2"
                    font.pixelSize: 13
                    font.family: "Courier"
                }
            }
        }
    }

    // Диалог с результатом регистрации
    Dialog {
        id: registrationDialog
        title: "Регистрация кассы"
        standardButtons: Dialog.Ok
        modal: true
        anchors.centerIn: parent
        width: 400

        property string message: ""
        property bool success: false

        ColumnLayout {
            spacing: 20
            width: parent.width

            Rectangle {
                Layout.alignment: Qt.AlignHCenter
                width: 60
                height: 60
                radius: 30
                color: registrationDialog.success ? "#4caf50" : "#f44336"

                Text {
                    anchors.centerIn: parent
                    text: registrationDialog.success ? "✓" : "✗"
                    color: "white"
                    font.pixelSize: 40
                    font.bold: true
                }
            }

            Text {
                Layout.fillWidth: true
                text: registrationDialog.message
                wrapMode: Text.WordWrap
                horizontalAlignment: Text.AlignHCenter
                font.pixelSize: 14
            }
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

        function onKktInfoChanged() {
            console.log("QML: информация о кассе обновлена")
        }

        function onRegistrationResultUpdated(result) {
            console.log("QML: результат регистрации:", result)
            registrationDialog.success = result.success
            registrationDialog.message = result.message ||
                (result.success ? "Касса успешно зарегистрирована" : "Ошибка регистрации")
            registrationDialog.open()
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