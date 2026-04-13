import QtQuick
import QtQuick.Layouts

Rectangle {
    color: "#2196f3"
    radius: 10
    height: 80

    ColumnLayout {
        anchors.fill: parent
        anchors.margins: 15

        Text {
            text: "Кассовое оборудование"
            font.pixelSize: 20
            font.bold: true
            color: "white"
        }
        Text {
            text: AppStorage.kktList.length + " касс · Текущая: "
                + (AppStorage.currentSerial || "не выбрана")
            font.pixelSize: 12
            color: "#e3f2fd"
        }
    }
}