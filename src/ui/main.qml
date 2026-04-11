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

        Rectangle {
            Layout.fillWidth: true
            height: 80
            color: "#2196f3"
            radius: 10

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
                    text: AppStorage.kktList.length + " касс · Текущая: " + (AppStorage.currentSerial || "не выбрана")
                    font.pixelSize: 12
                    color: "#e3f2fd"
                }
            }
        }

        RowLayout {
            Layout.fillWidth: true
            spacing: 10

            Button {
                text: "Обновить список"

                onClicked: {
                console.log("🔘 Кнопка 'Обновить список' нажата")
                console.log("  Текущий список ККТ:", AppStorage.kktList.length)
                AppStorage.reload_kkt()
                console.log("  reload_kkt() вызван")
                }
            }

            Button {
                text: "Очистить кэш"
                onClicked: AppStorage.clear_tspiot_cache()
            }
            Item { Layout.fillWidth: true }
            BusyIndicator {
                running: AppStorage.is_loading
                width: 40; height: 40
                visible: running
            }
        }

        ScrollView {
            Layout.fillWidth: true
            Layout.fillHeight: true
            clip: true
            ScrollBar.horizontal.policy: ScrollBar.AlwaysOff

            Flow {
                width: parent.width
                spacing: 12

                Repeater {
                    model: AppStorage.kktList

                    Cash {
                        width: 280
                        height: 190
                        kktData: modelData
                        isSelected: AppStorage.currentSerial === modelData.kktSerial
                        onCardClicked: AppStorage.set_current_cash(modelData.kktSerial)
                    }
                }
            }
        }

        Rectangle {
            Layout.fillWidth: true
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

        Rectangle {
            Layout.fillWidth: true
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

    Component.onCompleted: AppStorage.load_kkt()

    Connections {
        target: AppStorage
        function onKktListChanged() {
            console.log("kktList обновлён:", AppStorage.kktList.length)
        }
    }
}