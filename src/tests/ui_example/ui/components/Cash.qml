import QtQuick
import QtQuick.Layouts

Rectangle {
    id: card
    property var kktData: ({})
    property bool isSelected: false
    signal cardClicked()

    color: isSelected ? "#e3f2fd" : "white"
    radius: 8
    border.color: isSelected ? "#2196f3" : "#ddd"
    border.width: isSelected ? 2 : 1

    MouseArea {
        anchors.fill: parent
        onClicked: card.cardClicked()
        cursorShape: Qt.PointingHandCursor
    }

    ColumnLayout {
        anchors.fill: parent
        anchors.margins: 14
        spacing: 5

        Text {
            text: kktData.modelName || "—"
            font.bold: true
            font.pixelSize: 14
            color: "#212121"
            elide: Text.ElideRight
            Layout.fillWidth: true
        }
        Text {
            text: "S/N: " + (kktData.kktSerial || "—")
            color: "#444"
            font.pixelSize: 12
        }
        Text {
            text: "ИНН: " + (kktData.kktInn || "—")
            color: "#555"
            font.pixelSize: 12
        }
        Text {
            text: "РНМ: " + (kktData.kktRnm || "—")
            color: "#555"
            font.pixelSize: 12
        }
        Text {
            text: "ФН: " + (kktData.fnSerial || "—")
            color: "#777"
            font.pixelSize: 11
        }
        Text {
            text: "S/N: " + (kktData.kktSerial || "—")
            color: "#444"
            font.pixelSize: 12
        }
        Rectangle {
            width: shiftLabel.implicitWidth + 16
            height: 22
            radius: 11
            color: (kktData.shiftState === "Открыта") ? "#e8f5e9" : "#ffebee"

            Text {
                id: shiftLabel
                anchors.centerIn: parent
                text: kktData.shiftState || "—"
                font.pixelSize: 11
                color: (kktData.shiftState === "Открыта") ? "#2e7d32" : "#c62828"
            }
        }
    }
}