import QtQuick

Item {
    id: toolBar
    width: 500
    height: 70

    Item {
        id: group_5
        x: 13
        y: 23
        height: 39
        width: 296

        Rectangle {
            id: rectangle_8252
            height: 39
            width: 296
            border.color: "#000000"
            border.width: 1
            color: "#ffffff"
        }

        Text {
            id: element_5
            x: 13
            y: 11
            height: 19
            width: 144
            color: "#a39b9b"
            font.family: "Inter"
            font.pixelSize: 16
            font.weight: Font.Bold
            horizontalAlignment: Text.AlignLeft
            text: "Выберите кассу"
            textFormat: Text.PlainText
            verticalAlignment: Text.AlignTop
            wrapMode: Text.WordWrap
        }
    }

    Rectangle {
        id: rectangle_8254
        x: 324
        y: 23
        height: 39
        width: 148
        border.color: "#000000"
        border.width: 1
        color: "#ffffff"
    }

    Text {
        id: element_6
        x: 330
        y: 34
        height: 19
        width: 137
        color: "#000000"
        font.family: "Inter"
        font.pixelSize: 15
        font.weight: Font.Bold
        horizontalAlignment: Text.AlignLeft
        text: "Обновить список"
        textFormat: Text.PlainText
        verticalAlignment: Text.AlignTop
    }
}