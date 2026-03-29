// qml/components/Card.qml
//
// Карточка задачи.
// Только отображает данные и сообщает о действиях пользователя.
// Никакой логики — только "что нажали" передаём наружу через сигналы.

import QtQuick
import QtQuick.Layouts

Rectangle {
    id: root

    // --- Публичный интерфейс: props ---
    property int    taskId:    -1
    property string cardTitle: ""
    property string cardBody:  ""
    property string status:    "todo"

    // --- Публичный интерфейс: сигналы ---
    // Карточка НЕ знает что делать при нажатии — она только сообщает.
    // Решение принимает main.qml (передаёт в контроллер).
    signal statusClicked(int id)
    signal removeClicked(int id)

    // --- Приватные вычисляемые свойства ---
    readonly property string _statusLabel: {
        if (status === "done")        return "✓ Выполнено"
        if (status === "in_progress") return "⟳ В процессе"
        return "○ Нужно сделать"
    }
    readonly property color _statusColor: {
        if (status === "done")        return "#4ade80"
        if (status === "in_progress") return "#facc15"
        return "#94a3b8"
    }
    readonly property color _statusBg: {
        if (status === "done")        return "#14532d"
        if (status === "in_progress") return "#713f12"
        return "#1e293b"
    }

    height: layout.implicitHeight + 24
    radius: 10
    color: hoverArea.containsMouse ? "#1c2a4a" : "#16213e"
    border.color: hoverArea.containsMouse ? "#6c63ff" : "#2a2a40"
    border.width: 1

    Behavior on color       { ColorAnimation { duration: 120 } }
    Behavior on border.color { ColorAnimation { duration: 120 } }

    MouseArea {
        id: hoverArea
        anchors.fill: parent
        hoverEnabled: true
    }

    RowLayout {
        id: layout
        anchors {
            left: parent.left;   leftMargin: 14
            right: parent.right; rightMargin: 14
            top: parent.top;     topMargin: 14
            bottom: parent.bottom; bottomMargin: 14
        }
        spacing: 10

        // Текст задачи
        Column {
            Layout.fillWidth: true
            spacing: 5

            Text {
                text: root.cardTitle
                font { pixelSize: 14; weight: Font.Medium }
                color: root.status === "done" ? "#4a5568" : "#e2e8f0"
                width: parent.width
                elide: Text.ElideRight

                // Зачёркивание для выполненных
                Rectangle {
                    visible: root.status === "done"
                    width: parent.contentWidth
                    height: 1
                    anchors.verticalCenter: parent.verticalCenter
                    color: "#4a5568"
                }
            }

            Text {
                text: root.cardBody
                font.pixelSize: 12
                color: "#3a4a5a"
                width: parent.width
                wrapMode: Text.WordWrap
                visible: root.cardBody !== ""
            }
        }

        // Бейджик статуса — кликабельный
        Rectangle {
            width: statusText.implicitWidth + 16
            height: 26
            radius: 13
            color: statusBadgeArea.containsMouse
                   ? Qt.lighter(root._statusBg, 1.3)
                   : root._statusBg

            Behavior on color { ColorAnimation { duration: 120 } }

            Text {
                id: statusText
                anchors.centerIn: parent
                text: root._statusLabel
                font.pixelSize: 11
                color: root._statusColor
            }

            MouseArea {
                id: statusBadgeArea
                anchors.fill: parent
                hoverEnabled: true
                cursorShape: Qt.PointingHandCursor
                // Эмитируем сигнал — main.qml перехватит и вызовет контроллер
                onClicked: root.statusClicked(root.taskId)
            }
        }

        // Кнопка удаления — появляется при hover на карточке
        Rectangle {
            width: 26
            height: 26
            radius: 13
            color: removeArea.containsMouse ? "#7f1d1d" : "transparent"
            opacity: hoverArea.containsMouse ? 1.0 : 0.0

            Behavior on opacity { NumberAnimation { duration: 150 } }
            Behavior on color   { ColorAnimation  { duration: 120 } }

            Text {
                anchors.centerIn: parent
                text: "✕"
                font.pixelSize: 12
                color: removeArea.containsMouse ? "#fca5a5" : "#4a4a6a"
            }

            MouseArea {
                id: removeArea
                anchors.fill: parent
                hoverEnabled: true
                cursorShape: Qt.PointingHandCursor
                onClicked: root.removeClicked(root.taskId)
            }
        }
    }
}
