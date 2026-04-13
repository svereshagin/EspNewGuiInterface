import QtQuick
import QtQuick.Shapes

Item {
    id: root
    width: 829
    height: 646
    property var instanceInfo: null

    // Внешняя рамка блока
    Rectangle {
        id: rectangle_8243
        x: 13
        y: 97
        height: 137
        width: 800
        border.color: "#de2626"
        border.width: 1
        color: "transparent"
    }

    // Левая часть: Лицензия
    Text {
        id: element_2
        x: 26
        y: 105
        height: 19
        width: 80
        color: "#000000"
        font.family: "Inter"
        font.pixelSize: 16
        font.weight: Font.Bold
        text: "Лицензия"
    }

    Text {
        id: element_3
        x: 115
        y: 107
        height: 17
        width: 200          // расширили чтобы не переносилось
        color: "#000000"
        font.family: "Inter"
        font.pixelSize: 14
        font.weight: Font.Bold
        text: "Активна До 31.12.2027"
    }

    // Правая часть: Версия (с разделительной линией)
    Item {
        id: version
        x: 443
        y: 103
        height: 54
        width: 368

        Shape {
            id: line_2
            y: 20
            height: 2
            width: 368
            ShapePath {
                fillColor: "transparent"
                strokeColor: "#000000"
                strokeWidth: 1
                PathSvg { path: "M 0 0 L 368 0" }
            }
        }

        Text {
            id: element_4
            x: 1
            y: 0
            height: 18
            width: 100
            color: "#000000"
            font.family: "Inter"
            font.pixelSize: 15
            font.weight: Font.Bold
            text: "Версия"
        }

        Text {
            id: v1_2_3_
            x: 1
            y: 30
            height: 15
            width: 200
            color: "#000000"
            font.family: "Inter"
            font.pixelSize: 12
            text: "v1.2.3 Обновлений нет"
        }
    }

    // Нижний блок: ID + кнопка регистрации
    Item {
        id: group_4
        x: 26
        y: 139
        height: 87
        width: 256

        Text {
            id: iD_
            x: 10
            y: 9
            height: 19
            width: 22
            color: "#000000"
            font.family: "Inter"
            font.pixelSize: 16
            text: "ID:"
        }

        Text {
            id: element
            x: 10
            y: 28
            height: 19
            width: 135
            color: "#a39b9b"
            font.family: "Inter"
            font.pixelSize: 16
            text: "Нет информации"
        }

        // Кнопка (используем Rectangle вместо Shape — проще)
        Rectangle {
            x: 10
            y: 50
            height: 32
            width: 234
            color: "#ffffff"
            border.color: "#000000"
            border.width: 1

            Text {
                x: 4
                y: 7
                height: 19
                width: 226
                color: "#000000"
                font.family: "Inter"
                font.pixelSize: 16
                font.weight: Font.Bold
                text: "Зарегистрировать ТС ПИоТ"
            }
        }
    }
}