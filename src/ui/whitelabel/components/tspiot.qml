Text {
    id: element_2

    x: 94
    y: 111

    height: 19
    width: 80

    color: "#000000"
    font.family: "Inter"
    font.pixelSize: 16
    font.weight: Font.Bold
    horizontalAlignment: Text.AlignLeft
    text: "Лицензия"
    textFormat: Text.PlainText
    verticalAlignment: Text.AlignTop
    wrapMode: Text.WordWrap
}

Text {
    id: element_3

    x: 189
    y: 111

    height: 17
    width: 161

    color: "#000000"
    font.family: "Inter"
    font.pixelSize: 14
    font.weight: Font.Bold
    horizontalAlignment: Text.AlignLeft
    text: "Активна До 31.12.2027"
    textFormat: Text.PlainText
    verticalAlignment: Text.AlignTop
    wrapMode: Text.WordWrap
}

Item {
            id: group_3

            x: 443
            y: 111

            height: 54
            width: 368.50

            Shape {
                id: line_2

                y: 26

                height: 0.01
                width: 368.50

                rotation: 0.15

                ShapePath {
                    id: line_2_ShapePath0

                    fillColor: "#00000000"
                    strokeColor: "#000000"
                    strokeWidth: 1

                    PathSvg {
                        id: line_2_ShapePath0_PathSvg0

                        path: "M 0 0 L 368.5 0.006742153316736221"
                    }
                }
            }
            Text {
                id: element_4

                x: 1

                height: 18
                width: 57

                color: "#000000"
                font.family: "Inter"
                font.pixelSize: 15
                font.weight: Font.Bold
                horizontalAlignment: Text.AlignLeft
                text: "Версия"
                textFormat: Text.PlainText
                verticalAlignment: Text.AlignTop
                wrapMode: Text.WordWrap
            }
            Text {
                id: v1_2_3_

                x: 1
                y: 39

                height: 15
                width: 134

                color: "#000000"
                font.family: "Inter"
                font.pixelSize: 12
                font.weight: Font.Normal
                horizontalAlignment: Text.AlignLeft
                text: "v1.2.3 Обновлений нет"
                textFormat: Text.PlainText
                verticalAlignment: Text.AlignTop
                wrapMode: Text.WordWrap
            }
        }
