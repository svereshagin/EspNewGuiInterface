import QtQuick
import QtQuick.Controls
import QtQuick.Layouts

Rectangle {
    height: 50
    color: "transparent"

    RowLayout {
        anchors.fill: parent
        spacing: 10

        Button {
            text: "Обновить список"
            onClicked: {
                console.log("🔘 Обновить список нажата")
                AppStorage.reload_kkt()
            }
        }

        Button {
            text: "Очистить кэш"
            onClicked: AppStorage.clear_tspiot_cache()
        }

        Item { Layout.fillWidth: true }

        BusyIndicator {
            running: AppStorage.is_loading
            width: 40
            height: 40
            visible: running
        }
    }
}