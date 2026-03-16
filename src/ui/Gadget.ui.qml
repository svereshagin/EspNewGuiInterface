import QtQuick
import QtQuick.Layouts

Rectangle {
    id: element

    height: 612
    width: 829

    border.color: "#f5f5f5"
    border.width: 4
    clip: true
    color: "#f5f5f5"
    radius: 16

    Item {
        id: frame_1171279320

        anchors.fill: parent  // Растягиваем на весь родитель
        anchors.margins: 5   // Небольшой отступ от границ

        FlexboxLayout {
            id: frame_1171279320Layout
            anchors.fill: parent


            alignItems: FlexboxLayout.AlignStart
            columnGap: 8
            direction: FlexboxLayout.Row
            justifyContent: FlexboxLayout.JustifyStart
            rowGap: 0

            Rectangle {
                id: frame_1171279315

                Layout.fillWidth: true
                border.color: "#8c8471"
                border.width: 1
                clip: true
                color: "#f5f5f5"
                implicitHeight: 556
                implicitWidth: 406

                FlexboxLayout {
                    id: frame_1171279315Layout

                    x: 0
                    y: 0

                    height: 556
                    width: 406

                    alignItems: FlexboxLayout.AlignStart
                    direction: FlexboxLayout.Column
                    justifyContent: FlexboxLayout.JustifyStart
                    rowGap: 8

                    Image {
                        id: unit

                        Layout.fillWidth: true
                        clip: true
                        source: Qt.resolvedUrl("assets/unit.png")

                        FlexboxLayout {
                            id: unitLayout

                            x: 16
                            y: 16

                            height: 148
                            width: 374

                            alignItems: FlexboxLayout.AlignStart
                            direction: FlexboxLayout.Column
                            justifyContent: FlexboxLayout.JustifyStart
                            rowGap: 16

                            Item {
                                id: frame_1171279325

                                implicitHeight: 26
                                implicitWidth: 118

                                FlexboxLayout {
                                    id: frame_1171279325Layout

                                    x: 0
                                    y: 0

                                    height: 26
                                    width: 118

                                    alignItems: FlexboxLayout.AlignCenter
                                    columnGap: 32
                                    direction: FlexboxLayout.Row
                                    justifyContent: FlexboxLayout.JustifyCenter
                                    rowGap: 0

                                    Item {
                                        id: frame_1171279327

                                        implicitHeight: 26
                                        implicitWidth: 118

                                        FlexboxLayout {
                                            id: frame_1171279327Layout

                                            x: 0
                                            y: 0

                                            height: 26
                                            width: 118

                                            alignItems: FlexboxLayout.AlignStart
                                            direction: FlexboxLayout.Column
                                            justifyContent: FlexboxLayout.JustifyCenter
                                            rowGap: 0

                                            Text {
                                                id: _item

                                                Layout.preferredHeight: 24
                                                Layout.preferredWidth: 118
                                                color: "#161e25"
                                                font.family: "Playfair Display"
                                                font.pixelSize: 18
                                                font.weight: Font.DemiBold
                                                horizontalAlignment: Text.AlignLeft
                                                lineHeight: 24
                                                lineHeightMode: Text.FixedHeight
                                                text: "Информация"
                                                textFormat: Text.PlainText
                                                verticalAlignment: Text.AlignTop
                                                wrapMode: Text.WordWrap
                                            }
                                            Rectangle {
                                                id: rectangle_8234

                                                Layout.fillWidth: true
                                                color: "#161e25"
                                                implicitHeight: 2
                                                implicitWidth: 118
                                            }
                                        }
                                    }
                                }
                            }
                            Rectangle {
                                id: comboBox_

                                color: "transparent"
                                implicitHeight: 32
                                implicitWidth: 297
                                radius: 4

                                FlexboxLayout {
                                    id: comboBox_Layout

                                    x: 1
                                    y: 1

                                    height: 30
                                    width: 295

                                    alignItems: FlexboxLayout.AlignStart
                                    direction: FlexboxLayout.Column
                                    justifyContent: FlexboxLayout.JustifyStart
                                    rowGap: 24

                                    Image {
                                        id: base_2

                                        Layout.fillWidth: true
                                        source: Qt.resolvedUrl("assets/base_1.png")

                                        FlexboxLayout {
                                            id: base_2Layout

                                            x: 11
                                            y: 4

                                            height: 22
                                            width: 273

                                            alignItems: FlexboxLayout.AlignCenter
                                            direction: FlexboxLayout.Row
                                            justifyContent: FlexboxLayout.JustifySpaceBetween
                                            rowGap: 0

                                            Item {
                                                id: text_Wrapper

                                                implicitHeight: 22
                                                implicitWidth: 107

                                                FlexboxLayout {
                                                    id: text_WrapperLayout

                                                    x: 0
                                                    y: 0

                                                    height: 20
                                                    width: 107

                                                    alignItems: FlexboxLayout.AlignStart
                                                    direction: FlexboxLayout.Column
                                                    justifyContent: FlexboxLayout.JustifyCenter
                                                    rowGap: 0

                                                    Text {
                                                        id: _text_1

                                                        Layout.preferredHeight: 20
                                                        Layout.preferredWidth: 107
                                                        color: "#161e25"
                                                        font.family: "Inter"
                                                        font.pixelSize: 15
                                                        font.weight: Font.Normal
                                                        horizontalAlignment: Text.AlignLeft
                                                        lineHeight: 20
                                                        lineHeightMode: Text.FixedHeight
                                                        text: "Модель кассы"
                                                        textFormat: Text.PlainText
                                                        verticalAlignment: Text.AlignTop
                                                        wrapMode: Text.WordWrap
                                                    }
                                                    Image {
                                                        id: min_Width_1

                                                        source: Qt.resolvedUrl("assets/min_Width_1.png")
                                                    }
                                                }
                                            }
                                            Item {
                                                id: chevronDownMed

                                                Layout.fillHeight: true
                                                implicitHeight: 22
                                                implicitWidth: 12

                                                FlexboxLayout {
                                                    id: chevronDownMedLayout

                                                    x: 0
                                                    y: 0

                                                    height: 22
                                                    width: 12

                                                    alignItems: FlexboxLayout.AlignCenter
                                                    direction: FlexboxLayout.Column
                                                    justifyContent: FlexboxLayout.JustifyCenter
                                                    rowGap: 10

                                                    Text {
                                                        id: chevronDownMed_1

                                                        Layout.preferredHeight: 12
                                                        Layout.preferredWidth: 12
                                                        color: "#9b000000"
                                                        font.family: "Segoe Fluent Icons"
                                                        font.pixelSize: 12
                                                        font.weight: Font.Normal
                                                        horizontalAlignment: Text.AlignHCenter
                                                        lineHeight: 12
                                                        lineHeightMode: Text.FixedHeight
                                                        text: ""
                                                        textFormat: Text.PlainText
                                                        verticalAlignment: Text.AlignVCenter
                                                    }
                                                }
                                            }
                                        }
                                    }
                                }
                            }
                            Text {
                                id: element_2

                                Layout.preferredHeight: 24
                                Layout.preferredWidth: 73
                                color: "#161e25"
                                font.family: "Segoe UI"
                                font.pixelSize: 15
                                font.weight: Font.Bold
                                horizontalAlignment: Text.AlignLeft
                                lineHeight: 24
                                lineHeightMode: Text.FixedHeight
                                text: "Обновить"
                                textFormat: Text.PlainText
                                verticalAlignment: Text.AlignTop
                                wrapMode: Text.WordWrap
                            }
                        }
                    }
                    Image {
                        id: unit_1

                        Layout.fillWidth: true
                        clip: true
                        source: Qt.resolvedUrl("assets/unit_1.png")

                        FlexboxLayout {
                            id: unit_1Layout

                            x: 0
                            y: 0

                            height: 164
                            width: 406

                            alignItems: FlexboxLayout.AlignStart
                            direction: FlexboxLayout.Column
                            justifyContent: FlexboxLayout.JustifyStart
                            rowGap: 8

                            Rectangle {
                                id: frame_1171279279

                                Layout.fillWidth: true
                                color: "#e5e1de"
                                implicitHeight: 40
                                implicitWidth: 406

                                FlexboxLayout {
                                    id: frame_1171279279Layout

                                    x: 16
                                    y: 8

                                    height: 24
                                    width: 374

                                    alignItems: FlexboxLayout.AlignStart
                                    columnGap: 8
                                    direction: FlexboxLayout.Row
                                    justifyContent: FlexboxLayout.JustifyStart
                                    rowGap: 0

                                    Text {
                                        id: element_3

                                        Layout.preferredHeight: 24
                                        Layout.preferredWidth: 183
                                        color: "#161e25"
                                        font.family: "Playfair Display"
                                        font.pixelSize: 18
                                        font.weight: Font.DemiBold
                                        horizontalAlignment: Text.AlignLeft
                                        lineHeight: 24
                                        lineHeightMode: Text.FixedHeight
                                        text: "Информация о кассе"
                                        textFormat: Text.PlainText
                                        verticalAlignment: Text.AlignTop
                                        wrapMode: Text.WordWrap
                                    }
                                }
                            }
                            Item {
                                id: frame_1171279317

                                Layout.fillWidth: true
                                implicitHeight: 48
                                implicitWidth: 406

                                FlexboxLayout {
                                    id: frame_1171279317Layout

                                    x: 16
                                    y: 0

                                    height: 48
                                    width: 374

                                    alignItems: FlexboxLayout.AlignStart
                                    columnGap: 8
                                    direction: FlexboxLayout.Row
                                    justifyContent: FlexboxLayout.JustifyStart
                                    rowGap: 0

                                    Item {
                                        id: frame_1171279276

                                        Layout.fillWidth: true
                                        implicitHeight: 48
                                        implicitWidth: 183

                                        FlexboxLayout {
                                            id: frame_1171279276Layout

                                            x: 0
                                            y: 0

                                            height: 48
                                            width: 183

                                            alignItems: FlexboxLayout.AlignStart
                                            direction: FlexboxLayout.Column
                                            justifyContent: FlexboxLayout.JustifyStart
                                            rowGap: 0

                                            Text {
                                                id: element_4

                                                Layout.preferredHeight: 24
                                                Layout.preferredWidth: 200
                                                color: "#5c6064"
                                                font.family: "Inter"
                                                font.pixelSize: 15
                                                font.weight: Font.Normal
                                                horizontalAlignment: Text.AlignLeft
                                                lineHeight: 24
                                                lineHeightMode: Text.FixedHeight
                                                text: "Модель:"
                                                textFormat: Text.PlainText
                                                verticalAlignment: Text.AlignTop
                                                wrapMode: Text.WordWrap
                                            }
                                            Text {
                                                id: element_5

                                                Layout.preferredHeight: 24
                                                Layout.preferredWidth: 70
                                                color: "#161e25"
                                                font.family: "Inter"
                                                font.pixelSize: 15
                                                font.weight: Font.Normal
                                                horizontalAlignment: Text.AlignLeft
                                                lineHeight: 24
                                                lineHeightMode: Text.FixedHeight
                                                text: "Атол 55Ф"
                                                textFormat: Text.PlainText
                                                verticalAlignment: Text.AlignTop
                                                wrapMode: Text.WordWrap
                                            }
                                        }
                                    }
                                    Item {
                                        id: frame_1171279282

                                        Layout.fillWidth: true
                                        implicitHeight: 48
                                        implicitWidth: 183

                                        FlexboxLayout {
                                            id: frame_1171279282Layout

                                            x: 0
                                            y: 0

                                            height: 48
                                            width: 183

                                            alignItems: FlexboxLayout.AlignStart
                                            direction: FlexboxLayout.Column
                                            justifyContent: FlexboxLayout.JustifyStart
                                            rowGap: 0

                                            Text {
                                                id: element_6

                                                Layout.preferredHeight: 24
                                                Layout.preferredWidth: 200
                                                color: "#5c6064"
                                                font.family: "Inter"
                                                font.pixelSize: 15
                                                font.weight: Font.Normal
                                                horizontalAlignment: Text.AlignLeft
                                                lineHeight: 24
                                                lineHeightMode: Text.FixedHeight
                                                text: "Смена:"
                                                textFormat: Text.PlainText
                                                verticalAlignment: Text.AlignTop
                                                wrapMode: Text.WordWrap
                                            }
                                            Item {
                                                id: frame_1171279288

                                                implicitHeight: 24
                                                implicitWidth: 69

                                                FlexboxLayout {
                                                    id: frame_1171279288Layout

                                                    x: 0
                                                    y: 0

                                                    height: 24
                                                    width: 69

                                                    alignItems: FlexboxLayout.AlignCenter
                                                    columnGap: 4
                                                    direction: FlexboxLayout.Row
                                                    justifyContent: FlexboxLayout.JustifyCenter
                                                    rowGap: 0

                                                    Item {
                                                        id: frame_1171279285

                                                        implicitHeight: 10
                                                        implicitWidth: 8

                                                        FlexboxLayout {
                                                            id: frame_1171279285Layout

                                                            x: 0
                                                            y: 2

                                                            height: 8
                                                            width: 8

                                                            alignItems: FlexboxLayout.AlignCenter
                                                            columnGap: 4
                                                            direction: FlexboxLayout.Row
                                                            justifyContent: FlexboxLayout.JustifyStart
                                                            rowGap: 0

                                                            Rectangle {
                                                                id: rectangle_8159

                                                                color: "#d02828"
                                                                implicitHeight: 8
                                                                implicitWidth: 8
                                                            }
                                                        }
                                                    }
                                                    Text {
                                                        id: element_7

                                                        Layout.preferredHeight: 24
                                                        Layout.preferredWidth: 57
                                                        color: "#161e25"
                                                        font.family: "Segoe UI"
                                                        font.pixelSize: 15
                                                        font.weight: Font.Normal
                                                        horizontalAlignment: Text.AlignLeft
                                                        lineHeight: 24
                                                        lineHeightMode: Text.FixedHeight
                                                        text: "Закрыта"
                                                        textFormat: Text.PlainText
                                                        verticalAlignment: Text.AlignTop
                                                        wrapMode: Text.WordWrap
                                                    }
                                                }
                                            }
                                        }
                                    }
                                }
                            }
                            Text {
                                id: element_8

                                Layout.fillWidth: true
                                Layout.preferredHeight: 24
                                Layout.preferredWidth: 406
                                color: "#161e25"
                                font.family: "Segoe UI"
                                font.pixelSize: 15
                                font.weight: Font.Bold
                                horizontalAlignment: Text.AlignHCenter
                                lineHeight: 24
                                lineHeightMode: Text.FixedHeight
                                text: "Подробнее"
                                textFormat: Text.PlainText
                                verticalAlignment: Text.AlignTop
                                wrapMode: Text.WordWrap
                            }
                        }
                    }
                    Image {
                        id: unit_2

                        Layout.fillWidth: true
                        clip: true
                        source: Qt.resolvedUrl("assets/unit_2.png")

                        FlexboxLayout {
                            id: unit_2Layout

                            x: 0
                            y: 0

                            height: 164
                            width: 406

                            alignItems: FlexboxLayout.AlignStart
                            direction: FlexboxLayout.Column
                            justifyContent: FlexboxLayout.JustifyStart
                            rowGap: 8

                            Rectangle {
                                id: frame_1171279324

                                Layout.fillWidth: true
                                color: "#e5e1de"
                                implicitHeight: 40
                                implicitWidth: 406

                                FlexboxLayout {
                                    id: frame_1171279324Layout

                                    x: 16
                                    y: 8

                                    height: 24
                                    width: 374

                                    alignItems: FlexboxLayout.AlignStart
                                    columnGap: 8
                                    direction: FlexboxLayout.Row
                                    justifyContent: FlexboxLayout.JustifyStart
                                    rowGap: 0

                                    Text {
                                        id: element_9

                                        Layout.preferredHeight: 24
                                        Layout.preferredWidth: 112
                                        color: "#161e25"
                                        font.family: "Playfair Display"
                                        font.pixelSize: 18
                                        font.weight: Font.DemiBold
                                        horizontalAlignment: Text.AlignLeft
                                        lineHeight: 24
                                        lineHeightMode: Text.FixedHeight
                                        text: "Кассовое ПО"
                                        textFormat: Text.PlainText
                                        verticalAlignment: Text.AlignTop
                                        wrapMode: Text.WordWrap
                                    }
                                }
                            }
                            Item {
                                id: frame_1171279323

                                Layout.fillWidth: true
                                implicitHeight: 48
                                implicitWidth: 406

                                FlexboxLayout {
                                    id: frame_1171279323Layout

                                    x: 16
                                    y: 0

                                    height: 48
                                    width: 374

                                    alignItems: FlexboxLayout.AlignStart
                                    columnGap: 8
                                    direction: FlexboxLayout.Row
                                    justifyContent: FlexboxLayout.JustifyStart
                                    rowGap: 0

                                    Item {
                                        id: frame_1171279277

                                        Layout.fillWidth: true
                                        implicitHeight: 48
                                        implicitWidth: 183

                                        FlexboxLayout {
                                            id: frame_1171279277Layout

                                            x: 0
                                            y: 0

                                            height: 48
                                            width: 183

                                            alignItems: FlexboxLayout.AlignStart
                                            direction: FlexboxLayout.Column
                                            justifyContent: FlexboxLayout.JustifyStart
                                            rowGap: 0

                                            Text {
                                                id: element_10

                                                Layout.fillWidth: true
                                                Layout.preferredHeight: 24
                                                Layout.preferredWidth: 183
                                                color: "#5c6064"
                                                font.family: "Inter"
                                                font.pixelSize: 15
                                                font.weight: Font.Normal
                                                horizontalAlignment: Text.AlignLeft
                                                lineHeight: 24
                                                lineHeightMode: Text.FixedHeight
                                                text: "Версия:"
                                                textFormat: Text.PlainText
                                                verticalAlignment: Text.AlignTop
                                                wrapMode: Text.WordWrap
                                            }
                                            Text {
                                                id: v4_08

                                                Layout.preferredHeight: 24
                                                Layout.preferredWidth: 40
                                                color: "#161e25"
                                                font.family: "Inter"
                                                font.pixelSize: 15
                                                font.weight: Font.Normal
                                                horizontalAlignment: Text.AlignLeft
                                                lineHeight: 24
                                                lineHeightMode: Text.FixedHeight
                                                text: "v4.08"
                                                textFormat: Text.PlainText
                                                verticalAlignment: Text.AlignTop
                                                wrapMode: Text.WordWrap
                                            }
                                        }
                                    }
                                    Item {
                                        id: frame_1171279278

                                        Layout.fillWidth: true
                                        implicitHeight: 48
                                        implicitWidth: 183

                                        FlexboxLayout {
                                            id: frame_1171279278Layout

                                            x: 0
                                            y: 0

                                            height: 48
                                            width: 183

                                            alignItems: FlexboxLayout.AlignStart
                                            direction: FlexboxLayout.Column
                                            justifyContent: FlexboxLayout.JustifyStart
                                            rowGap: 0

                                            Text {
                                                id: element_11

                                                Layout.fillWidth: true
                                                Layout.preferredHeight: 24
                                                Layout.preferredWidth: 183
                                                color: "#5c6064"
                                                font.family: "Inter"
                                                font.pixelSize: 15
                                                font.weight: Font.Normal
                                                horizontalAlignment: Text.AlignLeft
                                                lineHeight: 24
                                                lineHeightMode: Text.FixedHeight
                                                text: "Статус:"
                                                textFormat: Text.PlainText
                                                verticalAlignment: Text.AlignTop
                                                wrapMode: Text.WordWrap
                                            }
                                            Item {
                                                id: frame_1171279286

                                                implicitHeight: 24
                                                implicitWidth: 90

                                                FlexboxLayout {
                                                    id: frame_1171279286Layout

                                                    x: 0
                                                    y: 0

                                                    height: 24
                                                    width: 90

                                                    alignItems: FlexboxLayout.AlignCenter
                                                    columnGap: 8
                                                    direction: FlexboxLayout.Row
                                                    justifyContent: FlexboxLayout.JustifyCenter
                                                    rowGap: 0

                                                    Item {
                                                        id: frame_1171279287

                                                        implicitHeight: 10
                                                        implicitWidth: 8

                                                        FlexboxLayout {
                                                            id: frame_1171279287Layout

                                                            x: 0
                                                            y: 2

                                                            height: 8
                                                            width: 8

                                                            alignItems: FlexboxLayout.AlignCenter
                                                            columnGap: 4
                                                            direction: FlexboxLayout.Row
                                                            justifyContent: FlexboxLayout.JustifyStart
                                                            rowGap: 0

                                                            Rectangle {
                                                                id: rectangle_8160

                                                                color: "#1caa31"
                                                                implicitHeight: 8
                                                                implicitWidth: 8
                                                            }
                                                        }
                                                    }
                                                    Text {
                                                        id: element_12

                                                        Layout.preferredHeight: 24
                                                        Layout.preferredWidth: 74
                                                        color: "#161e25"
                                                        font.family: "Segoe UI"
                                                        font.pixelSize: 15
                                                        font.weight: Font.Normal
                                                        horizontalAlignment: Text.AlignLeft
                                                        lineHeight: 24
                                                        lineHeightMode: Text.FixedHeight
                                                        text: "Стабильно"
                                                        textFormat: Text.PlainText
                                                        verticalAlignment: Text.AlignTop
                                                        wrapMode: Text.WordWrap
                                                    }
                                                }
                                            }
                                        }
                                    }
                                }
                            }
                        }
                    }
                }
            }
            Rectangle {
                id: frame_1171279314

                Layout.fillWidth: true
                border.color: "#8c8471"
                border.width: 1
                clip: true
                color: "#f5f5f5"
                implicitHeight: 556
                implicitWidth: 406

                FlexboxLayout {
                    id: frame_1171279314Layout

                    x: 0
                    y: 0

                    height: 556
                    width: 406

                    alignItems: FlexboxLayout.AlignStart
                    direction: FlexboxLayout.Column
                    justifyContent: FlexboxLayout.JustifyStart
                    rowGap: 8

                    Image {
                        id: unit_3

                        Layout.fillWidth: true
                        clip: true
                        source: Qt.resolvedUrl("assets/unit_3.png")

                        FlexboxLayout {
                            id: unit_3Layout

                            x: 0
                            y: 0

                            height: 164
                            width: 406

                            alignItems: FlexboxLayout.AlignStart
                            direction: FlexboxLayout.Column
                            justifyContent: FlexboxLayout.JustifyStart
                            rowGap: 8

                            Rectangle {
                                id: frame_1171279326

                                Layout.fillWidth: true
                                color: "#e5e1de"
                                implicitHeight: 40
                                implicitWidth: 406

                                FlexboxLayout {
                                    id: frame_1171279326Layout

                                    x: 16
                                    y: 8

                                    height: 24
                                    width: 374

                                    alignItems: FlexboxLayout.AlignStart
                                    columnGap: 8
                                    direction: FlexboxLayout.Row
                                    justifyContent: FlexboxLayout.JustifyStart
                                    rowGap: 0

                                    Text {
                                        id: element_13

                                        Layout.preferredHeight: 24
                                        Layout.preferredWidth: 79
                                        color: "#161e25"
                                        font.family: "Playfair Display"
                                        font.pixelSize: 18
                                        font.weight: Font.DemiBold
                                        horizontalAlignment: Text.AlignLeft
                                        lineHeight: 24
                                        lineHeightMode: Text.FixedHeight
                                        text: "ТС ПИоТ"
                                        textFormat: Text.PlainText
                                        verticalAlignment: Text.AlignTop
                                        wrapMode: Text.WordWrap
                                    }
                                }
                            }
                            Item {
                                id: frame_1171279328

                                Layout.fillWidth: true
                                implicitHeight: 72
                                implicitWidth: 406

                                FlexboxLayout {
                                    id: frame_1171279328Layout

                                    x: 16
                                    y: 0

                                    height: 72
                                    width: 374

                                    alignItems: FlexboxLayout.AlignStart
                                    columnGap: 8
                                    direction: FlexboxLayout.Row
                                    justifyContent: FlexboxLayout.JustifyStart
                                    rowGap: 0

                                    Item {
                                        id: frame_1171279280

                                        Layout.fillWidth: true
                                        implicitHeight: 48
                                        implicitWidth: 183

                                        FlexboxLayout {
                                            id: frame_1171279280Layout

                                            x: 0
                                            y: 0

                                            height: 48
                                            width: 183

                                            alignItems: FlexboxLayout.AlignStart
                                            direction: FlexboxLayout.Column
                                            justifyContent: FlexboxLayout.JustifyStart
                                            rowGap: 0

                                            Text {
                                                id: element_14

                                                Layout.preferredHeight: 24
                                                Layout.preferredWidth: 200
                                                color: "#5c6064"
                                                font.family: "Inter"
                                                font.pixelSize: 15
                                                font.weight: Font.Normal
                                                horizontalAlignment: Text.AlignLeft
                                                lineHeight: 24
                                                lineHeightMode: Text.FixedHeight
                                                text: "Лицензия:"
                                                textFormat: Text.PlainText
                                                verticalAlignment: Text.AlignTop
                                                wrapMode: Text.WordWrap
                                            }
                                            Item {
                                                id: frame_1171279289

                                                Layout.fillWidth: true
                                                implicitHeight: 24
                                                implicitWidth: 183

                                                FlexboxLayout {
                                                    id: frame_1171279289Layout

                                                    x: 0
                                                    y: 0

                                                    height: 24
                                                    width: 183

                                                    alignItems: FlexboxLayout.AlignCenter
                                                    columnGap: 4
                                                    direction: FlexboxLayout.Row
                                                    justifyContent: FlexboxLayout.JustifyStart
                                                    rowGap: 0

                                                    Item {
                                                        id: frame_1171279290

                                                        implicitHeight: 10
                                                        implicitWidth: 8

                                                        FlexboxLayout {
                                                            id: frame_1171279290Layout

                                                            x: 0
                                                            y: 2

                                                            height: 8
                                                            width: 8

                                                            alignItems: FlexboxLayout.AlignCenter
                                                            columnGap: 8
                                                            direction: FlexboxLayout.Row
                                                            justifyContent: FlexboxLayout.JustifyStart
                                                            rowGap: 0

                                                            Rectangle {
                                                                id: rectangle_8161

                                                                color: "#1caa32"
                                                                implicitHeight: 8
                                                                implicitWidth: 8
                                                                radius: 2
                                                            }
                                                        }
                                                    }
                                                    Text {
                                                        id: element_15

                                                        Layout.preferredHeight: 24
                                                        Layout.preferredWidth: 153
                                                        color: "#161e25"
                                                        font.family: "Segoe UI"
                                                        font.pixelSize: 15
                                                        font.weight: Font.Normal
                                                        horizontalAlignment: Text.AlignLeft
                                                        lineHeight: 24
                                                        lineHeightMode: Text.FixedHeight
                                                        text: "Активна до 31.12.2027"
                                                        textFormat: Text.PlainText
                                                        verticalAlignment: Text.AlignTop
                                                        wrapMode: Text.WordWrap
                                                    }
                                                }
                                            }
                                        }
                                    }
                                    Item {
                                        id: frame_1171279281

                                        Layout.fillWidth: true
                                        implicitHeight: 72
                                        implicitWidth: 183

                                        FlexboxLayout {
                                            id: frame_1171279281Layout

                                            x: 0
                                            y: 0

                                            height: 72
                                            width: 183

                                            alignItems: FlexboxLayout.AlignStart
                                            direction: FlexboxLayout.Column
                                            justifyContent: FlexboxLayout.JustifyStart
                                            rowGap: 0

                                            Text {
                                                id: element_16

                                                Layout.preferredHeight: 24
                                                Layout.preferredWidth: 200
                                                color: "#5c6064"
                                                font.family: "Inter"
                                                font.pixelSize: 15
                                                font.weight: Font.Normal
                                                horizontalAlignment: Text.AlignLeft
                                                lineHeight: 24
                                                lineHeightMode: Text.FixedHeight
                                                text: "Версия:"
                                                textFormat: Text.PlainText
                                                verticalAlignment: Text.AlignTop
                                                wrapMode: Text.WordWrap
                                            }
                                            Text {
                                                id: v1_2_3

                                                Layout.preferredHeight: 24
                                                Layout.preferredWidth: 42
                                                color: "#161e25"
                                                font.family: "Inter"
                                                font.pixelSize: 15
                                                font.weight: Font.Normal
                                                horizontalAlignment: Text.AlignLeft
                                                lineHeight: 24
                                                lineHeightMode: Text.FixedHeight
                                                text: "v1.2.3"
                                                textFormat: Text.PlainText
                                                verticalAlignment: Text.AlignTop
                                                wrapMode: Text.WordWrap
                                            }
                                            Text {
                                                id: element_17

                                                Layout.preferredHeight: 24
                                                Layout.preferredWidth: 120
                                                color: "#5c6064"
                                                font.family: "Inter"
                                                font.pixelSize: 15
                                                font.weight: Font.Normal
                                                horizontalAlignment: Text.AlignLeft
                                                lineHeight: 24
                                                lineHeightMode: Text.FixedHeight
                                                text: "Обновлений нет"
                                                textFormat: Text.PlainText
                                                verticalAlignment: Text.AlignTop
                                                wrapMode: Text.WordWrap
                                            }
                                        }
                                    }
                                }
                            }
                            Text {
                                id: element_18

                                Layout.fillWidth: true
                                Layout.preferredHeight: 24
                                Layout.preferredWidth: 406
                                color: "#161e25"
                                font.family: "Segoe UI"
                                font.pixelSize: 15
                                font.weight: Font.Bold
                                horizontalAlignment: Text.AlignHCenter
                                lineHeight: 24
                                lineHeightMode: Text.FixedHeight
                                text: "Подробнее"
                                textFormat: Text.PlainText
                                verticalAlignment: Text.AlignTop
                                wrapMode: Text.WordWrap
                            }
                        }
                    }
                    Image {
                        id: unit_4

                        Layout.fillWidth: true
                        clip: true
                        source: Qt.resolvedUrl("assets/unit_4.png")

                        FlexboxLayout {
                            id: unit_4Layout

                            x: 0
                            y: 0

                            height: 164
                            width: 406

                            alignItems: FlexboxLayout.AlignStart
                            direction: FlexboxLayout.Column
                            justifyContent: FlexboxLayout.JustifyStart
                            rowGap: 8

                            Rectangle {
                                id: frame_1171279329

                                Layout.fillWidth: true
                                color: "#e5e1de"
                                implicitHeight: 40
                                implicitWidth: 406

                                FlexboxLayout {
                                    id: frame_1171279329Layout

                                    x: 16
                                    y: 8

                                    height: 24
                                    width: 374

                                    alignItems: FlexboxLayout.AlignStart
                                    columnGap: 8
                                    direction: FlexboxLayout.Row
                                    justifyContent: FlexboxLayout.JustifyStart
                                    rowGap: 0

                                    Text {
                                        id: element_19

                                        Layout.preferredHeight: 24
                                        Layout.preferredWidth: 57
                                        color: "#161e25"
                                        font.family: "Playfair Display"
                                        font.pixelSize: 18
                                        font.weight: Font.DemiBold
                                        horizontalAlignment: Text.AlignLeft
                                        lineHeight: 24
                                        lineHeightMode: Text.FixedHeight
                                        text: "ЛМ ЧЗ"
                                        textFormat: Text.PlainText
                                        verticalAlignment: Text.AlignTop
                                        wrapMode: Text.WordWrap
                                    }
                                }
                            }
                            Item {
                                id: frame_1171279322

                                Layout.fillWidth: true
                                implicitHeight: 48
                                implicitWidth: 406

                                FlexboxLayout {
                                    id: frame_1171279322Layout

                                    x: 16
                                    y: 0

                                    height: 48
                                    width: 374

                                    alignItems: FlexboxLayout.AlignStart
                                    columnGap: 8
                                    direction: FlexboxLayout.Row
                                    justifyContent: FlexboxLayout.JustifyStart
                                    rowGap: 0

                                    Item {
                                        id: frame_1171279283

                                        Layout.fillWidth: true
                                        implicitHeight: 48
                                        implicitWidth: 183

                                        FlexboxLayout {
                                            id: frame_1171279283Layout

                                            x: 0
                                            y: 0

                                            height: 48
                                            width: 183

                                            alignItems: FlexboxLayout.AlignStart
                                            direction: FlexboxLayout.Column
                                            justifyContent: FlexboxLayout.JustifyStart
                                            rowGap: 0

                                            Text {
                                                id: element_20

                                                Layout.preferredHeight: 24
                                                Layout.preferredWidth: 200
                                                color: "#5c6064"
                                                font.family: "Inter"
                                                font.pixelSize: 15
                                                font.weight: Font.Normal
                                                horizontalAlignment: Text.AlignLeft
                                                lineHeight: 24
                                                lineHeightMode: Text.FixedHeight
                                                text: "Статус:"
                                                textFormat: Text.PlainText
                                                verticalAlignment: Text.AlignTop
                                                wrapMode: Text.WordWrap
                                            }
                                            Item {
                                                id: frame_1171279284

                                                implicitHeight: 24
                                                implicitWidth: 86

                                                FlexboxLayout {
                                                    id: frame_1171279284Layout

                                                    x: 0
                                                    y: 0

                                                    height: 24
                                                    width: 86

                                                    alignItems: FlexboxLayout.AlignCenter
                                                    columnGap: 4
                                                    direction: FlexboxLayout.Row
                                                    justifyContent: FlexboxLayout.JustifyCenter
                                                    rowGap: 0

                                                    Item {
                                                        id: frame_1171279291

                                                        implicitHeight: 10
                                                        implicitWidth: 8

                                                        FlexboxLayout {
                                                            id: frame_1171279291Layout

                                                            x: 0
                                                            y: 2

                                                            height: 8
                                                            width: 8

                                                            alignItems: FlexboxLayout.AlignCenter
                                                            columnGap: 8
                                                            direction: FlexboxLayout.Row
                                                            justifyContent: FlexboxLayout.JustifyStart
                                                            rowGap: 0

                                                            Rectangle {
                                                                id: rectangle_8162

                                                                color: "#1caa32"
                                                                implicitHeight: 8
                                                                implicitWidth: 8
                                                            }
                                                        }
                                                    }
                                                    Text {
                                                        id: element_21

                                                        Layout.preferredHeight: 24
                                                        Layout.preferredWidth: 74
                                                        color: "#161e25"
                                                        font.family: "Segoe UI"
                                                        font.pixelSize: 15
                                                        font.weight: Font.Normal
                                                        horizontalAlignment: Text.AlignLeft
                                                        lineHeight: 24
                                                        lineHeightMode: Text.FixedHeight
                                                        text: "Стабильно"
                                                        textFormat: Text.PlainText
                                                        verticalAlignment: Text.AlignTop
                                                        wrapMode: Text.WordWrap
                                                    }
                                                }
                                            }
                                        }
                                    }
                                    Item {
                                        id: frame_1171279292

                                        Layout.fillWidth: true
                                        implicitHeight: 48
                                        implicitWidth: 183

                                        FlexboxLayout {
                                            id: frame_1171279292Layout

                                            x: 0
                                            y: 0

                                            height: 48
                                            width: 183

                                            alignItems: FlexboxLayout.AlignStart
                                            direction: FlexboxLayout.Column
                                            justifyContent: FlexboxLayout.JustifyStart
                                            rowGap: 0

                                            Text {
                                                id: element_22

                                                Layout.preferredHeight: 24
                                                Layout.preferredWidth: 200
                                                color: "#5c6064"
                                                font.family: "Inter"
                                                font.pixelSize: 15
                                                font.weight: Font.Normal
                                                horizontalAlignment: Text.AlignLeft
                                                lineHeight: 24
                                                lineHeightMode: Text.FixedHeight
                                                text: "Версия:"
                                                textFormat: Text.PlainText
                                                verticalAlignment: Text.AlignTop
                                                wrapMode: Text.WordWrap
                                            }
                                            Text {
                                                id: v1_02

                                                Layout.preferredHeight: 24
                                                Layout.preferredWidth: 37
                                                color: "#161e25"
                                                font.family: "Inter"
                                                font.pixelSize: 15
                                                font.weight: Font.Normal
                                                horizontalAlignment: Text.AlignLeft
                                                lineHeight: 24
                                                lineHeightMode: Text.FixedHeight
                                                text: "v1.02"
                                                textFormat: Text.PlainText
                                                verticalAlignment: Text.AlignTop
                                                wrapMode: Text.WordWrap
                                            }
                                        }
                                    }
                                }
                            }
                            Item {
                                id: frame_1171279321

                                Layout.fillWidth: true
                                implicitHeight: 72
                                implicitWidth: 406

                                FlexboxLayout {
                                    id: frame_1171279321Layout

                                    x: 16
                                    y: 0

                                    height: 72
                                    width: 374

                                    alignItems: FlexboxLayout.AlignStart
                                    columnGap: 8
                                    direction: FlexboxLayout.Row
                                    justifyContent: FlexboxLayout.JustifyStart
                                    rowGap: 0

                                    Item {
                                        id: frame_1171279293

                                        Layout.fillWidth: true
                                        implicitHeight: 72
                                        implicitWidth: 183

                                        FlexboxLayout {
                                            id: frame_1171279293Layout

                                            x: 0
                                            y: 0

                                            height: 72
                                            width: 183

                                            alignItems: FlexboxLayout.AlignStart
                                            direction: FlexboxLayout.Column
                                            justifyContent: FlexboxLayout.JustifyStart
                                            rowGap: 0

                                            Text {
                                                id: iP_

                                                Layout.preferredHeight: 24
                                                Layout.preferredWidth: 200
                                                color: "#5c6064"
                                                font.family: "Inter"
                                                font.pixelSize: 15
                                                font.weight: Font.Normal
                                                horizontalAlignment: Text.AlignLeft
                                                lineHeight: 24
                                                lineHeightMode: Text.FixedHeight
                                                text: "IP:"
                                                textFormat: Text.PlainText
                                                verticalAlignment: Text.AlignTop
                                                wrapMode: Text.WordWrap
                                            }
                                            Text {
                                                id: element_23

                                                Layout.preferredHeight: 24
                                                Layout.preferredWidth: 118
                                                color: "#161e25"
                                                font.family: "Inter"
                                                font.pixelSize: 15
                                                font.weight: Font.Normal
                                                horizontalAlignment: Text.AlignLeft
                                                lineHeight: 24
                                                lineHeightMode: Text.FixedHeight
                                                text: "127/0/0/1:50063"
                                                textFormat: Text.PlainText
                                                verticalAlignment: Text.AlignTop
                                                wrapMode: Text.WordWrap
                                            }
                                            Text {
                                                id: element_24

                                                Layout.preferredHeight: 24
                                                Layout.preferredWidth: 123
                                                color: "#161e25"
                                                font.family: "Segoe UI"
                                                font.pixelSize: 15
                                                font.weight: Font.Bold
                                                horizontalAlignment: Text.AlignLeft
                                                lineHeight: 24
                                                lineHeightMode: Text.FixedHeight
                                                text: "Настроить адрес"
                                                textFormat: Text.PlainText
                                                verticalAlignment: Text.AlignTop
                                                wrapMode: Text.WordWrap
                                            }
                                        }
                                    }
                                    Item {
                                        id: frame_1171279294

                                        Layout.fillWidth: true
                                        implicitHeight: 72
                                        implicitWidth: 183

                                        FlexboxLayout {
                                            id: frame_1171279294Layout

                                            x: 0
                                            y: 0

                                            height: 72
                                            width: 183

                                            alignItems: FlexboxLayout.AlignStart
                                            direction: FlexboxLayout.Column
                                            justifyContent: FlexboxLayout.JustifyStart
                                            rowGap: 0

                                            Text {
                                                id: element_25

                                                Layout.preferredHeight: 48
                                                Layout.preferredWidth: 200
                                                color: "#5c6064"
                                                font.family: "Inter"
                                                font.pixelSize: 15
                                                font.weight: Font.Normal
                                                horizontalAlignment: Text.AlignLeft
                                                lineHeight: 24
                                                lineHeightMode: Text.FixedHeight
                                                text: "Последняя синхронизация:"
                                                textFormat: Text.PlainText
                                                verticalAlignment: Text.AlignTop
                                                wrapMode: Text.WordWrap
                                            }
                                            Text {
                                                id: element_26

                                                Layout.preferredHeight: 24
                                                Layout.preferredWidth: 125
                                                color: "#161e25"
                                                font.family: "Inter"
                                                font.pixelSize: 15
                                                font.weight: Font.Normal
                                                horizontalAlignment: Text.AlignLeft
                                                lineHeight: 24
                                                lineHeightMode: Text.FixedHeight
                                                text: "20.02.2025 14:30"
                                                textFormat: Text.PlainText
                                                verticalAlignment: Text.AlignTop
                                                wrapMode: Text.WordWrap
                                            }
                                        }
                                    }
                                }
                            }
                        }
                    }
                    Image {
                        id: unit_5

                        Layout.fillWidth: true
                        clip: true
                        source: Qt.resolvedUrl("assets/unit_5.png")

                        FlexboxLayout {
                            id: unit_5Layout

                            x: 0
                            y: 0

                            height: 164
                            width: 406

                            alignItems: FlexboxLayout.AlignStart
                            direction: FlexboxLayout.Column
                            justifyContent: FlexboxLayout.JustifyStart
                            rowGap: 8

                            Rectangle {
                                id: frame_1171279330

                                Layout.fillWidth: true
                                color: "#e5e1de"
                                implicitHeight: 40
                                implicitWidth: 406

                                FlexboxLayout {
                                    id: frame_1171279330Layout

                                    x: 16
                                    y: 8

                                    height: 24
                                    width: 374

                                    alignItems: FlexboxLayout.AlignStart
                                    columnGap: 8
                                    direction: FlexboxLayout.Row
                                    justifyContent: FlexboxLayout.JustifyStart
                                    rowGap: 0

                                    Text {
                                        id: element_27

                                        Layout.preferredHeight: 24
                                        Layout.preferredWidth: 70
                                        color: "#161e25"
                                        font.family: "Playfair Display"
                                        font.pixelSize: 18
                                        font.weight: Font.DemiBold
                                        horizontalAlignment: Text.AlignLeft
                                        lineHeight: 24
                                        lineHeightMode: Text.FixedHeight
                                        text: "ГИС МТ"
                                        textFormat: Text.PlainText
                                        verticalAlignment: Text.AlignTop
                                        wrapMode: Text.WordWrap
                                    }
                                }
                            }
                            Item {
                                id: frame_1171279331

                                Layout.fillWidth: true
                                implicitHeight: 72
                                implicitWidth: 406

                                FlexboxLayout {
                                    id: frame_1171279331Layout

                                    x: 16
                                    y: 0

                                    height: 72
                                    width: 374

                                    alignItems: FlexboxLayout.AlignStart
                                    columnGap: 8
                                    direction: FlexboxLayout.Row
                                    justifyContent: FlexboxLayout.JustifyStart
                                    rowGap: 0

                                    Item {
                                        id: frame_1171279295

                                        Layout.fillWidth: true
                                        implicitHeight: 72
                                        implicitWidth: 183

                                        FlexboxLayout {
                                            id: frame_1171279295Layout

                                            x: 0
                                            y: 0

                                            height: 72
                                            width: 183

                                            alignItems: FlexboxLayout.AlignStart
                                            direction: FlexboxLayout.Column
                                            justifyContent: FlexboxLayout.JustifyStart
                                            rowGap: 0

                                            Text {
                                                id: element_28

                                                Layout.fillWidth: true
                                                Layout.preferredHeight: 48
                                                Layout.preferredWidth: 183
                                                color: "#5c6064"
                                                font.family: "Inter"
                                                font.pixelSize: 15
                                                font.weight: Font.Normal
                                                horizontalAlignment: Text.AlignLeft
                                                lineHeight: 24
                                                lineHeightMode: Text.FixedHeight
                                                text: "Последняя синхронизация:"
                                                textFormat: Text.PlainText
                                                verticalAlignment: Text.AlignTop
                                                wrapMode: Text.WordWrap
                                            }
                                            Text {
                                                id: element_29

                                                Layout.preferredHeight: 24
                                                Layout.preferredWidth: 125
                                                color: "#161e25"
                                                font.family: "Inter"
                                                font.pixelSize: 15
                                                font.weight: Font.Normal
                                                horizontalAlignment: Text.AlignLeft
                                                lineHeight: 24
                                                lineHeightMode: Text.FixedHeight
                                                text: "20.02.2025 14:30"
                                                textFormat: Text.PlainText
                                                verticalAlignment: Text.AlignTop
                                                wrapMode: Text.WordWrap
                                            }
                                        }
                                    }
                                    Item {
                                        id: frame_1171279296

                                        Layout.fillWidth: true
                                        implicitHeight: 48
                                        implicitWidth: 183

                                        FlexboxLayout {
                                            id: frame_1171279296Layout

                                            x: 0
                                            y: 0

                                            height: 48
                                            width: 183

                                            alignItems: FlexboxLayout.AlignStart
                                            direction: FlexboxLayout.Column
                                            justifyContent: FlexboxLayout.JustifyStart
                                            rowGap: 0

                                            Text {
                                                id: element_30

                                                Layout.fillWidth: true
                                                Layout.preferredHeight: 24
                                                Layout.preferredWidth: 183
                                                color: "#5c6064"
                                                font.family: "Inter"
                                                font.pixelSize: 15
                                                font.weight: Font.Normal
                                                horizontalAlignment: Text.AlignLeft
                                                lineHeight: 24
                                                lineHeightMode: Text.FixedHeight
                                                text: "Статус:"
                                                textFormat: Text.PlainText
                                                verticalAlignment: Text.AlignTop
                                                wrapMode: Text.WordWrap
                                            }
                                            Item {
                                                id: frame_1171279297

                                                implicitHeight: 24
                                                implicitWidth: 86

                                                FlexboxLayout {
                                                    id: frame_1171279297Layout

                                                    x: 0
                                                    y: 0

                                                    height: 24
                                                    width: 86

                                                    alignItems: FlexboxLayout.AlignCenter
                                                    columnGap: 4
                                                    direction: FlexboxLayout.Row
                                                    justifyContent: FlexboxLayout.JustifyCenter
                                                    rowGap: 0

                                                    Item {
                                                        id: frame_1171279298

                                                        implicitHeight: 10
                                                        implicitWidth: 8

                                                        FlexboxLayout {
                                                            id: frame_1171279298Layout

                                                            x: 0
                                                            y: 2

                                                            height: 8
                                                            width: 8

                                                            alignItems: FlexboxLayout.AlignCenter
                                                            columnGap: 8
                                                            direction: FlexboxLayout.Row
                                                            justifyContent: FlexboxLayout.JustifyStart
                                                            rowGap: 0

                                                            Rectangle {
                                                                id: rectangle_8163

                                                                color: "#1caa32"
                                                                implicitHeight: 8
                                                                implicitWidth: 8
                                                                radius: 2
                                                            }
                                                        }
                                                    }
                                                    Text {
                                                        id: element_31

                                                        Layout.preferredHeight: 24
                                                        Layout.preferredWidth: 74
                                                        color: "#161e25"
                                                        font.family: "Segoe UI"
                                                        font.pixelSize: 15
                                                        font.weight: Font.Normal
                                                        horizontalAlignment: Text.AlignLeft
                                                        lineHeight: 24
                                                        lineHeightMode: Text.FixedHeight
                                                        text: "Стабильно"
                                                        textFormat: Text.PlainText
                                                        verticalAlignment: Text.AlignTop
                                                        wrapMode: Text.WordWrap
                                                    }
                                                }
                                            }
                                        }
                                    }
                                }
                            }
                        }
                    }
                }
            }
        }
    }
}