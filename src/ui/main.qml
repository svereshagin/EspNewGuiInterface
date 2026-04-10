import QtQuick
import QtQuick.Controls
import QtQuick.Window

Window {
    id: root
    width: 1024
    height: 768
    visible: true
    title: "ESP Interface"

    Text {
        anchors.centerIn: parent
        text: "App is running"
        font.pixelSize: 24
    }
}