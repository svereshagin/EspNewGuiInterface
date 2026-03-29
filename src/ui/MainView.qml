import QtQuick 2.15
import QtQuick.Controls 2.15
import QtQuick.Layouts 1.15
import "components"  // Простой относительный импорт для dev режима

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

    // Компонент NetworkStatusPanel будет загружен динамически
    property Component networkStatusComponent: null
    property color primaryColor: "#0078d4"
    property color backgroundColor: "#f5f5f5"

    // ==================== БАННЕР ОШИБОК (глобальный, поверх всего) ====================
    Rectangle {
        id: errorBanner
        z: 100
        anchors.bottom: parent.bottom
        anchors.left: parent.left
        anchors.right: parent.right
        anchors.bottomMargin: 20
        anchors.leftMargin: 20
        anchors.rightMargin: 20
        height: 48
        radius: 8
        color: "#ffebee"
        border.color: "#ef9a9a"
        border.width: 1
        visible: opacity > 0
        opacity: 0

        property string errorText: ""

        Behavior on opacity {
            NumberAnimation { duration: 250; easing.type: Easing.OutCubic }
        }

        RowLayout {
            anchors.fill: parent
            anchors.margins: 12
            spacing: 8

            Text { text: "⚠️"; font.pixelSize: 16 }

            Text {
                Layout.fillWidth: true
                text: errorBanner.errorText
                color: "#c62828"
                font.pixelSize: 13
                elide: Text.ElideRight
                verticalAlignment: Text.AlignVCenter
            }

            Text {
                text: "✕"
                color: "#c62828"
                font.pixelSize: 16
                font.bold: true

                MouseArea {
                    anchors.fill: parent
                    cursorShape: Qt.PointingHandCursor
                    onClicked: {
                        errorHideTimer.stop()
                        errorBanner.opacity = 0
                    }
                }
            }
        }

        Timer {
            id: errorHideTimer
            interval: 5000
            repeat: false
            onTriggered: errorBanner.opacity = 0
        }

        function showError(msg) {
            errorBanner.errorText = msg
            errorBanner.opacity = 1
            errorHideTimer.restart()
        }
    }

    // ==================== ОСНОВНОЙ КОНТЕЙНЕР ====================
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

            // ==================== ПАНЕЛЬ СОСТОЯНИЯ СЕТИ ====================
            Loader {
                id: networkPanelLoader
                Layout.fillWidth: true
                Layout.preferredHeight: 300
                sourceComponent: networkStatusComponent
                active: networkStatusComponent !== null

                onLoaded: {
                    if (item && networkCheckerObj) {
                        item.networkChecker = networkCheckerObj
                        console.log("✅ NetworkStatusPanel загружен и настроен")
                    }
                }
            }

            // Разделитель
            Rectangle {
                Layout.fillWidth: true
                height: 1
                color: "#e0e0e0"
            }

            // ==================== ЛМ ЧЗ СЕКЦИЯ ====================
            Rectangle {
                Layout.fillWidth: true
                Layout.preferredHeight: 280
                color: "white"
                radius: 8
                border.color: "#e0e0e0"
                border.width: 1

                // ... (весь ваш код ЛМ ЧЗ секции, который у вас был)
                // Я сократил для читаемости, но вы можете вставить свой полный код
            }

            // ==================== ГИС МТ СЕКЦИЯ ====================
            Rectangle {
                Layout.fillWidth: true
                Layout.preferredHeight: 380
                color: "white"
                radius: 8
                border.color: "#e0e0e0"
                border.width: 1

                // ... (весь ваш код ГИС МТ секции)
            }

            // ==================== ККТ СЕКЦИЯ ====================
            Rectangle {
                Layout.fillWidth: true
                Layout.preferredHeight: 480
                color: "white"
                radius: 8
                border.color: "#e0e0e0"
                border.width: 1

                // ... (весь ваш код ККТ секции)
            }

            // ==================== СТРОКА СОСТОЯНИЯ ====================
            Rectangle {
                Layout.fillWidth: true
                height: 30
                color: "#f0f0f0"
                radius: 4

                RowLayout {
                    anchors.fill: parent
                    anchors.margins: 5

                    Text {
                        text: "✅ Статус: " + (networkCheckerObj ? (networkCheckerObj.workingCdn !== "" ? "CDN доступен" : "Поиск CDN...") : "Не инициализирован")
                        font.pixelSize: 11
                        color: "#666"
                    }

                    Item { Layout.fillWidth: true }

                    Text {
                        text: "🔄 Автообновление: 30 сек"
                        font.pixelSize: 11
                        color: "#666"
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

        Loader {
            anchors.fill: parent
            sourceComponent: {
                if (activeDialog === "gismt") return gismtSettings
                if (activeDialog === "lmchz") return lmchzSettings
                return null
            }
        }

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

    // ==================== ДИАЛОГ РЕГИСТРАЦИИ ККТ ====================
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
        target: appStorage

        function onKktListChanged(list) {
            console.log("appStorage: список ККТ обновлен, касс:", list ? list.length : 0)
            if (list && list.length > 0 && !appStorage.currentKkt) {
                appStorage.set_current_kkt(list[0])
            }
        }

        function onCurrentKktChanged(kktId) {
            console.log("appStorage: выбрана касса:", kktId)
            if (kktId) {
                var index = kktCombo.find(kktId)
                if (index !== -1) {
                    kktCombo.currentIndex = index
                }
            }
        }

        function onKktInfoUpdated(info) {
            console.log("appStorage: информация о кассе обновлена:", JSON.stringify(info))
            if (info) {
                kktSerialText.text = info.kktSerial || "—"
                modelText.text = info.modelName || "—"
                fnSerialText.text = info.fnSerial || "—"
                dkktVersionText.text = info.dkktVersion || "—"
                innText.text = info.kktInn || "—"
                kktRnmText.text = info.kktRnm || "—"
                manufacturerText.text = info.manufacturer || "—"
                developerText.text = info.developer || "—"

                var shiftState = info.shiftState
                if (shiftState === "OPENED" || shiftState === "Открыта") {
                    shiftStateText.text = "Открыта"
                } else if (shiftState === "CLOSED" || shiftState === "Закрыта") {
                    shiftStateText.text = "Закрыта"
                } else {
                    shiftStateText.text = shiftState || "—"
                }
            }
        }

        function onRegistrationCompleted(result) {
            console.log("appStorage: регистрация завершена:", JSON.stringify(result))
            registrationDialog.success = result.success
            registrationDialog.message = result.message ||
                (result.success ? "Касса успешно зарегистрирована" : "Ошибка регистрации")
            registrationDialog.open()

            if (result.success && result.kkt_serial) {
                console.log("Принудительное обновление после регистрации для", result.kkt_serial)
                appStorage.refresh_kkt_info(result.kkt_serial)
                appStorage.force_check_registration(result.kkt_serial)
            }
        }

        function onRegistrationStatusChanged(kktSerial, isRegistered) {
            console.log("appStorage: статус регистрации изменен", kktSerial, "->", isRegistered)
            if (kktSerial === appStorage.currentKkt) {
                registerButton.visible = !isRegistered
            }
        }

        function onErrorOccurred(message) {
            console.error("appStorage: ошибка:", message)
            errorBanner.showError(message)
        }

        function onLoadingChanged(loading) {
            console.log("appStorage: загрузка:", loading)
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

    // ==================== ЕДИНЫЙ БЛОК ИНИЦИАЛИЗАЦИИ ====================
    Component.onCompleted: {
        console.log("Главное окно загружено")

        // Загрузка компонента NetworkStatusPanel
        var componentPath = ""

        if (typeof networkCheckerObj !== 'undefined' && networkCheckerObj) {
            console.log("Network checker объект получен")
        }

        if (typeof qrcComponentsAvailable !== 'undefined' && qrcComponentsAvailable) {
            componentPath = "qrc:/components/NetworkStatusPanel.qml"
        } else {
            componentPath = "components/NetworkStatusPanel.qml"
        }

        var component = Qt.createComponent(componentPath)
        if (component.status === Component.Ready) {
            networkStatusComponent = component
            console.log("✅ Компонент загружен:", componentPath)
        } else {
            console.error("❌ Не удалось загрузить компонент:", componentPath)
            console.error(component.errorString())
        }

        if (appStorage) {
            Qt.callLater(function() {
                appStorage.notify_ui_ready()
            })
        }
    }
}