import QtQuick 2.15
import QtQuick.Controls 2.15
import QtQuick.Layouts 1.15

Item {
    width: 450
    height: 350

    // Состояния для диалога
    property bool settingsDialogVisible: false
    property string tempAddress: ""
    property int tempPort: 0
    property string tempLogin: ""
    property string tempPassword: ""

    // Основной контент
    Rectangle {
        anchors.fill: parent
        color: "#f5f5f5"

        ColumnLayout {
            anchors.fill: parent
            anchors.margins: 20
            spacing: 15

            // Индикатор загрузки
            BusyIndicator {
                Layout.alignment: Qt.AlignHCenter
                running: regimeController.isLoading
                visible: regimeController.isLoading
            }

            // Информационная панель
            Rectangle {
                Layout.fillWidth: true
                Layout.preferredHeight: 200
                color: "white"
                radius: 8
                border.color: "#e0e0e0"
                border.width: 1

                ColumnLayout {
                    anchors.fill: parent
                    anchors.margins: 15
                    spacing: 12

                    // Статус
                    RowLayout {
                        Layout.fillWidth: true
                        Text {
                            text: "Статус:"
                            font.pixelSize: 14
                            font.bold: true
                            color: "#333"
                            width: 140
                        }
                        Text {
                            text: regimeController.status
                            font.pixelSize: 14
                            color: "#666"
                            Layout.fillWidth: true
                        }
                    }

                    // Версия
                    RowLayout {
                        Layout.fillWidth: true
                        Text {
                            text: "Версия:"
                            font.pixelSize: 14
                            font.bold: true
                            color: "#333"
                            width: 140
                        }
                        Text {
                            text: regimeController.version
                            font.pixelSize: 14
                            color: "#666"
                            Layout.fillWidth: true
                        }
                    }

                    // IP адрес
                    RowLayout {
                        Layout.fillWidth: true
                        Text {
                            text: "IP адрес:"
                            font.pixelSize: 14
                            font.bold: true
                            color: "#333"
                            width: 140
                        }
                        Text {
                            text: regimeController.ip
                            font.pixelSize: 14
                            color: "#666"
                            Layout.fillWidth: true
                        }
                    }

                    // Последняя синхронизация
                    RowLayout {
                        Layout.fillWidth: true
                        Text {
                            text: "Последняя синхр.:"
                            font.pixelSize: 14
                            font.bold: true
                            color: "#333"
                            width: 140
                        }
                        Text {
                            text: regimeController.lastSync
                            font.pixelSize: 14
                            color: "#666"
                            Layout.fillWidth: true
                        }
                    }

                    // ИНН
                    RowLayout {
                        Layout.fillWidth: true
                        Text {
                            text: "ИНН:"
                            font.pixelSize: 14
                            font.bold: true
                            color: "#333"
                            width: 140
                        }
                        Text {
                            text: regimeController.inn
                            font.pixelSize: 14
                            color: "#666"
                            Layout.fillWidth: true
                        }
                    }

                    // Логин
                    RowLayout {
                        Layout.fillWidth: true
                        Text {
                            text: "Логин:"
                            font.pixelSize: 14
                            font.bold: true
                            color: "#333"
                            width: 140
                        }
                        Text {
                            text: regimeController.login
                            font.pixelSize: 14
                            color: "#666"
                            Layout.fillWidth: true
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
                visible: regimeController.errorMessage !== ""

                Text {
                    anchors.fill: parent
                    anchors.margins: 5
                    text: regimeController.errorMessage
                    color: "#c62828"
                    font.pixelSize: 12
                    verticalAlignment: Text.AlignVCenter
                    wrapMode: Text.WordWrap
                }
            }

            // Кнопка настройки
            Button {
                Layout.alignment: Qt.AlignHCenter
                Layout.preferredWidth: 200
                Layout.preferredHeight: 40

                text: "Настроить адрес"
                font.pixelSize: 14

                background: Rectangle {
                    color: parent.pressed ? "#1565c0" : (parent.hovered ? "#1976d2" : "#2196f3")
                    radius: 4
                }

                contentItem: Text {
                    text: parent.text
                    color: "white"
                    font.pixelSize: 14
                    horizontalAlignment: Text.AlignHCenter
                    verticalAlignment: Text.AlignVCenter
                }

                onClicked: {
                    // Заполняем временные переменные текущими значениями
                    tempAddress = regimeController.ip !== "—" ? regimeController.ip : ""
                    tempPort = regimeController.ip !== "—" ? 50063 : 0
                    tempLogin = regimeController.login !== "—" ? regimeController.login : ""
                    tempPassword = ""
                    settingsDialogVisible = true
                }
            }

            // Кнопка обновления
            Button {
                Layout.alignment: Qt.AlignHCenter
                Layout.preferredWidth: 200
                Layout.preferredHeight: 40

                text: "Обновить"
                font.pixelSize: 14

                background: Rectangle {
                    color: parent.pressed ? "#2e7d32" : (parent.hovered ? "#388e3c" : "#4caf50")
                    radius: 4
                }

                contentItem: Text {
                    text: parent.text
                    color: "white"
                    font.pixelSize: 14
                    horizontalAlignment: Text.AlignHCenter
                    verticalAlignment: Text.AlignVCenter
                }

                onClicked: {
                    regimeController.refresh_all()
                }
            }
        }
    }

    // Диалог настройки (затемняющий фон)
    Rectangle {
        anchors.fill: parent
        color: "#80000000"
        visible: settingsDialogVisible

        MouseArea {
            anchors.fill: parent
            onClicked: {
                // Ничего не делаем, чтобы нельзя было закрыть кликом вне диалога
            }
        }

        // Сам диалог
        Rectangle {
            anchors.centerIn: parent
            width: 350
            height: 300
            color: "white"
            radius: 8

            ColumnLayout {
                anchors.fill: parent
                anchors.margins: 20
                spacing: 15

                Text {
                    text: "Параметры подключения к ЛМ ЧЗ"
                    font.pixelSize: 16
                    font.bold: true
                    color: "#333"
                    Layout.alignment: Qt.AlignHCenter
                }

                // Адрес
                RowLayout {
                    Layout.fillWidth: true
                    Text {
                        text: "Адрес:"
                        font.pixelSize: 14
                        width: 80
                    }
                    TextField {
                        id: addressField
                        Layout.fillWidth: true
                        text: tempAddress
                        placeholderText: "127.0.0.1"
                        selectByMouse: true
                    }
                }

                // Порт
                RowLayout {
                    Layout.fillWidth: true
                    Text {
                        text: "Порт:"
                        font.pixelSize: 14
                        width: 80
                    }
                    TextField {
                        id: portField
                        Layout.fillWidth: true
                        text: tempPort.toString()
                        placeholderText: "50063"
                        validator: IntValidator { bottom: 1; top: 65535 }
                        selectByMouse: true
                    }
                }

                // Логин
                RowLayout {
                    Layout.fillWidth: true
                    Text {
                        text: "Логин:"
                        font.pixelSize: 14
                        width: 80
                    }
                    TextField {
                        id: loginField
                        Layout.fillWidth: true
                        text: tempLogin
                        placeholderText: "admin"
                        selectByMouse: true
                    }
                }

                // Пароль
                RowLayout {
                    Layout.fillWidth: true
                    Text {
                        text: "Пароль:"
                        font.pixelSize: 14
                        width: 80
                    }
                    TextField {
                        id: passwordField
                        Layout.fillWidth: true
                        text: tempPassword
                        placeholderText: "••••••"
                        echoMode: TextInput.Password
                        selectByMouse: true
                    }
                }

                // Кнопки
                RowLayout {
                    Layout.alignment: Qt.AlignHCenter
                    spacing: 10

                    Button {
                        text: "Сохранить"
                        font.pixelSize: 14
                        Layout.preferredWidth: 100

                        background: Rectangle {
                            color: parent.pressed ? "#2e7d32" : (parent.hovered ? "#388e3c" : "#4caf50")
                            radius: 4
                        }

                        contentItem: Text {
                            text: parent.text
                            color: "white"
                            font.pixelSize: 14
                            horizontalAlignment: Text.AlignHCenter
                            verticalAlignment: Text.AlignVCenter
                        }

                        onClicked: {
                            var port = parseInt(portField.text)
                            if (isNaN(port)) port = 50063

                            regimeController.save_settings(
                                addressField.text,
                                port,
                                loginField.text,
                                passwordField.text
                            )
                            settingsDialogVisible = false
                        }
                    }

                    Button {
                        text: "Отмена"
                        font.pixelSize: 14
                        Layout.preferredWidth: 100

                        background: Rectangle {
                            color: parent.pressed ? "#b71c1c" : (parent.hovered ? "#c62828" : "#d32f2f")
                            radius: 4
                        }

                        contentItem: Text {
                            text: parent.text
                            color: "white"
                            font.pixelSize: 14
                            horizontalAlignment: Text.AlignHCenter
                            verticalAlignment: Text.AlignVCenter
                        }

                        onClicked: {
                            settingsDialogVisible = false
                        }
                    }
                }
            }
        }
    }
}