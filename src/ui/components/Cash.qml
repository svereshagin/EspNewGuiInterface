// src/qml/components/KktCard.qml
import QtQuick 2.15
import QtQuick.Controls 2.15
import QtQuick.Layouts 1.15

Rectangle {
    id: root

    // Свойства для данных ККТ
    property string kktSerial: ""
    property string fnSerial: ""
    property string kktInn: ""
    property string kktRnm: ""
    property string modelName: ""
    property string dkktVersion: ""
    property string developer: ""
    property string manufacturer: ""
    property string shiftState: ""

    // Дополнительные свойства для UI
    property bool isSelected: false
    property int cardWidth: 300
    property int cardHeight: 200

    width: cardWidth
    height: cardHeight

    // Закруглённые углы
    radius: 10

    // Цвет фона (зависит от выбора)
    color: isSelected ? "#e3f2fd" : "#ffffff"

    // Тень
    border.color: isSelected ? "#2196f3" : "#cccccc"
    border.width: isSelected ? 2 : 1

    // Эффект при наведении
    MouseArea {
        anchors.fill: parent
        hoverEnabled: true
        cursorShape: Qt.PointingHandCursor

        onEntered: {
            parent.color = isSelected ? "#e3f2fd" : "#f5f5f5"
        }
        onExited: {
            parent.color = isSelected ? "#e3f2fd" : "#ffffff"
        }
        onClicked: {
            // При клике устанавливаем текущую кассу
            AppStorage.set_current_cash(kktSerial)
        }
    }

    // Содержимое карточки
    ColumnLayout {
        anchors.fill: parent
        anchors.margins: 10
        spacing: 5

        // Заголовок - серийный номер
        Rectangle {
            Layout.fillWidth: true
            height: 40
            color: isSelected ? "#2196f3" : "#4caf50"
            radius: 5

            Text {
                anchors.centerIn: parent
                text: kktSerial
                color: "white"
                font.bold: true
                font.pixelSize: 14
                elide: Text.ElideRight
                width: parent.width - 20
            }
        }

        // Информация о кассе
        GridLayout {
            Layout.fillWidth: true
            columns: 2
            columnSpacing: 10
            rowSpacing: 5

            Text { text: "ИНН:"; font.bold: true; color: "#666" }
            Text { text: kktInn; elide: Text.ElideRight; Layout.fillWidth: true }

            Text { text: "ФН:"; font.bold: true; color: "#666" }
            Text { text: fnSerial; elide: Text.ElideRight; Layout.fillWidth: true }

            Text { text: "Модель:"; font.bold: true; color: "#666" }
            Text { text: modelName; elide: Text.ElideRight; Layout.fillWidth: true }

            Text { text: "Версия:"; font.bold: true; color: "#666" }
            Text { text: dkktVersion; elide: Text.ElideRight; Layout.fillWidth: true }

            Text { text: "Производитель:"; font.bold: true; color: "#666" }
            Text { text: manufacturer; elide: Text.ElideRight; Layout.fillWidth: true }

            Text { text: "Статус смены:"; font.bold: true; color: "#666" }
            Rectangle {
                Layout.fillWidth: true
                height: 24
                radius: 12
                color: shiftState === "Открыта" ? "#4caf50" :
                       shiftState === "Закрыта" ? "#f44336" : "#ff9800"

                Text {
                    anchors.centerIn: parent
                    text: shiftState || "Неизвестно"
                    color: "white"
                    font.pixelSize: 11
                }
            }
        }

        // Нижняя панель с кнопками (опционально)
        RowLayout {
            Layout.fillWidth: true
            Layout.topMargin: 5
            visible: isSelected

            Button {
                text: "Выбрать"
                Layout.fillWidth: true
                onClicked: {
                    AppStorage.set_current_cash(kktSerial)
                }
            }
        }
    }

    // Индикатор выбора (галочка)
    Rectangle {
        visible: isSelected
        width: 24
        height: 24
        radius: 12
        color: "#2196f3"
        anchors.top: parent.top
        anchors.right: parent.right
        anchors.margins: 5

        Text {
            anchors.centerIn: parent
            text: "✓"
            color: "white"
            font.bold: true
            font.pixelSize: 16
        }
    }
}