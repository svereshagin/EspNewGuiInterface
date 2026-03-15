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

    Rectangle {
        id: header

        height: 48
        width: 829

        clip: true
        color: "#f5f5f5"

        Image {
            id: image_89

            x: 16
            y: 12

            source: Qt.resolvedUrl("assets/image_89.png")
        }
        Text {
            id: element_1

            x: 56
            y: 12

            height: 24
            width: 80

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
        Rectangle {
            id: parts_Title_Bar_Caption_Control_Group

            x: 685

            height: 48
            width: 144

            color: "transparent"
            topRightRadius: 7

            FlexboxLayout {
                id: parts_Title_Bar_Caption_Control_GroupLayout

                x: 0
                y: 0

                height: 48
                width: 144

                alignItems: FlexboxLayout.AlignStart
                columnGap: 0
                direction: FlexboxLayout.Row
                justifyContent: FlexboxLayout.JustifyEnd
                rowGap: 0

                Image {
                    id: parts_Title_Bar_Caption_Control_Button

                    source: Qt.resolvedUrl("assets/parts_Title_Bar_Caption_Control_Button.png")
                    visible: false
                }
                Image {
                    id: parts_Title_Bar_Caption_Control_Button_1

                    source: Qt.resolvedUrl("assets/parts_Title_Bar_Caption_Control_Button_1.png")
                    visible: false
                }
                Item {
                    id: identity

                    implicitHeight: 48
                    implicitWidth: 48
                    visible: false

                    Item {
                        id: parts_Title_Bar_Identity

                        x: 12
                        y: 12

                        height: 24
                        width: 24

                        Image {
                            id: person_Picture_Person_Picture

                            source: Qt.resolvedUrl("assets/person_Picture_Person_Picture.png")
                        }
                        Rectangle {
                            id: parts_Title_Bar_Identity_Menu

                            x: -135
                            y: 32

                            height: 314
                            width: 282

                            color: "transparent"
                            radius: 8
                            visible: false

                            FlexboxLayout {
                                id: parts_Title_Bar_Identity_MenuLayout

                                x: 0
                                y: 0

                                height: 314
                                width: 282

                                alignItems: FlexboxLayout.AlignStart
                                direction: FlexboxLayout.Column
                                justifyContent: FlexboxLayout.JustifyStart
                                rowGap: 0

                                Item {
                                    id: surface_Flyout_Surface

                                    Layout.fillWidth: true
                                    implicitHeight: 314
                                    implicitWidth: 282

                                    FlexboxLayout {
                                        id: surface_Flyout_SurfaceLayout

                                        x: 1
                                        y: 1

                                        height: 312
                                        width: 280

                                        alignItems: FlexboxLayout.AlignStart
                                        direction: FlexboxLayout.Column
                                        justifyContent: FlexboxLayout.JustifyStart
                                        rowGap: 0

                                        Rectangle {
                                            id: flyout_Base_Stroke_

                                            Layout.fillWidth: true
                                            border.color: "#0f000000"
                                            border.width: 1
                                            color: "transparent"
                                            implicitHeight: 312
                                            implicitWidth: 280
                                            radius: 7

                                            FlexboxLayout {
                                                id: flyout_Base_Stroke_Layout

                                                x: 0
                                                y: 0

                                                height: 312
                                                width: 280

                                                alignItems: FlexboxLayout.AlignStart
                                                direction: FlexboxLayout.Column
                                                justifyContent: FlexboxLayout.JustifyStart
                                                rowGap: 0

                                                Image {
                                                    id: flyout_Base_Shadow_

                                                    Layout.fillWidth: true
                                                    source: Qt.resolvedUrl("assets/flyout_Base_Shadow_.png")

                                                    FlexboxLayout {
                                                        id: flyout_Base_Shadow_Layout

                                                        x: 0
                                                        y: 0

                                                        height: 312
                                                        width: 280

                                                        alignItems: FlexboxLayout.AlignStart
                                                        direction: FlexboxLayout.Column
                                                        justifyContent: FlexboxLayout.JustifyStart
                                                        rowGap: 0

                                                        Image {
                                                            id: flyout_Base_Fill_

                                                            Layout.fillWidth: true
                                                            source: Qt.resolvedUrl("assets/flyout_Base_Fill_.png")

                                                            FlexboxLayout {
                                                                id: flyout_Base_Fill_Layout

                                                                x: 0
                                                                y: 0

                                                                height: 312
                                                                width: 280

                                                                alignItems: FlexboxLayout.AlignStart
                                                                direction: FlexboxLayout.Column
                                                                justifyContent: FlexboxLayout.JustifyStart
                                                                rowGap: 0

                                                                Item {
                                                                    id: list_Items

                                                                    Layout.fillWidth: true
                                                                    implicitHeight: 312
                                                                    implicitWidth: 280

                                                                    FlexboxLayout {
                                                                        id: list_ItemsLayout

                                                                        x: 0
                                                                        y: 2

                                                                        height: 308
                                                                        width: 280

                                                                        alignItems: FlexboxLayout.AlignStart
                                                                        direction: FlexboxLayout.Column
                                                                        justifyContent: FlexboxLayout.JustifyStart
                                                                        rowGap: 0

                                                                        Image {
                                                                            id: flyout_Menu_Flyout_Menu_Subheader

                                                                            Layout.fillWidth: true
                                                                            source: Qt.resolvedUrl("assets/flyout_Menu_Flyout_Menu_Subheader.png")
                                                                        }
                                                                        Item {
                                                                            id: custom_List_Item

                                                                            Layout.fillWidth: true
                                                                            implicitHeight: 40
                                                                            implicitWidth: 280

                                                                            Image {
                                                                                id: list_Item_List_Item

                                                                                source: Qt.resolvedUrl("assets/list_Item_List_Item.png")
                                                                            }
                                                                            Image {
                                                                                id: person_Picture_Person_Picture_1

                                                                                x: 12
                                                                                y: 8

                                                                                source: Qt.resolvedUrl("assets/person_Picture_Person_Picture_1.png")
                                                                            }
                                                                        }
                                                                        Item {
                                                                            id: custom_List_Item_1

                                                                            Layout.fillWidth: true
                                                                            implicitHeight: 40
                                                                            implicitWidth: 280

                                                                            Image {
                                                                                id: list_Item_List_Item_1

                                                                                source: Qt.resolvedUrl("assets/list_Item_List_Item_1.png")
                                                                            }
                                                                            Image {
                                                                                id: person_Picture_Person_Picture_2

                                                                                x: 12
                                                                                y: 8

                                                                                source: Qt.resolvedUrl("assets/person_Picture_Person_Picture_2.png")
                                                                            }
                                                                        }
                                                                        Item {
                                                                            id: custom_List_Item_2

                                                                            Layout.fillWidth: true
                                                                            implicitHeight: 40
                                                                            implicitWidth: 280

                                                                            Image {
                                                                                id: list_Item_List_Item_2

                                                                                source: Qt.resolvedUrl("assets/list_Item_List_Item_2.png")
                                                                            }
                                                                            Image {
                                                                                id: person_Picture_Person_Picture_3

                                                                                x: 12
                                                                                y: 8

                                                                                source: Qt.resolvedUrl("assets/person_Picture_Person_Picture_3.png")
                                                                            }
                                                                        }
                                                                        Item {
                                                                            id: custom_List_Item_3

                                                                            Layout.fillWidth: true
                                                                            implicitHeight: 40
                                                                            implicitWidth: 280

                                                                            Image {
                                                                                id: list_Item_List_Item_3

                                                                                source: Qt.resolvedUrl("assets/list_Item_List_Item_3.png")
                                                                            }
                                                                            Image {
                                                                                id: person_Picture_Person_Picture_4

                                                                                x: 12
                                                                                y: 8

                                                                                source: Qt.resolvedUrl("assets/person_Picture_Person_Picture_4.png")
                                                                            }
                                                                        }
                                                                        Item {
                                                                            id: footer

                                                                            Layout.fillWidth: true
                                                                            implicitHeight: 108
                                                                            implicitWidth: 280

                                                                            FlexboxLayout {
                                                                                id: footerLayout

                                                                                x: 0
                                                                                y: 4

                                                                                height: 104
                                                                                width: 280

                                                                                alignItems: FlexboxLayout.AlignStart
                                                                                direction: FlexboxLayout.Column
                                                                                justifyContent: FlexboxLayout.JustifyStart
                                                                                rowGap: 0

                                                                                Image {
                                                                                    id: flyout_Menu_Flyout_Menu_Divider

                                                                                    Layout.fillWidth: true
                                                                                    source: Qt.resolvedUrl("assets/flyout_Menu_Flyout_Menu_Divider.png")
                                                                                }
                                                                                Item {
                                                                                    id: button_Wrapper

                                                                                    Layout.fillWidth: true
                                                                                    implicitHeight: 100
                                                                                    implicitWidth: 280

                                                                                    FlexboxLayout {
                                                                                        id: button_WrapperLayout

                                                                                        x: 16
                                                                                        y: 14

                                                                                        height: 72
                                                                                        width: 248

                                                                                        alignItems: FlexboxLayout.AlignStart
                                                                                        direction: FlexboxLayout.Column
                                                                                        justifyContent: FlexboxLayout.JustifyStart
                                                                                        rowGap: 8

                                                                                        Image {
                                                                                            id: button_Button

                                                                                            Layout.fillWidth: true
                                                                                            source: Qt.resolvedUrl("assets/button_Button.png")
                                                                                        }
                                                                                        Rectangle {
                                                                                            id: button_Button_1

                                                                                            Layout.fillWidth: true
                                                                                            color: "transparent"
                                                                                            implicitHeight: 32
                                                                                            implicitWidth: 248
                                                                                            radius: 4

                                                                                            FlexboxLayout {
                                                                                                id: button_Button_1Layout

                                                                                                x: 1
                                                                                                y: 1

                                                                                                height: 30
                                                                                                width: 246

                                                                                                alignItems: FlexboxLayout.AlignCenter
                                                                                                direction: FlexboxLayout.Column
                                                                                                justifyContent: FlexboxLayout.JustifyCenter
                                                                                                rowGap: 0

                                                                                                Image {
                                                                                                    id: base

                                                                                                    Layout.fillHeight: true
                                                                                                    Layout.fillWidth: true
                                                                                                    source: Qt.resolvedUrl("assets/base.png")

                                                                                                    FlexboxLayout {
                                                                                                        id: baseLayout

                                                                                                        x: 11
                                                                                                        y: 4

                                                                                                        height: 20
                                                                                                        width: 224

                                                                                                        alignItems: FlexboxLayout.AlignCenter
                                                                                                        direction: FlexboxLayout.Column
                                                                                                        justifyContent: FlexboxLayout.JustifyCenter
                                                                                                        rowGap: 0

                                                                                                        Image {
                                                                                                            id: min_Width

                                                                                                            source: Qt.resolvedUrl("assets/min_Width.png")
                                                                                                        }
                                                                                                        Text {
                                                                                                            id: _text

                                                                                                            Layout.preferredHeight: 20
                                                                                                            Layout.preferredWidth: 52
                                                                                                            color: "#e4000000"
                                                                                                            font.family: "Segoe UI Variable"
                                                                                                            font.pixelSize: 14
                                                                                                            font.weight: Font.Normal
                                                                                                            horizontalAlignment: Text.AlignHCenter
                                                                                                            lineHeight: 20
                                                                                                            lineHeightMode: Text.FixedHeight
                                                                                                            text: "Sign out"
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
                                                }
                                            }
                                        }
                                    }
                                }
                            }
                        }
                    }
                }
                Item {
                    id: parts_Title_Bar_Caption_Control_Button_2

                    implicitHeight: 48
                    implicitWidth: 48

                    Rectangle {
                        id: base_1

                        height: 48
                        width: 48

                        color: "#00ffffff"
                    }
                    Text {
                        id: icon

                        x: 16
                        y: 16

                        height: 16
                        width: 17

                        color: "#e4000000"
                        font.family: "Segoe Fluent Icons"
                        font.pixelSize: 10
                        font.weight: Font.Normal
                        horizontalAlignment: Text.AlignHCenter
                        lineHeight: 16
                        lineHeightMode: Text.FixedHeight
                        text: ""
                        textFormat: Text.PlainText
                        verticalAlignment: Text.AlignVCenter
                    }
                }
                Image {
                    id: parts_Title_Bar_Caption_Control_Button_3

                    source: Qt.resolvedUrl("assets/parts_Title_Bar_Caption_Control_Button_2.png")
                }
                Image {
                    id: parts_Title_Bar_Caption_Control_Button_4

                    source: Qt.resolvedUrl("assets/parts_Title_Bar_Caption_Control_Button_3.png")
                }
            }
        }
    }
    Item {
        id: frame_1171279320

        x: 5
        y: 48

        height: 556
        width: 820

        FlexboxLayout {
            id: frame_1171279320Layout

            x: 0
            y: 0

            height: 556
            width: 820

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