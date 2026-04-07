import QtQuick 2.15
import QtQuick.Controls 2.15
import QtQuick.Layouts 1.15
import QtQuick.Window 2.15

ApplicationWindow {
    id: window
    visible: true
    width: 500
    height: 450
    title: "Приложение с контроллером"

    background: Rectangle {
        color: "#f0f0f0"
    }

    ColumnLayout {
        anchors.fill: parent
        anchors.margins: 20
        spacing: 15

        // Заголовок
        Text {
            Layout.alignment: Qt.AlignHCenter
            text: "Данные из контроллера"
            font.pixelSize: 22
            font.bold: true
            color: "#333333"
        }

        Rectangle {
            Layout.fillWidth: true
            height: 2
            color: "#3498db"
        }

        // Блок с текстом
        GroupBox {
            title: "Текст"
            Layout.fillWidth: true

            background: Rectangle {
                color: "white"
                border.color: "#cccccc"
                border.width: 1
                radius: 5
            }

            ColumnLayout {
                anchors.fill: parent
                anchors.margins: 10
                spacing: 10

                Text {
                    text: mainController.text
                    font.pixelSize: 16
                    color: "#2c3e50"
                    wrapMode: Text.WordWrap
                }

                RowLayout {
                    TextField {
                        id: textInput
                        Layout.fillWidth: true
                        placeholderText: "Введите новый текст"
                    }

                    Button {
                        text: "Обновить"
                        onClicked: {
                            if (textInput.text)
                                mainController.updateText(textInput.text)
                        }
                    }
                }
            }
        }

        // Блок со счетчиком
        GroupBox {
            title: "Счетчик"
            Layout.fillWidth: true

            background: Rectangle {
                color: "white"
                border.color: "#cccccc"
                border.width: 1
                radius: 5
            }

            ColumnLayout {
                anchors.fill: parent
                anchors.margins: 10
                spacing: 10

                Text {
                    Layout.alignment: Qt.AlignHCenter
                    text: mainController.counter
                    font.pixelSize: 48
                    font.bold: true
                    color: "#e74c3c"
                }

                RowLayout {
                    Layout.alignment: Qt.AlignHCenter
                    spacing: 20

                    Button {
                        text: "-"
                        font.pixelSize: 20
                        onClicked: mainController.decrementCounter()
                    }

                    Button {
                        text: "+"
                        font.pixelSize: 20
                        onClicked: mainController.incrementCounter()
                    }
                }
            }
        }

        // Блок со статусом
        GroupBox {
            title: "Статус"
            Layout.fillWidth: true

            background: Rectangle {
                color: "white"
                border.color: "#cccccc"
                border.width: 1
                radius: 5
            }

            RowLayout {
                anchors.fill: parent
                anchors.margins: 10

                Text {
                    text: "Текущий статус:"
                    font.pixelSize: 14
                }

                Rectangle {
                    width: 12
                    height: 12
                    radius: 6
                    color: mainController.status === "Активен" ? "#2ecc71" : "#e74c3c"
                }

                Text {
                    text: mainController.status
                    font.pixelSize: 14
                    font.bold: true
                    color: mainController.status === "Активен" ? "#27ae60" : "#c0392b"
                }
            }
        }

        // Кнопка изменения статуса
        Button {
            Layout.alignment: Qt.AlignHCenter
            Layout.preferredWidth: 200
            text: "Изменить статус"

            onClicked: {
                if (mainController.status === "Активен")
                    mainController.status = "Неактивен"
                else
                    mainController.status = "Активен"
            }
        }

        // Информационная строка
        Text {
            Layout.alignment: Qt.AlignHCenter
            text: "Данные обновляются автоматически через Property bindings"
            font.pixelSize: 10
            color: "#999999"
        }
    }

    // Вывод в консоль при загрузке
    Component.onCompleted: {
        console.log("QML загружен")
        console.log("Начальный текст:", mainController.text)
        console.log("Начальный счетчик:", mainController.counter)
        console.log("Начальный статус:", mainController.status)
    }
}