import QtQuick
import QtQuick.Shapes

Rectangle {
    id: element

    height: 646
    width: 829

    clip: true
    color: "#ffffff"
    radius: 2

    Rectangle {
        id: tSPIOTRectanle

        x: 13
        y: 97

        height: 137
        width: 800

        border.color: "#de2626"
        border.width: 1
        color: "transparent"
    }
    Rectangle {
        id: toolBarRectangle

        x: 11
        y: 4

        height: 78
        width: 800

        border.color: "#de2626"
        border.width: 1
        color: "transparent"
    }
    Rectangle {
        id: cashRectangle

        x: 15
        y: 244

        height: 167
        width: 800

        border.color: "#de2626"
        border.width: 1
        color: "transparent"
    }
    Item {
        id: group_4

        x: 82
        y: 139

        height: 87
        width: 256

        Item {
            id: registrateTSPIOT

            height: 87
            width: 256

            Rectangle {
                id: rectangle_8249

                height: 87
                width: 256

                color: "#ffffff"
            }
            Text {
                id: iD_

                x: 10
                y: 9

                height: 19
                width: 22

                color: "#000000"
                font.family: "Inter"
                font.pixelSize: 16
                font.weight: Font.Normal
                horizontalAlignment: Text.AlignLeft
                text: "ID:"
                textFormat: Text.PlainText
                verticalAlignment: Text.AlignTop
                wrapMode: Text.WordWrap
            }
            Text {
                id: element_1

                x: 10
                y: 28

                height: 19
                width: 135

                color: "#a39b9b"
                font.family: "Inter"
                font.pixelSize: 16
                font.weight: Font.Normal
                horizontalAlignment: Text.AlignLeft
                text: "Нет информации"
                textFormat: Text.PlainText
                verticalAlignment: Text.AlignTop
                wrapMode: Text.WordWrap
            }
            Shape {
                id: rectangle_8248

                x: 10
                y: 50

                height: 32
                width: 234

                ShapePath {
                    id: rectangle_8248_ShapePath0

                    fillColor: "#ffffff"
                    fillRule: ShapePath.WindingFill
                    strokeColor: "#000000"
                    strokeWidth: 1

                    PathSvg {
                        id: rectangle_8248_ShapePath0_PathSvg0

                        path: "M 0 0 L 234 0 L 234 32 L 0 32 L 0 0 Z"
                    }
                }
            }
            Text {
                id: element_2

                x: 14
                y: 57

                height: 19
                width: 226

                color: "#000000"
                font.family: "Inter"
                font.pixelSize: 16
                font.weight: Font.Bold
                horizontalAlignment: Text.AlignLeft
                text: "Зарегистрировать ТС ПИоТ"
                textFormat: Text.PlainText
                verticalAlignment: Text.AlignTop
                wrapMode: Text.WordWrap
            }
        }
    }
    Item {
        id: tSPIOT_LICENCE

        x: 78
        y: 105

        height: 32
        width: 360

        Rectangle {
            id: rectangle_8254

            height: 32
            width: 360

            color: "#ffffff"
        }
        Item {
            id: license_and_status

            x: 16
            y: 6

            height: 19
            width: 255

            Text {
                id: element_3

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
                id: element_4

                x: 95

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
        }
        Image {
            id: line_2

            x: 1
            y: 32

            source: Qt.resolvedUrl("assets/line_2.png")
        }
    }
    Item {
        id: version

        x: 443
        y: 111

        height: 54
        width: 368.50

        Shape {
            id: line_3

            y: 26

            height: 0.01
            width: 368.50

            rotation: 0.15

            ShapePath {
                id: line_3_ShapePath0

                fillColor: "#00000000"
                strokeColor: "#000000"
                strokeWidth: 1

                PathSvg {
                    id: line_3_ShapePath0_PathSvg0

                    path: "M 0 0 L 368.5 0.006742153316736221"
                }
            }
        }
        Text {
            id: element_5

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
    Item {
        id: group_5

        x: 13
        y: 23

        height: 39
        width: 296

        Rectangle {
            id: rectangle_8250

            height: 39
            width: 296

            border.color: "#000000"
            border.width: 1
            color: "#ffffff"
        }
        Text {
            id: element_6

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
        id: rectangle_8251

        x: 324
        y: 23

        height: 39
        width: 148

        border.color: "#000000"
        border.width: 1
        color: "#ffffff"
    }
    Text {
        id: element_7

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
    Item {
        id: kKTINFO

        x: 80
        y: 256

        height: 28
        width: 359

        Text {
            id: element_8

            x: 11

            height: 19
            width: 106

            color: "#000000"
            font.family: "Inter"
            font.pixelSize: 16
            font.weight: Font.Bold
            horizontalAlignment: Text.AlignLeft
            text: "Информация"
            textFormat: Text.PlainText
            verticalAlignment: Text.AlignTop
            wrapMode: Text.WordWrap
        }
        Text {
            id: element_9

            x: 231
            y: 2

            height: 17
            width: 107

            color: "#000000"
            font.family: "Inter"
            font.pixelSize: 14
            font.weight: Font.Normal
            horizontalAlignment: Text.AlignLeft
            text: "Смена открыта"
            textFormat: Text.PlainText
            verticalAlignment: Text.AlignTop
            wrapMode: Text.WordWrap
        }
        Image {
            id: line_4

            y: 28

            source: Qt.resolvedUrl("assets/line_3.png")
        }
    }
    Item {
        id: kKTModel

        x: 90
        y: 297

        height: 40
        width: 134

        Text {
            id: element_10

            x: 1

            height: 19
            width: 67

            color: "#000000"
            font.family: "Inter"
            font.pixelSize: 16
            font.weight: Font.Normal
            horizontalAlignment: Text.AlignLeft
            text: "Модель:"
            textFormat: Text.PlainText
            verticalAlignment: Text.AlignTop
            wrapMode: Text.WordWrap
        }
        Text {
            id: element_11

            y: 21

            height: 19
            width: 135

            color: "#a39b9b"
            font.family: "Inter"
            font.pixelSize: 16
            font.weight: Font.Normal
            horizontalAlignment: Text.AlignLeft
            text: "Нет информации"
            textFormat: Text.PlainText
            verticalAlignment: Text.AlignTop
            wrapMode: Text.WordWrap
        }
    }
    Item {
        id: kKTFN

        x: 92
        y: 350

        height: 40
        width: 134

        Text {
            id: element_12

            x: 1

            height: 19
            width: 30

            color: "#000000"
            font.family: "Inter"
            font.pixelSize: 16
            font.weight: Font.Normal
            horizontalAlignment: Text.AlignLeft
            text: "ФН:"
            textFormat: Text.PlainText
            verticalAlignment: Text.AlignTop
            wrapMode: Text.WordWrap
        }
        Text {
            id: element_13

            y: 21

            height: 19
            width: 135

            color: "#a39b9b"
            font.family: "Inter"
            font.pixelSize: 16
            font.weight: Font.Normal
            horizontalAlignment: Text.AlignLeft
            text: "Нет информации"
            textFormat: Text.PlainText
            verticalAlignment: Text.AlignTop
            wrapMode: Text.WordWrap
        }
    }
    Item {
        id: kKTINN

        x: 259
        y: 298

        height: 40
        width: 134

        Text {
            id: kKTINN_1

            x: 1

            height: 19
            width: 42

            color: "#000000"
            font.family: "Inter"
            font.pixelSize: 16
            font.weight: Font.Normal
            horizontalAlignment: Text.AlignLeft
            text: "ИНН:"
            textFormat: Text.PlainText
            verticalAlignment: Text.AlignTop
            wrapMode: Text.WordWrap
        }
        Text {
            id: kKTINN_2

            y: 21

            height: 19
            width: 135

            color: "#a39b9b"
            font.family: "Inter"
            font.pixelSize: 16
            font.weight: Font.Normal
            horizontalAlignment: Text.AlignLeft
            text: "Нет информации"
            textFormat: Text.PlainText
            verticalAlignment: Text.AlignTop
            wrapMode: Text.WordWrap
        }
    }
    Item {
        id: cashPO

        x: 444
        y: 258

        height: 80
        width: 368.50

        Shape {
            id: line_5

            y: 26

            height: 0.01
            width: 368.50

            rotation: 0.15

            ShapePath {
                id: line_5_ShapePath0

                fillColor: "#00000000"
                strokeColor: "#000000"
                strokeWidth: 1

                PathSvg {
                    id: line_5_ShapePath0_PathSvg0

                    path: "M 0 0 L 368.5 0.006742153316736221"
                }
            }
        }
        Text {
            id: element_14

            x: 1

            height: 18
            width: 101

            color: "#000000"
            font.family: "Inter"
            font.pixelSize: 15
            font.weight: Font.Bold
            horizontalAlignment: Text.AlignLeft
            text: "Кассовое ПО"
            textFormat: Text.PlainText
            verticalAlignment: Text.AlignTop
            wrapMode: Text.WordWrap
        }
        Text {
            id: element_15

            x: 2
            y: 38

            height: 15
            width: 98

            color: "#000000"
            font.family: "Inter"
            font.pixelSize: 12
            font.weight: Font.Normal
            horizontalAlignment: Text.AlignLeft
            text: "Наименование"
            textFormat: Text.PlainText
            verticalAlignment: Text.AlignTop
            wrapMode: Text.WordWrap
        }
        Text {
            id: element_16

            x: 157
            y: 35

            height: 15
            width: 98

            color: "#000000"
            font.family: "Inter"
            font.pixelSize: 12
            font.weight: Font.Normal
            horizontalAlignment: Text.AlignLeft
            text: "Версия:"
            textFormat: Text.PlainText
            verticalAlignment: Text.AlignTop
            wrapMode: Text.WordWrap
        }
        Text {
            id: element_17

            x: 227

            height: 18
            width: 95

            color: "#000000"
            font.family: "Inter"
            font.pixelSize: 15
            font.weight: Font.Normal
            horizontalAlignment: Text.AlignLeft
            text: "Подключено"
            textFormat: Text.PlainText
            verticalAlignment: Text.AlignTop
            wrapMode: Text.WordWrap
        }
        Text {
            id: element_18

            y: 61

            height: 19
            width: 135

            color: "#a39b9b"
            font.family: "Inter"
            font.pixelSize: 16
            font.weight: Font.Normal
            horizontalAlignment: Text.AlignLeft
            text: "Нет информации"
            textFormat: Text.PlainText
            verticalAlignment: Text.AlignTop
            wrapMode: Text.WordWrap
        }
        Text {
            id: element_19

            x: 157
            y: 61

            height: 19
            width: 135

            color: "#a39b9b"
            font.family: "Inter"
            font.pixelSize: 16
            font.weight: Font.Normal
            horizontalAlignment: Text.AlignLeft
            text: "Нет информации"
            textFormat: Text.PlainText
            verticalAlignment: Text.AlignTop
            wrapMode: Text.WordWrap
        }
    }
    Item {
        id: lM_AND_GISMT

        x: 15
        y: 447

        height: 194
        width: 798

        Shape {
            id: rectangle_8252

            x: 245
            y: 94

            height: 37
            width: 155

            ShapePath {
                id: rectangle_8252_ShapePath0

                fillColor: "#ffffff"
                fillRule: ShapePath.WindingFill
                strokeColor: "#000000"
                strokeWidth: 1

                PathSvg {
                    id: rectangle_8252_ShapePath0_PathSvg0

                    path: "M 0 0 L 155 0 L 155 37 L 0 37 L 0 0 Z"
                }
            }
        }
        Rectangle {
            id: rectangle_8253

            height: 194
            width: 798

            border.color: "#de2626"
            border.width: 1
            color: "transparent"
        }
        Text {
            id: element_20

            x: 76
            y: 14

            height: 22
            width: 54

            color: "#000000"
            font.family: "Inter"
            font.pixelSize: 16
            font.weight: Font.Bold
            horizontalAlignment: Text.AlignLeft
            text: "ЛМ ЧЗ"
            textFormat: Text.PlainText
            verticalAlignment: Text.AlignTop
        }
        Text {
            id: element_21

            x: 295
            y: 16

            height: 20
            width: 81

            color: "#000000"
            font.family: "Inter"
            font.pixelSize: 14
            font.weight: Font.Normal
            horizontalAlignment: Text.AlignLeft
            text: "Установлен"
            textFormat: Text.PlainText
            verticalAlignment: Text.AlignTop
        }
        Item {
            id: gISMT

            x: 427.93
            y: 16

            height: 94
            width: 367.58

            Shape {
                id: line_6

                y: 30.27

                height: 0.01
                width: 367.58

                rotation: 0.18

                ShapePath {
                    id: line_6_ShapePath0

                    fillColor: "#00000000"
                    strokeColor: "#000000"
                    strokeWidth: 1

                    PathSvg {
                        id: line_6_ShapePath0_PathSvg0

                        path: "M 0 0 L 367.5792236328125 0.007825706154108047"
                    }
                }
            }
            Text {
                id: element_22

                x: 1
                y: 0.25

                height: 20.89
                width: 59.85

                color: "#000000"
                font.family: "Inter"
                font.pixelSize: 15
                font.weight: Font.Bold
                horizontalAlignment: Text.AlignLeft
                text: "ГИС МТ"
                textFormat: Text.PlainText
                verticalAlignment: Text.AlignTop
            }
            Text {
                id: element_23

                x: 1.99
                y: 35.07

                height: 37.14
                width: 140.65

                color: "#000000"
                font.family: "Inter"
                font.pixelSize: 13
                font.weight: Font.Normal
                horizontalAlignment: Text.AlignLeft
                text: "Последняя синхронизация:"
                textFormat: Text.PlainText
                verticalAlignment: Text.AlignTop
            }
            Text {
                id: element_24

                x: 2.07
                y: 72

                height: 22
                width: 135

                color: "#a39b9b"
                font.family: "Inter"
                font.pixelSize: 16
                font.weight: Font.Normal
                horizontalAlignment: Text.AlignLeft
                text: "Нет информации"
                textFormat: Text.PlainText
                verticalAlignment: Text.AlignTop
            }
            Text {
                id: element_25

                x: 226.07

                height: 21
                width: 130

                color: "#000000"
                font.family: "Inter"
                font.pixelSize: 15
                font.weight: Font.Normal
                horizontalAlignment: Text.AlignLeft
                text: "Сервер доступен"
                textFormat: Text.PlainText
                verticalAlignment: Text.AlignTop
            }
        }
        Item {
            id: lM_CZ_LAST_SYNC

            x: 77
            y: 54

            height: 59.05
            width: 134.66

            Text {
                id: element_26

                height: 44.11
                width: 130.68

                color: "#000000"
                font.family: "Inter"
                font.pixelSize: 14
                font.weight: Font.Normal
                horizontalAlignment: Text.AlignLeft
                text: "Последняя
синхронизация:"
                textFormat: Text.PlainText
                verticalAlignment: Text.AlignTop
                wrapMode: Text.WordWrap
            }
            Text {
                id: element_27

                x: 1
                y: 37

                height: 22.05
                width: 134.66

                color: "#a39b9b"
                font.family: "Inter"
                font.pixelSize: 16
                font.weight: Font.Normal
                horizontalAlignment: Text.AlignLeft
                text: "Нет информации"
                textFormat: Text.PlainText
                verticalAlignment: Text.AlignTop
            }
        }
        Item {
            id: lM_IP

            x: 245
            y: 54

            height: 44
            width: 134

            Text {
                id: lM_IP_1

                height: 44
                width: 20

                color: "#000000"
                font.family: "Inter"
                font.pixelSize: 16
                font.weight: Font.Normal
                horizontalAlignment: Text.AlignLeft
                text: "IP:
"
                textFormat: Text.PlainText
                verticalAlignment: Text.AlignTop
                wrapMode: Text.WordWrap
            }
            Text {
                id: lM_IP_2

                y: 21

                height: 22
                width: 135

                color: "#a39b9b"
                font.family: "Inter"
                font.pixelSize: 16
                font.weight: Font.Normal
                horizontalAlignment: Text.AlignLeft
                text: "Нет информации"
                textFormat: Text.PlainText
                verticalAlignment: Text.AlignTop
            }
        }
        Item {
            id: lM_CZ_VERSION

            x: 77
            y: 123

            height: 46
            width: 135

            Text {
                id: element_28

                x: 1

                height: 22
                width: 63

                color: "#000000"
                font.family: "Inter"
                font.pixelSize: 16
                font.weight: Font.Normal
                horizontalAlignment: Text.AlignLeft
                text: "Версия:"
                textFormat: Text.PlainText
                verticalAlignment: Text.AlignTop
            }
            Text {
                id: element_29

                y: 24

                height: 22
                width: 136

                color: "#a39b9b"
                font.family: "Inter"
                font.pixelSize: 16
                font.weight: Font.Normal
                horizontalAlignment: Text.AlignLeft
                text: "Нет информации"
                textFormat: Text.PlainText
                verticalAlignment: Text.AlignTop
            }
        }
        Text {
            id: element_30

            x: 252
            y: 103

            height: 22
            width: 142

            color: "#000000"
            font.family: "Inter"
            font.pixelSize: 16
            font.weight: Font.Bold
            horizontalAlignment: Text.AlignLeft
            text: "Настроить адрес"
            textFormat: Text.PlainText
            verticalAlignment: Text.AlignTop
        }
        Image {
            id: line_7

            x: 66
            y: 47

            source: Qt.resolvedUrl("assets/line_4.png")
        }
    }
    Item {
        id: tSPIoT_RectangleName

        x: 15
        y: 101

        height: 130
        width: 51

        Rectangle {
            id: rectangle_8255

            height: 130
            width: 51

            color: "#ffffff"
        }
        Text {
            id: element_31

            x: -9.50
            y: 55.50

            height: 19
            width: 71

            color: "#000000"
            font.family: "Inter"
            font.pixelSize: 16
            font.weight: Font.Bold
            horizontalAlignment: Text.AlignLeft
            rotation: -90
            text: "ТС ПИоТ"
            textFormat: Text.PlainText
            verticalAlignment: Text.AlignTop
            wrapMode: Text.WordWrap
        }
        Image {
            id: line_8

            x: -14
            y: 65

            rotation: -90
            source: Qt.resolvedUrl("assets/line_5.png")
        }
    }
    Item {
        id: tSPIoT_RectangleName_1

        x: 20
        y: 485

        height: 130
        width: 51

        Rectangle {
            id: rectangle_8256

            height: 130
            width: 51

            color: "#ffffff"
        }
        Text {
            id: element_32

            x: -3
            y: 62

            height: 19
            width: 58

            color: "#000000"
            font.family: "Inter"
            font.pixelSize: 16
            font.weight: Font.Bold
            horizontalAlignment: Text.AlignLeft
            rotation: -90
            text: "Статус"
            textFormat: Text.PlainText
            verticalAlignment: Text.AlignTop
            wrapMode: Text.WordWrap
        }
        Image {
            id: line_9

            x: -14
            y: 65

            rotation: -90
            source: Qt.resolvedUrl("assets/line_6.png")
        }
    }
    Item {
        id: tSPIoT_RectangleName_2

        x: 20
        y: 258

        height: 130
        width: 51

        Rectangle {
            id: rectangle_8257

            height: 130
            width: 51

            color: "#ffffff"
        }
        Text {
            id: element_33

            x: 1
            y: 66

            height: 19
            width: 50

            color: "#000000"
            font.family: "Inter"
            font.pixelSize: 16
            font.weight: Font.Bold
            horizontalAlignment: Text.AlignLeft
            rotation: -90
            text: "Касса"
            textFormat: Text.PlainText
            verticalAlignment: Text.AlignTop
            wrapMode: Text.WordWrap
        }
        Image {
            id: line_10

            x: -14
            y: 65

            rotation: -90
            source: Qt.resolvedUrl("assets/line_7.png")
        }
    }
}