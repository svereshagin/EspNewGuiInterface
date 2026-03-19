import QtQuick 2.15
import QtQuick.Controls 2.15
import QtQuick.Layouts 1.15

Rectangle {
    id: root
    width: 700
    height: 600
    color: "#f5f5f5"

    // Свойства для диалога
    property bool dialogOpen: false
    property bool tempCompatibilityMode: false
    property bool tempAllowRemote: false
    property string tempGismtAddress: ""

    ColumnLayout {
        anchors.fill: parent
        anchors.margins: 20
        spacing: 15

        // Заголовок
        Label {
            text: "Управление ГИС МТ"
            font.pixelSize: 20
            font.bold: true
            color: "#333333"
            Layout.alignment: Qt.AlignHCenter
        }

        // Выпадающий список инстансов
        RowLayout {
            Layout.fillWidth: true
            spacing: 10

            ComboBox {
                id: instanceCombo
                Layout.fillWidth: true
                Layout.preferredHeight: 40

                model: gisMtController ? gisMtController.instances : []

                displayText: currentIndex === -1 ? "Выберите инстанс..." : currentText

                onActivated: function(index) {
                    if (gisMtController) {
                        gisMtController.select_instance(model[index])
                    }
                }

                delegate: ItemDelegate {
                    width: instanceCombo.width
                    text: modelData

                    contentItem: Text {
                        text: modelData
                        color: "black"
                        font.pixelSize: 14
                        font.family: "Courier"
                        leftPadding: 10
                        verticalAlignment: Text.AlignVCenter
                        elide: Text.ElideRight
                    }
                }

                background: Rectangle {
                    color: "white"
                    border.color: instanceCombo.pressed ? "#2196F3" : "#c0c0c0"
                    border.width: 1
                    radius: 5
                }
            }

            // Кнопка обновления
            Button {
                Layout.preferredWidth: 40
                Layout.preferredHeight: 40
                text: "↻"

                onClicked: {
                    if (gisMtController) {
                        gisMtController.refresh_instances()
                    }
                }

                background: Rectangle {
                    color: parent.hovered ? "#e0e0e0" : "#f0f0f0"
                    border.color: "#c0c0c0"
                    radius: 5
                }

                contentItem: Text {
                    text: parent.text
                    font.pixelSize: 18
                    color: "#333333"
                    horizontalAlignment: Text.AlignHCenter
                    verticalAlignment: Text.AlignVCenter
                }
            }
        }

        // Индикатор загрузки
        BusyIndicator {
            Layout.alignment: Qt.AlignHCenter
            running: gisMtController ? gisMtController.isLoading : false
            visible: running
            implicitWidth: 50
            implicitHeight: 50
        }

        // Карточка с информацией об инстансе
        Rectangle {
            Layout.fillWidth: true
            Layout.preferredHeight: 150
            color: "white"
            radius: 8
            border.color: "#e0e0e0"
            border.width: 1
            visible: gisMtController && gisMtController.selectedInstance !== ""

            ColumnLayout {
                anchors.fill: parent
                anchors.margins: 15
                spacing: 10

                Text {
                    text: "Информация об инстансе"
                    font.pixelSize: 16
                    font.bold: true
                    color: "#2196F3"
                }

                GridLayout {
                    Layout.fillWidth: true
                    columns: 2
                    columnSpacing: 10
                    rowSpacing: 8

                    Text { text: "Статус:"; font.pixelSize: 12; color: "#666666" }
                    Text {
                        text: {
                            if (!gisMtController || !gisMtController.currentSettings) return "Неизвестно"
                            return gisMtController.currentSettings.compatibilityMode ? "Активен" : "Неактивен"
                        }
                        font.pixelSize: 12
                        color: gisMtController && gisMtController.currentSettings &&
                               gisMtController.currentSettings.compatibilityMode ? "#4caf50" : "#ff9800"
                    }

                    Text { text: "ID:"; font.pixelSize: 12; color: "#666666" }
                    Text {
                        text: gisMtController ? gisMtController.selectedInstance : ""
                        font.pixelSize: 12
                        font.family: "Courier"
                        color: "#333333"
                    }

                    Text { text: "Последняя синхронизация:"; font.pixelSize: 12; color: "#666666" }
                    Text {
                        text: "только что"
                        font.pixelSize: 12
                        color: "#333333"
                    }
                }
            }
        }

        // Кнопка "Настройки"
        Button {
            Layout.fillWidth: true
            Layout.preferredHeight: 40
            text: "Настройки"
            enabled: gisMtController && gisMtController.selectedInstance !== ""

            onClicked: {
                if (gisMtController && gisMtController.currentSettings) {
                    tempCompatibilityMode = gisMtController.currentSettings.compatibilityMode
                    tempAllowRemote = gisMtController.currentSettings.allowRemote
                    tempGismtAddress = gisMtController.currentSettings.gismtAddress
                    dialogOpen = true
                    settingsDialog.open()
                }
            }

            background: Rectangle {
                color: parent.enabled ? (parent.hovered ? "#1976D2" : "#2196F3") : "#cccccc"
                radius: 5
            }

            contentItem: Text {
                text: parent.text
                color: "white"
                font.pixelSize: 14
                font.bold: true
                horizontalAlignment: Text.AlignHCenter
                verticalAlignment: Text.AlignVCenter
            }
        }

        // Сообщение, если инстанс не выбран
        Rectangle {
            Layout.fillWidth: true
            Layout.preferredHeight: 80
            color: "#f0f0f0"
            radius: 8
            visible: !gisMtController || gisMtController.selectedInstance === ""

            ColumnLayout {
                anchors.centerIn: parent
                spacing: 5
                Text {
                    text: "ℹ️"
                    font.pixelSize: 24
                    Layout.alignment: Qt.AlignHCenter
                }
                Text {
                    text: "Выберите инстанс из списка"
                    color: "#666666"
                    font.pixelSize: 14
                    Layout.alignment: Qt.AlignHCenter
                }
            }
        }
    }

    // Диалог настроек
    Dialog {
        id: settingsDialog
        title: "Настройки ГИС МТ"
        modal: true
        standardButtons: Dialog.Ok | Dialog.Cancel
        width: 400
        height: 300
        x: (parent.width - width) / 2
        y: (parent.height - height) / 2

        onAccepted: {
            if (gisMtController) {
                gisMtController.update_settings(
                    tempCompatibilityMode,
                    tempAllowRemote,
                    tempGismtAddress
                )
            }
        }

        onRejected: {
            dialogOpen = false
        }

        ColumnLayout {
            anchors.fill: parent
            anchors.margins: 20
            spacing: 15

            // Режим совместимости
            RowLayout {
                Layout.fillWidth: true
                spacing: 10

                Text {
                    text: "Режим совместимости:"
                    font.pixelSize: 14
                    color: "#333333"
                }

                Item { Layout.fillWidth: true }

                Switch {
                    checked: tempCompatibilityMode
                    onCheckedChanged: tempCompatibilityMode = checked
                }
            }

            // Режим удаленного подключения
            RowLayout {
                Layout.fillWidth: true
                spacing: 10

                Text {
                    text: "Удаленное подключение:"
                    font.pixelSize: 14
                    color: "#333333"
                }

                Item { Layout.fillWidth: true }

                Switch {
                    checked: tempAllowRemote
                    onCheckedChanged: tempAllowRemote = checked
                }
            }

            // Адрес ГИС МТ
            ColumnLayout {
                Layout.fillWidth: true
                spacing: 5

                Text {
                    text: "Адрес ГИС МТ:"
                    font.pixelSize: 14
                    color: "#333333"
                }

                TextField {
                    Layout.fillWidth: true
                    Layout.preferredHeight: 35
                    text: tempGismtAddress
                    onTextChanged: tempGismtAddress = text
                    placeholderText: "https://адрес:порт"

                    background: Rectangle {
                        color: "white"
                        border.color: parent.focus ? "#2196F3" : "#c0c0c0"
                        border.width: 1
                        radius: 3
                    }
                }
            }
        }
    }

    // Связи с контроллером
    Connections {
        target: gisMtController

        function onInstancesListChanged() {
            console.log("QML: список инстансов обновлен")
            if (instanceCombo.count === 0) {
                instanceCombo.currentIndex = -1
            }
        }

        function onSelectedInstanceChanged() {
            console.log("QML: выбран инстанс:", gisMtController.selectedInstance)
            var selected = gisMtController.selectedInstance
            if (selected) {
                var index = instanceCombo.find(selected)
                if (index !== -1) {
                    instanceCombo.currentIndex = index
                }
            }
        }

        function onSettingsChanged() {
            console.log("QML: настройки обновлены")
        }

        function onOperationCompleted(result) {
            console.log("QML: операция завершена:", JSON.stringify(result))
            if (result.success) {
                dialogOpen = false
                settingsDialog.close()
            }
        }

        function onErrorOccurred(message) {
            console.error("QML ошибка:", message)
        }
    }
}