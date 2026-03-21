import QtQuick 2.15
import QtQuick.Controls 2.15
import QtQuick.Layouts 1.15

Item {
    id: root
    width: 900
    height: 700

    // Глобальные временные переменные для диалогов
    property string tempGismtAddress: ""
    property bool tempGismtCompatibilityMode: false
    property bool tempGismtAllowRemote: false

    property string tempLmAddress: ""
    property int tempLmPort: 0
    property string tempLmLogin: ""
    property string tempLmPassword: ""

    property bool settingsDialogOpen: false
    property string activeDialog: "" // "gismt", "lmchz", "kkt"

    // Основной контейнер с скроллом
    ScrollView {
        anchors.fill: parent
        anchors.margins: 20
        clip: true
        contentWidth: availableWidth

        ColumnLayout {
            width: parent.width
            spacing: 20

            // ==================== ЗАГОЛОВОК ====================
            Rectangle {
                Layout.fillWidth: true
                Layout.preferredHeight: 60
                color: "#2196F3"
                radius: 8

                Text {
                    anchors.centerIn: parent
                    text: "Управление кассами и интеграциями"
                    font.pixelSize: 22
                    font.bold: true
                    color: "white"
                }
            }

            // ==================== ЛМ ЧЗ СЕКЦИЯ ====================
            Rectangle {
                Layout.fillWidth: true
                Layout.preferredHeight: 280
                color: "white"
                radius: 8
                border.color: "#e0e0e0"
                border.width: 1

                ColumnLayout {
                    anchors.fill: parent
                    anchors.margins: 16
                    spacing: 12

                    // Заголовок секции
                    RowLayout {
                        Layout.fillWidth: true

                        Text {
                            text: "🔌 ЛМ ЧЗ (Честный Знак)"
                            font.pixelSize: 18
                            font.bold: true
                            color: "#2196F3"
                        }

                        Item { Layout.fillWidth: true }

                        // Статус подключения
                        Rectangle {
                            width: 12
                            height: 12
                            radius: 6
                            color: lmController && lmController.isConfigured ? "#4caf50" : "#f44336"
                        }

                        Text {
                            text: lmController && lmController.isConfigured ? "Подключено" : "Отключено"
                            color: lmController && lmController.isConfigured ? "#4caf50" : "#f44336"
                            font.pixelSize: 12
                            font.bold: true
                        }
                    }

                    // Индикатор загрузки
                    BusyIndicator {
                        Layout.alignment: Qt.AlignHCenter
                        running: appStorage ? appStorage.isLoading : false
                        visible: running
                        implicitWidth: 30
                        implicitHeight: 30
                    }

                    // Информационная сетка
                    GridLayout {
                        Layout.fillWidth: true
                        columns: 2
                        columnSpacing: 20
                        rowSpacing: 8

                        Text { text: "Статус:"; font.pixelSize: 13; color: "#666" }
                        Text {
                            text: lmController ? lmController.status : "—"
                            font.pixelSize: 13
                            color: "#333"
                            Layout.fillWidth: true
                        }

                        Text { text: "Версия:"; font.pixelSize: 13; color: "#666" }
                        Text {
                            text: lmController ? lmController.version : "—"
                            font.pixelSize: 13
                            color: "#333"
                        }

                        Text { text: "IP адрес:"; font.pixelSize: 13; color: "#666" }
                        Text {  // ← Убрал RowLayout, он здесь не нужен
                            text: lmController ? lmController.ip : "—"  // ← ИСПРАВЛЕНО: теперь используем ip
                            font.pixelSize: 13
                            font.family: "Courier"
                            color: "#333"
                            Layout.fillWidth: true
                        }

                        Text { text: "Последняя синхр.:"; font.pixelSize: 13; color: "#666" }
                        Text {
                            text: lmController ? lmController.lastSync : "—"
                            font.pixelSize: 13
                            color: "#333"
                        }

                        Text { text: "ИНН:"; font.pixelSize: 13; color: "#666" }
                        Text {
                            text: lmController ? lmController.inn : "—"
                            font.pixelSize: 13
                            font.family: "Courier"
                            color: "#333"
                        }

                        // Если есть поле login, добавьте его
                        Text { text: "Логин:"; font.pixelSize: 13; color: "#666" }
                        Text {
                            text: lmController ? lmController.login : "—"
                            font.pixelSize: 13
                            color: "#333"
                        }
                    }


                    // Кнопки управления
                    RowLayout {
                        Layout.fillWidth: true
                        Layout.topMargin: 8
                        spacing: 10

                        Button {
                            Layout.preferredWidth: 140
                            Layout.preferredHeight: 36
                            text: "⚙️ Настроить"
                            enabled: appStorage && appStorage.currentKkt !== ""

                            background: Rectangle {
                                color: parent.enabled ? (parent.hovered ? "#1976D2" : "#2196F3") : "#bdbdbd"
                                radius: 5
                            }

                            contentItem: Text {
                                text: parent.text
                                color: "white"
                                font.pixelSize: 13
                                font.bold: true
                                horizontalAlignment: Text.AlignHCenter
                                verticalAlignment: Text.AlignVCenter
                            }

                            onClicked: {
                                if (lmController) {
                                    // Здесь нужно получить текущие настройки
                                    tempLmAddress = ""
                                    tempLmPort = 50063
                                    tempLmLogin = ""
                                    tempLmPassword = ""
                                    activeDialog = "lmchz"
                                    settingsDialogOpen = true
                                }
                            }
                        }

                        Button {
                            Layout.preferredWidth: 140
                            Layout.preferredHeight: 36
                            text: "🔄 Обновить"
                            enabled: appStorage && appStorage.currentKkt !== ""

                            background: Rectangle {
                                color: parent.enabled ? (parent.hovered ? "#388e3c" : "#4caf50") : "#bdbdbd"
                                radius: 5
                            }

                            contentItem: Text {
                                text: parent.text
                                color: "white"
                                font.pixelSize: 13
                                font.bold: true
                                horizontalAlignment: Text.AlignHCenter
                                verticalAlignment: Text.AlignVCenter
                            }

                            onClicked: {
                                if (appStorage) {
                                    appStorage.get_application_status()
                                }
                            }
                        }
                    }

                    // Сообщение об ошибке
                    Rectangle {
                        Layout.fillWidth: true
                        Layout.preferredHeight: 30
                        color: "#ffebee"
                        radius: 4
                        visible: lmController && lmController.error !== ""

                        Text {
                            anchors.fill: parent
                            anchors.margins: 5
                            text: lmController ? lmController.error : ""
                            color: "#c62828"
                            font.pixelSize: 12
                            verticalAlignment: Text.AlignVCenter
                            wrapMode: Text.WordWrap
                        }
                    }

                    // Сообщение, если не выбран ККТ
                    Rectangle {
                        Layout.fillWidth: true
                        Layout.preferredHeight: 30
                        color: "#fff3e0"
                        radius: 4
                        visible: appStorage && appStorage.currentKkt === ""

                        Text {
                            anchors.fill: parent
                            anchors.margins: 5
                            text: "⚠️ Сначала выберите кассу в секции ККТ"
                            color: "#ff9800"
                            font.pixelSize: 12
                            verticalAlignment: Text.AlignVCenter
                            horizontalAlignment: Text.AlignHCenter
                        }
                    }
                }
            }

            // ==================== ГИС МТ СЕКЦИЯ ====================
            Rectangle {
                Layout.fillWidth: true
                Layout.preferredHeight: 380
                color: "white"
                radius: 8
                border.color: "#e0e0e0"
                border.width: 1

                ColumnLayout {
                    anchors.fill: parent
                    anchors.margins: 16
                    spacing: 12

                    // Заголовок секции
                    RowLayout {
                        Layout.fillWidth: true

                        Text {
                            text: "🌐 ГИС МТ (Маркировка)"
                            font.pixelSize: 18
                            font.bold: true
                            color: "#2196F3"
                        }

                        Item { Layout.fillWidth: true }

                        // Статус
                        Rectangle {
                            width: 12
                            height: 12
                            radius: 6
                            color: gisMtController && gisMtController.licenseActive ? "#4caf50" : "#ff9800"
                        }

                        Text {
                            text: gisMtController && gisMtController.licenseActive ?
                                  "Лицензия активна" : "Лицензия не активна"
                            color: gisMtController && gisMtController.licenseActive ? "#4caf50" : "#ff9800"
                            font.pixelSize: 12
                            font.bold: true
                        }
                    }

                    // Индикатор загрузки
                    BusyIndicator {
                        Layout.alignment: Qt.AlignHCenter
                        running: appStorage ? appStorage.isLoading : false
                        visible: running
                        implicitWidth: 30
                        implicitHeight: 30
                    }

                    // Информация о текущем инстансе (берется из выбранного ККТ)
                    Rectangle {
                        Layout.fillWidth: true
                        Layout.preferredHeight: 240
                        color: "#f8f9fa"
                        radius: 6
                        border.color: "#e0e0e0"
                        border.width: 1
                        visible: appStorage && appStorage.currentKkt !== ""

                        ColumnLayout {
                            anchors.fill: parent
                            anchors.margins: 12
                            spacing: 8

                            // Заголовок
                            RowLayout {
                                Layout.fillWidth: true

                                Text {
                                    text: "Информация для инстанса:"
                                    font.pixelSize: 14
                                    font.bold: true
                                    color: "#333"
                                }

                                Text {
                                    text: appStorage ? appStorage.currentKkt : ""
                                    font.pixelSize: 14
                                    font.family: "Courier"
                                    color: "#2196F3"
                                    font.bold: true
                                }
                            }

                            // Основная информация
                            GridLayout {
                                Layout.fillWidth: true
                                columns: 2
                                columnSpacing: 20
                                rowSpacing: 6

                                Text { text: "Статус ГИС МТ:"; font.pixelSize: 12; color: "#666" }
                                Text {
                                    text: gisMtController ? gisMtController.status : "—"
                                    font.pixelSize: 12
                                    color: gisMtController && gisMtController.status === "Подключено" ? "#4caf50" : "#f44336"
                                }

                                Text { text: "Версия:"; font.pixelSize: 12; color: "#666" }
                                Text {
                                    text: gisMtController ? gisMtController.licenseVersion : "—"
                                    font.pixelSize: 12
                                    font.family: "Courier"
                                    color: "#333"
                                }

                                Text { text: "Состояние:"; font.pixelSize: 12; color: "#666" }
                                Text {
                                    text: gisMtController ? gisMtController.licenseState : "—"
                                    font.pixelSize: 12
                                    color: "#333"
                                }

                                Text { text: "Последнее соединение:"; font.pixelSize: 12; color: "#666" }
                                Text {
                                    text: gisMtController ? gisMtController.lastConnection : "—"
                                    font.pixelSize: 12
                                    color: "#333"
                                }
                            }

                            // Секция лицензии
                            Rectangle {
                                Layout.fillWidth: true
                                Layout.preferredHeight: 70
                                color: gisMtController && gisMtController.licenseActive ? "#e8f5e8" : "#fff3e0"
                                radius: 4
                                border.color: gisMtController && gisMtController.licenseActive ? "#a5d6a5" : "#ffe0b2"
                                border.width: 1

                                ColumnLayout {
                                    anchors.fill: parent
                                    anchors.margins: 8
                                    spacing: 4

                                    RowLayout {
                                        Layout.fillWidth: true

                                        Text {
                                            text: "📄 Лицензия:"
                                            font.pixelSize: 11
                                            font.bold: true
                                            color: "#666"
                                        }

                                        Item { Layout.fillWidth: true }

                                        Rectangle {
                                            width: 8
                                            height: 8
                                            radius: 4
                                            color: gisMtController && gisMtController.licenseActive ? "#4caf50" : "#ff9800"
                                        }

                                        Text {
                                            text: gisMtController && gisMtController.licenseActive ? "Активна" : "Не активна"
                                            color: gisMtController && gisMtController.licenseActive ? "#4caf50" : "#ff9800"
                                            font.pixelSize: 10
                                            font.bold: true
                                        }
                                    }

                                    GridLayout {
                                        Layout.fillWidth: true
                                        columns: 2
                                        columnSpacing: 15
                                        rowSpacing: 2

                                        Text { text: "Действует до:"; font.pixelSize: 10; color: "#666" }
                                        Text {
                                            text: gisMtController ? gisMtController.licenseActiveTill : "—"
                                            font.pixelSize: 10
                                            font.bold: gisMtController && gisMtController.licenseActive
                                            color: gisMtController && gisMtController.licenseActive ? "#2e7d32" : "#666"
                                        }

                                        Text { text: "Последняя синхр.:"; font.pixelSize: 10; color: "#666" }
                                        Text {
                                            text: gisMtController ? gisMtController.licenseLastSync : "—"
                                            font.pixelSize: 10
                                            color: "#666"
                                        }
                                    }
                                }
                            }

                            Button {
                                Layout.alignment: Qt.AlignRight
                                Layout.preferredWidth: 120
                                Layout.preferredHeight: 30
                                text: "⚙️ Настройки"
                                enabled: appStorage && appStorage.currentKkt !== ""

                                background: Rectangle {
                                    color: parent.enabled ? (parent.hovered ? "#1976D2" : "#2196F3") : "#bdbdbd"
                                    radius: 4
                                }

                                contentItem: Text {
                                    text: parent.text
                                    color: "white"
                                    font.pixelSize: 12
                                    font.bold: true
                                    horizontalAlignment: Text.AlignHCenter
                                    verticalAlignment: Text.AlignVCenter
                                }

                                onClicked: {
                                    if (gisMtController && gisMtController.settings) {
                                        tempGismtCompatibilityMode = gisMtController.settings.compatibilityMode || false
                                        tempGismtAllowRemote = gisMtController.settings.allowRemote || false
                                        tempGismtAddress = gisMtController.settings.gismtAddress || ""
                                        activeDialog = "gismt"
                                        settingsDialogOpen = true
                                    }
                                }
                            }
                        }
                    }

                    // Сообщение, если ККТ не выбран
                    Rectangle {
                        Layout.fillWidth: true
                        Layout.preferredHeight: 80
                        color: "#f8f9fa"
                        radius: 6
                        border.color: "#e0e0e0"
                        border.width: 1
                        visible: !appStorage || appStorage.currentKkt === ""

                        ColumnLayout {
                            anchors.centerIn: parent
                            spacing: 5
                            Text {
                                text: "ℹ️"
                                font.pixelSize: 24
                                Layout.alignment: Qt.AlignHCenter
                            }
                            Text {
                                text: "Сначала выберите кассу в секции ККТ"
                                color: "#666"
                                font.pixelSize: 13
                                Layout.alignment: Qt.AlignHCenter
                            }
                        }
                    }
                }
            }

            // ==================== ККТ СЕКЦИЯ ====================
            Rectangle {
                Layout.fillWidth: true
                Layout.preferredHeight: 380
                color: "white"
                radius: 8
                border.color: "#e0e0e0"
                border.width: 1

                ColumnLayout {
                    anchors.fill: parent
                    anchors.margins: 16
                    spacing: 12

                    // Заголовок секции
                    RowLayout {
                        Layout.fillWidth: true

                        Text {
                            text: "💰 Управление кассами (ККТ)"
                            font.pixelSize: 18
                            font.bold: true
                            color: "#2196F3"
                        }

                        Item { Layout.fillWidth: true }

                        Text {
                            text: "Всего: " + (kktController ? kktController.kktList.length : 0)
                            color: "#666"
                            font.pixelSize: 12
                            font.bold: true
                        }
                    }

                    // Выбор кассы
                    RowLayout {
                        Layout.fillWidth: true
                        spacing: 10

                        Text {
                            text: "Касса:"
                            font.pixelSize: 14
                            font.bold: true
                            color: "#333"
                        }

                        ComboBox {
                            id: kktCombo
                            Layout.fillWidth: true
                            Layout.preferredHeight: 36

                            model: kktController ? kktController.kktList : []

                            displayText: currentIndex === -1 ? "Выберите серийный номер..." : currentText

                            onActivated: function(index) {
                                if (kktController) {
                                    kktController.selectKkt(model[index])
                                }
                            }

                            delegate: ItemDelegate {
                                width: kktCombo.width
                                text: modelData

                                contentItem: Text {
                                    text: modelData
                                    color: "black"
                                    font.pixelSize: 13
                                    font.family: "Courier"
                                    leftPadding: 12
                                    verticalAlignment: Text.AlignVCenter
                                }
                            }

                            background: Rectangle {
                                color: "white"
                                border.color: kktCombo.pressed ? "#2196F3" : "#c0c0c0"
                                border.width: 1
                                radius: 5
                            }
                        }

                        Button {
                            Layout.preferredWidth: 36
                            Layout.preferredHeight: 36
                            text: "↻"

                            onClicked: {
                                if (kktController) {
                                    kktController.refreshList()
                                }
                            }

                            background: Rectangle {
                                color: parent.hovered ? "#e0e0e0" : "#f5f5f5"
                                border.color: "#c0c0c0"
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

                    // Индикатор загрузки
                    BusyIndicator {
                        Layout.alignment: Qt.AlignHCenter
                        running: appStorage ? appStorage.isLoading : false
                        visible: running
                        implicitWidth: 30
                        implicitHeight: 30
                    }

                    // Информация о кассе
                    Rectangle {
                        Layout.fillWidth: true
                        Layout.preferredHeight: 200
                        color: "#f8f9fa"
                        radius: 6
                        border.color: "#e0e0e0"
                        border.width: 1
                        visible: kktController && kktController.kktInfo !== null

                        ColumnLayout {
                            anchors.fill: parent
                            anchors.margins: 12
                            spacing: 8

                            // Заголовок
                            Text {
                                text: "Информация о кассе"
                                font.pixelSize: 14
                                font.bold: true
                                color: "#333"
                            }

                            // Сетка информации
                            GridLayout {
                                Layout.fillWidth: true
                                columns: 2
                                columnSpacing: 20
                                rowSpacing: 6

                                Text { text: "Серийный номер:"; font.pixelSize: 12; color: "#666" }
                                Text {
                                    text: kktController && kktController.kktInfo ?
                                          kktController.kktInfo.kktSerial : ""
                                    font.pixelSize: 12
                                    font.family: "Courier"
                                    color: "#333"
                                    Layout.fillWidth: true
                                }

                                Text { text: "Модель:"; font.pixelSize: 12; color: "#666" }
                                Text {
                                    text: kktController && kktController.kktInfo ?
                                          kktController.kktInfo.modelName : ""
                                    font.pixelSize: 12
                                    color: "#333"
                                }

                                Text { text: "СН ФН:"; font.pixelSize: 12; color: "#666" }
                                Text {
                                    text: kktController && kktController.kktInfo ?
                                          kktController.kktInfo.fnSerial : ""
                                    font.pixelSize: 12
                                    font.family: "Courier"
                                    color: "#333"
                                }

                                Text { text: "Версия ДККТ:"; font.pixelSize: 12; color: "#666" }
                                Text {
                                    text: kktController && kktController.kktInfo ?
                                          kktController.kktInfo.dkktVersion : ""
                                    font.pixelSize: 12
                                    color: "#333"
                                }

                                Text { text: "ИНН:"; font.pixelSize: 12; color: "#666" }
                                Text {
                                    text: kktController && kktController.kktInfo ?
                                          kktController.kktInfo.kktInn : ""
                                    font.pixelSize: 12
                                    font.family: "Courier"
                                    color: "#333"
                                }

                                Text { text: "РНМ ККТ:"; font.pixelSize: 12; color: "#666" }
                                Text {
                                    text: kktController && kktController.kktInfo ?
                                          kktController.kktInfo.kktRnm : ""
                                    font.pixelSize: 12
                                    font.family: "Courier"
                                    color: "#333"
                                }
                            }
                        }
                    }

                    // Кнопка регистрации
                    Button {
                        Layout.alignment: Qt.AlignHCenter
                        Layout.preferredWidth: 250
                        Layout.preferredHeight: 40
                        text: "📝 Зарегистрировать кассу"
                        visible: kktController && kktController.canRegister

                        enabled: kktController && !appStorage.isLoading

                        background: Rectangle {
                            color: parent.enabled ?
                                   (parent.pressed ? "#2e7d32" : (parent.hovered ? "#388e3c" : "#4caf50")) :
                                   "#bdbdbd"
                            radius: 20
                        }

                        contentItem: Text {
                            text: parent.text
                            color: "white"
                            font.pixelSize: 14
                            font.bold: true
                            horizontalAlignment: Text.AlignHCenter
                            verticalAlignment: Text.AlignVCenter
                        }

                        onClicked: {
                            if (kktController) {
                                kktController.registerCurrentKkt()
                            }
                        }
                    }

                    // Сообщение о статусе
                    Text {
                        Layout.alignment: Qt.AlignHCenter
                        visible: kktController && !kktController.canRegister &&
                                kktController && kktController.selectedKkt !== ""
                        text: "✅ Касса уже зарегистрирована"
                        color: "#4caf50"
                        font.pixelSize: 13
                        font.bold: true
                    }

                    // Сообщение, если касса не выбрана
                    Rectangle {
                        Layout.fillWidth: true
                        Layout.preferredHeight: 80
                        color: "#f8f9fa"
                        radius: 6
                        border.color: "#e0e0e0"
                        border.width: 1
                        visible: !kktController || kktController.kktInfo === null

                        ColumnLayout {
                            anchors.centerIn: parent
                            spacing: 5
                            Text {
                                text: "📋"
                                font.pixelSize: 24
                                Layout.alignment: Qt.AlignHCenter
                            }
                            Text {
                                text: "Выберите кассу из списка"
                                color: "#666"
                                font.pixelSize: 13
                                Layout.alignment: Qt.AlignHCenter
                            }
                        }
                    }
                }
            }

            // ==================== ФУТЕР ====================
            Rectangle {
                Layout.fillWidth: true
                Layout.preferredHeight: 40
                color: "transparent"

                Text {
                    anchors.centerIn: parent
                    text: "Текущая касса: " + (appStorage && appStorage.currentKkt ? appStorage.currentKkt : "не выбрана")
                    color: "#666"
                    font.pixelSize: 12
                    font.bold: true
                }
            }
        }
    }

    // ==================== ДИАЛОГ НАСТРОЕК ====================
    Dialog {
        id: settingsDialog
        modal: true
        standardButtons: Dialog.Ok | Dialog.Cancel
        width: 450
        height: getDialogHeight()
        x: (parent.width - width) / 2
        y: (parent.height - height) / 2
        visible: settingsDialogOpen

        function getDialogHeight() {
            switch(activeDialog) {
                case "gismt": return 280
                case "lmchz": return 350
                default: return 200
            }
        }

        title: {
            switch(activeDialog) {
                case "gismt": return "Настройки ГИС МТ для кассы " + (appStorage ? appStorage.currentKkt : "")
                case "lmchz": return "Параметры подключения к ЛМ ЧЗ для кассы " + (appStorage ? appStorage.currentKkt : "")
                default: return "Настройки"
            }
        }

        onAccepted: {
            if (activeDialog === "gismt" && gisMtController && appStorage && appStorage.currentKkt) {
                gisMtController.updateSettings(
                    appStorage.currentKkt,
                    tempGismtCompatibilityMode,
                    tempGismtAllowRemote,
                    tempGismtAddress
                )
            } else if (activeDialog === "lmchz" && lmController) {
                lmController.saveSettings(
                    tempLmAddress,
                    tempLmPort,
                    tempLmLogin,
                    tempLmPassword
                )
            }
            settingsDialogOpen = false
        }

        onRejected: {
            settingsDialogOpen = false
        }

        // Контент для ГИС МТ
        Loader {
            anchors.fill: parent
            sourceComponent: {
                if (activeDialog === "gismt") return gismtSettings
                if (activeDialog === "lmchz") return lmchzSettings
                return null
            }
        }

        // Компонент настроек ГИС МТ
        Component {
            id: gismtSettings
            ColumnLayout {
                anchors.fill: parent
                anchors.margins: 20
                spacing: 15

                RowLayout {
                    Layout.fillWidth: true
                    Text { text: "Режим совместимости:"; font.pixelSize: 14; color: "#333" }
                    Item { Layout.fillWidth: true }
                    Switch {
                        checked: tempGismtCompatibilityMode
                        onCheckedChanged: tempGismtCompatibilityMode = checked
                    }
                }

                RowLayout {
                    Layout.fillWidth: true
                    Text { text: "Удаленное подключение:"; font.pixelSize: 14; color: "#333" }
                    Item { Layout.fillWidth: true }
                    Switch {
                        checked: tempGismtAllowRemote
                        onCheckedChanged: tempGismtAllowRemote = checked
                    }
                }

                ColumnLayout {
                    Layout.fillWidth: true
                    Text { text: "Адрес ГИС МТ:"; font.pixelSize: 14; color: "#333" }
                    TextField {
                        Layout.fillWidth: true
                        text: tempGismtAddress
                        onTextChanged: tempGismtAddress = text
                        placeholderText: "https://адрес:порт"
                    }
                }
            }
        }

        // Компонент настроек ЛМ ЧЗ
        Component {
            id: lmchzSettings
            ColumnLayout {
                anchors.fill: parent
                anchors.margins: 20
                spacing: 15

                RowLayout {
                    Layout.fillWidth: true
                    Text { text: "Адрес:"; font.pixelSize: 14; width: 80 }
                    TextField {
                        Layout.fillWidth: true
                        text: tempLmAddress
                        placeholderText: "127.0.0.1"
                        onTextChanged: tempLmAddress = text
                    }
                }

                RowLayout {
                    Layout.fillWidth: true
                    Text { text: "Порт:"; font.pixelSize: 14; width: 80 }
                    TextField {
                        Layout.fillWidth: true
                        text: tempLmPort.toString()
                        placeholderText: "50063"
                        validator: IntValidator { bottom: 1; top: 65535 }
                        onTextChanged: tempLmPort = parseInt(text) || 0
                    }
                }

                RowLayout {
                    Layout.fillWidth: true
                    Text { text: "Логин:"; font.pixelSize: 14; width: 80 }
                    TextField {
                        Layout.fillWidth: true
                        text: tempLmLogin
                        placeholderText: "admin"
                        onTextChanged: tempLmLogin = text
                    }
                }

                RowLayout {
                    Layout.fillWidth: true
                    Text { text: "Пароль:"; font.pixelSize: 14; width: 80 }
                    TextField {
                        Layout.fillWidth: true
                        text: tempLmPassword
                        placeholderText: "••••••"
                        echoMode: TextInput.Password
                        onTextChanged: tempLmPassword = text
                    }
                }
            }
        }
    }

    // Диалог регистрации ККТ
    Dialog {
        id: registrationDialog
        title: "Регистрация кассы"
        standardButtons: Dialog.Ok
        modal: true
        x: (parent.width - width) / 2
        y: (parent.height - height) / 2
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

    // ==================== СВЯЗИ С КОНТРОЛЛЕРАМИ ====================
    Connections {
        target: kktController

        function onKktListChanged() {
            console.log("ККТ: список обновлен, касс:", kktController.kktList.length)
            // Автоматически выбираем первый элемент, если список не пуст и ничего не выбрано
            if (kktController.kktList.length > 0 && kktController.selectedKkt === "") {
                kktController.selectKkt(kktController.kktList[0])
            }
        }

        function onSelectedKktChanged() {
            console.log("ККТ: выбрана касса:", kktController.selectedKkt)
            var selected = kktController.selectedKkt
            if (selected) {
                var index = kktCombo.find(selected)
                if (index !== -1) {
                    kktCombo.currentIndex = index
                }
            }
        }


        // Добавьте этот обработчик
        function onKktInfoChanged(info) {
            console.log("ККТ: информация обновлена:", JSON.stringify(info))
            // UI автоматически обновится через привязку kktController.kktInfo
        }

        function onRegistrationResultChanged(result) {
            console.log("ККТ: результат регистрации:", JSON.stringify(result))
            registrationDialog.success = result.success
            registrationDialog.message = result.message ||
                (result.success ? "Касса успешно зарегистрирована" : "Ошибка регистрации")
            registrationDialog.open()
        }
    }

    Connections {
        target: gisMtController

        function onGismtStatusChanged() {
            console.log("ГИС МТ: статус обновлен")
        }

        function onLicenseInfoChanged() {
            console.log("ГИС МТ: информация о лицензии обновлена")
        }
    }

    Connections {
        target: lmController

        function onLmStatusChanged() {
            console.log("ЛМ ЧЗ: статус обновлен")
        }
    }

    Connections {
        target: appStorage

        function onErrorOccurred(message) {
            console.error("Ошибка:", message)
        }
    }

    // Инициализация при загрузке
    Component.onCompleted: {
        console.log("Главное окно загружено")
         if (appStorage) {
        appStorage.notify_ui_ready()
         }
    }
}