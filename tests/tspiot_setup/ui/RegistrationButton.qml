import QtQuick 2.15
import QtQuick.Controls 2.15
import QtQuick.Layouts 1.15

Rectangle {
    id: root
    width: 400
    height: 200
    color: "white"
    radius: 10

    // Свойства для доступа извне
    property string kktSerial: "00106327428745"

    ColumnLayout {
        anchors.centerIn: parent
        spacing: 20
        width: parent.width - 40

        // Заголовок
        Label {
            text: "Регистрация ТС ПИоТ"
            font.pixelSize: 18
            font.bold: true
            color: "#333333"
            Layout.alignment: Qt.AlignHCenter
        }

        // Серийный номер
        Label {
            text: "ККТ: " + root.kktSerial
            font.pixelSize: 14
            color: "#666666"
            Layout.alignment: Qt.AlignHCenter
        }

        // Статус регистрации
        Label {
            id: statusLabel
            text: {
                if (registrationController.isRegistered) return "✅ Зарегистрировано"
                if (registrationController.isLoading) return "⏳ Регистрация..."
                if (registrationController.error) return "❌ " + registrationController.error
                return "⚪ Ожидание регистрации"
            }
            font.pixelSize: 14
            color: {
                if (registrationController.isRegistered) return "#2e7d32"
                if (registrationController.error) return "#c62828"
                if (registrationController.isLoading) return "#ed6c02"
                return "#757575"
            }
            Layout.alignment: Qt.AlignHCenter
        }

        // Кнопка регистрации (исчезает после успеха)
        Button {
            id: registerButton
            text: "Зарегистрировать"
            visible: !registrationController.isRegistered
            enabled: !registrationController.isLoading && !registrationController.isRegistered
            Layout.alignment: Qt.AlignHCenter
            Layout.preferredWidth: 200
            Layout.preferredHeight: 40

            // Стилизация
            background: Rectangle {
                color: parent.enabled ? "#2196f3" : "#bdbdbd"
                radius: 5
                border.color: parent.pressed ? "#1976d2" : "#2196f3"
                border.width: 1
            }

            contentItem: Text {
                text: parent.text
                color: "white"
                font.pixelSize: 14
                font.bold: true
                horizontalAlignment: Text.AlignHCenter
                verticalAlignment: Text.AlignVCenter
            }

            // Обработчик нажатия
            onClicked: {
                registrationController.register(root.kktSerial)
            }

            // Анимация появления/исчезновения
            Behavior on visible {
                NumberAnimation {
                    property: "opacity"
                    duration: 300
                    easing.type: Easing.InOutQuad
                }
            }
            opacity: visible ? 1 : 0
        }

        // Индикатор загрузки (крутилка)
        BusyIndicator {
            running: registrationController.isLoading
            visible: running
            Layout.alignment: Qt.AlignHCenter
        }

        // Кнопка сброса (для тестирования)
        Button {
            text: "Сбросить статус"
            visible: registrationController.isRegistered
            Layout.alignment: Qt.AlignHCenter
            onClicked: {
                registrationController.reset()
            }

            background: Rectangle {
                color: parent.hovered ? "#f5f5f5" : "#ffffff"
                border.color: "#cccccc"
                radius: 5
            }
        }
    }

    // Обработка завершения загрузки компонента
    Component.onCompleted: {
        console.log("QML: RegistrationButton загружен, KKT:", root.kktSerial)
    }

    // Связи с контроллером
    Connections {
        target: registrationController

        onIsRegisteredChanged: {
            console.log("QML: Статус регистрации изменился:", registrationController.isRegistered)
        }

        onErrorChanged: {
            if (registrationController.error) {
                console.log("QML: Ошибка:", registrationController.error)
            }
        }
    }
}