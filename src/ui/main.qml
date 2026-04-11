import QtQuick
import QtQuick.Controls
import QtQuick.Layouts
import "components"

ApplicationWindow {
    id: root
    width: 900
    height: 700
    minimumWidth: 600
    minimumHeight: 500
    visible: true
    title: "ESM GUI - Управление ККТ"
    color: "#f5f5f5"

    ColumnLayout {
        anchors.fill: parent
        anchors.margins: 20
        spacing: 16

        HeaderBar {
            Layout.fillWidth: true
        }

        ToolBar {
            Layout.fillWidth: true
        }

        KktGrid {
            Layout.fillWidth: true
            Layout.fillHeight: true
        }

        StatusBar {
            Layout.fillWidth: true
        }
    }

    Component.onCompleted: AppStorage.load_kkt()

    Connections {
        target: AppStorage
        function onKktListChanged() {
            console.log("kktList обновлён:", AppStorage.kktList.length)
        }
    }
}