import QtQuick
import QtQuick.Layouts

Column {
    spacing: 8

    // Выбранная касса
    Rectangle {
        width: parent.width
        height: 50
        color: "#e3f2fd"
        radius: 8
        visible: AppStorage.currentSerial !== ""

        RowLayout {
            anchors.fill: parent
            anchors.margins: 12

            Text { text: "Выбрана касса:"; font.bold: true; color: "#1565c0" }
            Text { text: AppStorage.currentSerial; font.bold: true; color: "#0d47a1" }
            Item { Layout.fillWidth: true }
            Text { text: "Всего: " + AppStorage.kktList.length; color: "#666"; font.pixelSize: 11 }
        }
    }

    // Ошибка
    Rectangle {
        width: parent.width
        height: 40
        color: "#ffebee"
        radius: 5
        visible: AppStorage.error !== ""

        RowLayout {
            anchors.fill: parent
            anchors.margins: 10

            Text {
                text: "⚠️ " + AppStorage.error
                color: "#c62828"
                font.pixelSize: 12
                Layout.fillWidth: true
                wrapMode: Text.WordWrap
            }
        }
    }
}