import QtQuick 2.15
import QtQuick.Controls 2.15
import QtQuick.Layouts 1.15
import QtQuick.Window 2.15

ApplicationWindow {
    id: window
    visible: true
    width: 400
    height: 300
    title: "Простой выбор Да/Нет"

    // Настройки внешнего вида
    background: Rectangle {
        color: "#f5f5f5"
    }

    // Основной контейнер
    ColumnLayout {
        anchors.centerIn: parent
        spacing: 20
        width: parent.width - 40

        // Заголовок
        Text {
            Layout.alignment: Qt.AlignHCenter
            text: "Выберите вариант:"
            font.pixelSize: 18
            font.bold: true
            color: "#333333"
        }

        // Выпадающий список
        ComboBox {
            id: comboBox
            Layout.fillWidth: true
            Layout.preferredHeight: 40

            // Получаем данные из Python
            model: simpleController.getOptions()

            // Плейсхолдер
            currentIndex: -1
            displayText: currentIndex === -1 ? "─── Выберите ───" : currentText

            // Настройка внешнего вида
            delegate: ItemDelegate {
                width: comboBox.width
                height: 40

                contentItem: Text {
                    text: modelData
                    color: "#333333"
                    font.pixelSize: 14
                    verticalAlignment: Text.AlignVCenter
                    horizontalAlignment: Text.AlignHCenter
                }

                background: Rectangle {
                    color: highlighted ? "#e0e0e0" : "white"
                }
            }

            // Индикатор (стрелочка)
            indicator: Canvas {
                id: canvas
                x: comboBox.width - width - 15
                y: comboBox.topPadding + (comboBox.availableHeight - height) / 2
                width: 12
                height: 6

                onPaint: {
                    var ctx = getContext("2d")
                    ctx.reset()
                    ctx.moveTo(0, 0)
                    ctx.lineTo(width / 2, height)
                    ctx.lineTo(width, 0)
                    ctx.closePath()
                    ctx.fillStyle = "#666666"
                    ctx.fill()
                }
            }

            // Фон
            background: Rectangle {
                implicitWidth: 200
                implicitHeight: 40
                border.color: "#cccccc"
                border.width: 1
                radius: 5
                color: "white"
            }

            // Обработка выбора
            onActivated: {
                simpleController.selectOption(currentText)
            }
        }

        // Разделитель
        Rectangle {
            Layout.fillWidth: true
            height: 1
            color: "#dddddd"
            Layout.topMargin: 10
            Layout.bottomMargin: 10
        }

        // Информация о выборе
        Rectangle {
            Layout.fillWidth: true
            Layout.preferredHeight: 80
            color: "#ffffff"
            radius: 5
            border.color: "#dddddd"
            border.width: 1

            ColumnLayout {
                anchors.fill: parent
                anchors.margins: 15
                spacing: 8

                Text {
                    text: "Текущий выбор:"
                    font.pixelSize: 12
                    color: "#666666"
                }

                Text {
                    id: selectionDisplay
                    text: {
                        var current = simpleController.getCurrentSelection()
                        return current === "Ничего не выбрано" ? "❌ Ничего не выбрано" : "✅ " + current
                    }
                    font.pixelSize: 16
                    font.bold: true
                    color: selectionDisplay.text.includes("✅") ? "#4CAF50" : "#999999"
                }
            }
        }

        // Кнопка "Показать выбор"
        Button {
            Layout.alignment: Qt.AlignHCenter
            Layout.preferredWidth: 150
            Layout.preferredHeight: 40

            text: "Показать выбор"

            background: Rectangle {
                color: parent.pressed ? "#45a049" : "#4CAF50"
                radius: 5
            }

            contentItem: Text {
                text: parent.text
                color: "white"
                font.bold: true
                horizontalAlignment: Text.AlignHCenter
                verticalAlignment: Text.AlignVCenter
            }

            onClicked: {
                var selection = simpleController.getCurrentSelection()
                messageText.text = "Выбрано: " + selection
                messagePopup.open()
            }
        }
    }

    // Всплывающее сообщение
    Popup {
        id: messagePopup
        anchors.centerIn: parent
        width: 250
        height: 100
        modal: true
        focus: true

        background: Rectangle {
            color: "white"
            radius: 10
            border.color: "#4CAF50"
            border.width: 2
        }

        ColumnLayout {
            anchors.fill: parent
            anchors.margins: 15
            spacing: 10

            Text {
                id: messageText
                Layout.fillWidth: true
                wrapMode: Text.WordWrap
                horizontalAlignment: Text.AlignHCenter
                font.pixelSize: 14
            }

            Button {
                Layout.alignment: Qt.AlignHCenter
                text: "OK"
                onClicked: messagePopup.close()

                background: Rectangle {
                    color: "#4CAF50"
                    radius: 3
                }

                contentItem: Text {
                    text: "OK"
                    color: "white"
                }
            }
        }
    }

    // Подключение сигнала из Python для автоматического обновления
    Connections {
        target: simpleController
        function onSelectionChanged(option) {
            console.log("Сигнал из Python: выбрано", option)
            selectionDisplay.text = "✅ " + option
        }
    }

    // Вывод в консоль при загрузке
    Component.onCompleted: {
        console.log("QML загружен")
        console.log("Доступные варианты:", simpleController.getOptions())
    }
}