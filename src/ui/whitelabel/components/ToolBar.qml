import QtQuick
import QtQuick.Controls

Item {
    id: toolBar
    width: 500
    height: 70

    // Сохраняем выбранную кассу
    property string selectedKktSerial: ""

    Connections {
        target: AppStorage
        function onKktListChanged() {
            console.log("kktList обновлён:", AppStorage.kktList.length)
        }
    }

    // --- Выпадающий список касс ---

    Rectangle {
        id: rectangle_8253

        x: 11
        y: 4

        height: 78
        width: 800

        border.color: "#de2626"
        border.width: 1
        color: "transparent"
    }
    ComboBox {
        id: kassaCombo
        x: 13
        y: 23
        width: 296
        height: 39

        // Заполняем модель из AppStorage.kktList
        model: {
            var items = ["Выберите кассу"]
            for (var i = 0; i < AppStorage.kktList.length; i++) {
                items.push(AppStorage.kktList[i].kktSerial)
            }
            return items
        }

        // Сбрасываем на дефолт при обновлении списка
        Connections {
            target: AppStorage
            function onKktListChanged() {
                kassaCombo.currentIndex = 0
                toolBar.selectedKktSerial = ""
            }
        }

        onCurrentIndexChanged: {
            if (currentIndex === 0) {
                toolBar.selectedKktSerial = ""
            } else {

            var kktData = AppStorage.kktList[currentIndex - 1]
            toolBar.selectedKktSerial = kktData.kktSerial
            console.log("Выбрана касса:", toolBar.selectedKktSerial)
            AppStorage.set_current_cash(kktData.kktSerial)
            AppStorage.load_instance_info(kktData.kktSerial)
            }
        }

        contentItem: Text {
            leftPadding: 13
            text: kassaCombo.displayText
            font.family: "Inter"
            font.pixelSize: 16
            font.weight: Font.Bold
            color: kassaCombo.currentIndex === 0 ? "#a39b9b" : "#000000"
            verticalAlignment: Text.AlignVCenter
        }

        background: Rectangle {
            border.color: "#000000"
            border.width: 1
            color: "#ffffff"
        }

        delegate: ItemDelegate {
            width: kassaCombo.width
            contentItem: Text {
                text: modelData
                font.family: "Inter"
                font.pixelSize: 15
                color: index === 0 ? "#a39b9b" : "#000000"
                verticalAlignment: Text.AlignVCenter
                leftPadding: 13
            }
            highlighted: kassaCombo.highlightedIndex === index

            // Фон элемента при наведении
            background: Rectangle {
                color: highlighted ? "#e0e0e0" : "transparent"
            }
        }

        // КАСТОМИЗАЦИЯ ВЫПАДАЮЩЕГО СПИСКА (POPUP) - БЕЛЫЙ ЦВЕТ
        popup: Popup {
            id: popup
            width: kassaCombo.width
            height: Math.min(contentHeight, 300)
            padding: 0
            margins: 0

            background: Rectangle {
                color: "#ffffff"  // Белый фон выпадающего списка
                border.color: "#000000"
                border.width: 1
            }

            contentItem: ListView {
                clip: true
                implicitHeight: contentHeight
                model: kassaCombo.popup.visible ? kassaCombo.delegateModel : null
                currentIndex: kassaCombo.highlightedIndex

                // Скроллбар для длинных списков
                ScrollIndicator.vertical: ScrollIndicator { }
            }
        }
    }

    // --- Кнопка "Обновить список" ---
    Rectangle {
        id: refreshButton
        x: 324
        y: 23
        height: 39
        width: 148
        border.color: "#000000"
        border.width: 1
        color: refreshMouse.containsMouse ? "#f0f0f0" : "#ffffff"

        Text {
            anchors.centerIn: parent
            color: "#000000"
            font.family: "Inter"
            font.pixelSize: 15
            font.weight: Font.Bold
            text: "Обновить список"
        }

        MouseArea {
            id: refreshMouse
            anchors.fill: parent
            hoverEnabled: true
            onClicked: {
                console.log("🔘 Обновить список нажата")
                AppStorage.reload_kkt()
            }
        }
    }
}