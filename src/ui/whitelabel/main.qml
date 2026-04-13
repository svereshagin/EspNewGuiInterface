import QtQuick
import QtQuick.Shapes
import "components"



Window {
    width: 829
    height: 646
    visible: true
    title: "EspNewGuiInterface"


    ToolBar {
        x: 0
        y: 0
        width: parent.width
        height: 70
        z: 1
    }

    TSPIOT {
        x: 0
        y: 0
        width: parent.width
        height: 70
        z: 1
        instanceInfo: null
    }

    Rectangle {
        id: frame_1171279325

        height: 646
        width: 829

        clip: true
        color: "#ffffff"
        radius: 2

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
        Image {
            id: image_97

            x: 19
            y: 101

            source: Qt.resolvedUrl("assets/image_97.png")
        }
        Rectangle {
            id: rectangle_8251

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

            Rectangle {
                id: rectangle_8249

                height: 87
                width: 256

                color: "#ffffff"
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
                id: element_1

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
        Shape {
            id: rectangle_8250

            x: 260
            y: 541

            height: 37
            width: 155

            ShapePath {
                id: rectangle_8250_ShapePath0

                fillColor: "#ffffff"
                fillRule: ShapePath.WindingFill
                strokeColor: "#000000"
                strokeWidth: 1

                PathSvg {
                    id: rectangle_8250_ShapePath0_PathSvg0

                    path: "M 0 0 L 155 0 L 155 37 L 0 37 L 0 0 Z"
                }
            }
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
        Image {
            id: image_99

            x: 24
            y: 244

            source: Qt.resolvedUrl("assets/image_99.png")
        }
        Text {
            id: element_7

            x: 91
            y: 256

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
            id: element_8

            x: 311
            y: 258

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
        Item {
            id: group_6

            x: 444
            y: 258

            height: 53
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
                id: element_9

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
                id: element_10

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
        }
        Text {
            id: element_11

            x: 601
            y: 293

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
            id: element_12

            x: 671
            y: 258

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
        Item {
            id: group_7

            x: 90
            y: 297

            height: 40
            width: 134

            Text {
                id: element_13

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
                id: element_14

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
        Text {
            id: element_15

            x: 93
            y: 350

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
            id: element_16

            x: 92
            y: 371

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
            id: element_17

            x: 260
            y: 298

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
            id: element_18

            x: 259
            y: 319

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

            x: 444
            y: 319

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
            id: element_20

            x: 601
            y: 319

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
        Rectangle {
            id: rectangle_8255

            x: 15
            y: 447

            height: 194
            width: 798

            border.color: "#de2626"
            border.width: 1
            color: "transparent"
        }
        Text {
            id: element_21

            x: 91
            y: 461

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
            id: element_22

            x: 310
            y: 463

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
            id: group_8

            x: 442.93
            y: 463.25

            height: 71.96
            width: 367.58

            Shape {
                id: line_4

                y: 30.02

                height: 0.01
                width: 367.58

                rotation: 0.18

                ShapePath {
                    id: line_4_ShapePath0

                    fillColor: "#00000000"
                    strokeColor: "#000000"
                    strokeWidth: 1

                    PathSvg {
                        id: line_4_ShapePath0_PathSvg0

                        path: "M 0 0 L 367.5792236328125 0.007825706154108047"
                    }
                }
            }
            Text {
                id: element_23

                x: 1

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
                id: element_24

                x: 1.99
                y: 34.82

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
        }
        Text {
            id: element_25

            x: 669
            y: 463

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
        Item {
            id: group_9

            x: 92
            y: 501

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
        Text {
            id: iP_

            x: 260
            y: 501

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
            id: element_28

            x: 260
            y: 522

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
            id: element_29

            x: 445
            y: 535

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
            id: element_30

            x: 93
            y: 570

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
            id: element_31

            x: 92
            y: 594

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
        Image {
            id: image_98

            x: 22
            y: 447

            source: Qt.resolvedUrl("assets/image_98.png")
        }
        Text {
            id: element_32

            x: 267
            y: 550

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
    }


    Component.onCompleted: AppStorage.load_kkt()

    Connections {
        target: AppStorage
        function onKktListChanged() {
            console.log("kktList обновлён:", AppStorage.kktList.length)
        }

        function onInstanceStatusChanged(instanceId, info) {
             console.log("Keys:", Object.keys(info))
            console.log(info.licenses[0].isActive)
            console.log("Keys:", Object.keys(info.licenses))
            console.log("state:", info.state)
            console.log("version:", info.version)
            console.log("port:", info.clientPort)
            console.log("inn:", info.regData.kktInn)
            console.log("license active:", info.licenses[0].isActive)
        }
    }
}