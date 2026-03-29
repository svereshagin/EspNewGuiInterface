// qml/components/AddTaskForm.qml
//
// Форма добавления задачи.
//
// Публичный интерфейс — только один сигнал: taskSubmitted.
// Компонент сам знает когда сабмитить (Enter или кнопка),
// сам очищает поля после отправки.
// Родитель (main.qml) просто слушает сигнал и передаёт в контроллер.

import QtQuick
import QtQuick.Controls
import QtQuick.Layouts

Rectangle {
    id: root

    // --- Публичный интерфейс ---
    // Единственное что компонент сообщает наружу — данные новой задачи.
    signal taskSubmitted(string title, string body)

    height: formColumn.implicitHeight + 24
    radius: 12
    color: "#1a1a2e"
    border.color: titleField.activeFocus || bodyField.activeFocus
                  ? "#6c63ff" : "#2a2a40"
    border.width: 1

    Behavior on border.color { ColorAnimation { duration: 150 } }

    Column {
        id: formColumn
        anchors {
            left: parent.left;   leftMargin: 16
            right: parent.right; rightMargin: 16
            top: parent.top;     topMargin: 16
        }
        spacing: 10

        // Поле заголовка
        TextField {
            id: titleField
            width: parent.width
            placeholderText: "Название задачи..."
            font.pixelSize: 14
            color: "#e2e8f0"
            placeholderTextColor: "#3a3a5a"
            background: Rectangle {
                color: "#0f0f1f"
                radius: 8
                border.color: titleField.activeFocus ? "#6c63ff" : "#2a2a40"
                border.width: 1
            }
            leftPadding: 12
            rightPadding: 12
            topPadding: 10
            bottomPadding: 10

            // Enter в заголовке — переходим в описание
            Keys.onReturnPressed: bodyField.forceActiveFocus()
        }

        // Поле описания
        TextArea {
            id: bodyField
            width: parent.width
            height: 64
            placeholderText: "Описание (необязательно)..."
            font.pixelSize: 13
            color: "#94a3b8"
            placeholderTextColor: "#2a2a4a"
            wrapMode: TextArea.Wrap
            background: Rectangle {
                color: "#0f0f1f"
                radius: 8
                border.color: bodyField.activeFocus ? "#6c63ff" : "#2a2a40"
                border.width: 1
            }
            leftPadding: 12
            rightPadding: 12
            topPadding: 10

            // Ctrl+Enter в описании — сабмитим форму
            Keys.onPressed: (event) => {
                if (event.key === Qt.Key_Return
                        && (event.modifiers & Qt.ControlModifier)) {
                    submitForm()
                }
            }
        }

        // Строка с подсказкой и кнопкой
        RowLayout {
            width: parent.width

            Text {
                text: "Enter → следующее поле  ·  Ctrl+Enter → добавить"
                font.pixelSize: 11
                color: "#2a2a4a"
                Layout.fillWidth: true
            }

            Rectangle {
                width: addBtn.implicitWidth + 28
                height: 34
                radius: 8
                color: addBtnArea.containsMouse ? "#7c73ff" : "#6c63ff"

                Behavior on color { ColorAnimation { duration: 120 } }

                Text {
                    id: addBtn
                    anchors.centerIn: parent
                    text: "Добавить"
                    font { pixelSize: 13; weight: Font.Medium }
                    color: "#ffffff"
                }

                MouseArea {
                    id: addBtnArea
                    anchors.fill: parent
                    hoverEnabled: true
                    cursorShape: Qt.PointingHandCursor
                    onClicked: submitForm()
                }
            }
        }
    }

    // --- Приватная функция сабмита ---
    // Вынесена чтобы не дублировать логику в двух местах (кнопка и Ctrl+Enter)
    function submitForm() {
        var title = titleField.text.trim()
        if (title === "") {
            // Мигаем бордером если поле пустое
            titleField.forceActiveFocus()
            return
        }
        root.taskSubmitted(title, bodyField.text)
        // Очищаем форму после отправки
        titleField.text = ""
        bodyField.text  = ""
        titleField.forceActiveFocus()
    }
}
