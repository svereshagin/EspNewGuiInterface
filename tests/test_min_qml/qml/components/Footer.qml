// qml/components/Footer.qml
//
// Футер — показывает счётчик выполненных и кнопку их очистки.
// Логики нет — только отображение и один сигнал наружу.

import QtQuick
import QtQuick.Layouts

Rectangle {
    id: root

    // --- Публичный интерфейс ---
    property int doneCount: 0
    signal clearDoneClicked()

    height: 44
    radius: 8
    color: "#12122a"

    RowLayout {
        anchors {
            fill: parent
            leftMargin: 16
            rightMargin: 12
        }
        spacing: 8

        Text {
            text: root.doneCount > 0
                  ? root.doneCount + " выполненных задач"
                  : "Нет выполненных задач"
            font.pixelSize: 12
            color: "#4a4a6a"
            Layout.fillWidth: true
        }

        // Кнопка очистки — видна только если есть что чистить
        Rectangle {
            visible: root.doneCount > 0
            width: clearText.implicitWidth + 20
            height: 28
            radius: 6
            color: clearArea.containsMouse ? "#2d1515" : "transparent"
            border.color: "#3a1a1a"
            border.width: 1

            Behavior on color { ColorAnimation { duration: 120 } }

            Text {
                id: clearText
                anchors.centerIn: parent
                text: "Очистить выполненные"
                font.pixelSize: 11
                color: clearArea.containsMouse ? "#fca5a5" : "#6a3a3a"
            }

            MouseArea {
                id: clearArea
                anchors.fill: parent
                hoverEnabled: true
                cursorShape: Qt.PointingHandCursor
                onClicked: root.clearDoneClicked()
            }
        }
    }
}
