import QtQuick 2.15
import QtQuick.Controls 2.15
import QtQuick.Layouts 1.15
import QtQuick.Controls.Material 2.15

ApplicationWindow {
    id: root
    visible: true
    width: 600
    height: 500
    title: "Управление кассами"

    Material.theme: Material.Light
    Material.accent: Material.Blue

    // Подключаемся к контроллеру из Python
    property var kktController: KKTController {}

    ColumnLayout {
        anchors.fill: parent
        anchors.margins: 15
        spacing: 15

        // Верхняя панель с заголовком и кнопкой обновления
        RowLayout {
            Layout.fillWidth: true
            spacing: 10

            Label {
                text: "Доступные кассы"
                font.pixelSize: 22
                font.bold: true
                color: Material.primary
            }

            Item { Layout.fillWidth: true }

            // Индикатор загрузки
            BusyIndicator {
                id: busyIndicator
                running: false
                visible: running
                Layout.preferredWidth: 30
                Layout.preferredHeight: 30
            }

            // Кнопка обновления
            Button {
                text: "Обновить"
                icon.source: "qrc:/icons/refresh.png"
                icon.width: 16
                icon.height: 16
                enabled: !busyIndicator.running
                onClicked: updateKktList()

                // Встроенная иконка если нет файла
                contentItem: RowLayout {
                    spacing: 5
                    Text {
                        text: "⟳"
                        font.pixelSize: 16
                        color: enabled ? Material.primary : Material.hintTextColor
                    }
                    Text {
                        text: "Обновить"
                        font.pixelSize: 14
                        color: enabled ? Material.primary : Material.hintTextColor
                    }
                }
            }
        }

        // Статистика по кассам
        RowLayout {
            Layout.fillWidth: true
            visible: kktListModel.count > 0

            Rectangle {
                Layout.fillWidth: true
                Layout.preferredHeight: 40
                color: "#f0f0f0"
                radius: 5

                RowLayout {
                    anchors.fill: parent
                    anchors.margins: 5
                    spacing: 15

                    Label {
                        text: "Всего касс: " + kktListModel.count
                        font.pixelSize: 13
                        color: "#666"
                    }

                    Rectangle {
                        width: 1
                        height: 20
                        color: "#ccc"
                    }

                    Label {
                        text: "Открытых смен: " + openedShiftsCount
                        font.pixelSize: 13
                        color: openedShiftsCount > 0 ? "green" : "#666"
                    }

                    Rectangle {
                        width: 1
                        height: 20
                        color: "#ccc"
                    }

                    Label {
                        text: "Истекших смен: " + expiredShiftsCount
                        font.pixelSize: 13
                        color: expiredShiftsCount > 0 ? "red" : "#666"
                    }
                }
            }
        }

        // Выпадающий список касс
        ComboBox {
            id: kktComboBox
            Layout.fillWidth: true
            Layout.preferredHeight: 50
            model: ListModel {
                id: kktListModel
            }

            // Кастомный делегат для отображения
            delegate: ItemDelegate {
                width: kktComboBox.width
                contentItem: ColumnLayout {
                    spacing: 2

                    RowLayout {
                        Layout.fillWidth: true
                        spacing: 5

                        Text {
                            text: "🖥️"
                            font.pixelSize: 14
                        }

                        Text {
                            text: model.kktSerial || "Н/Д"
                            font.pixelSize: 14
                            font.bold: true
                            color: Material.primary
                        }

                        Item { Layout.fillWidth: true }

                        // Индикатор состояния смены
                        Rectangle {
                            width: 10
                            height: 10
                            radius: 5
                            color: {
                                switch(model.shiftState) {
                                    case "Открыта": return "green"
                                    case "Истекла": return "red"
                                    default: return "gray"
                                }
                            }
                        }
                    }

                    Text {
                        text: model.modelName || "Неизвестная модель"
                        font.pixelSize: 12
                        color: "gray"
                    }
                }
                highlighted: kktComboBox.highlightedIndex === index
            }

            // Отображение выбранного элемента
            contentItem: RowLayout {
                spacing: 5

                Text {
                    text: "🖥️"
                    font.pixelSize: 16
                }

                ColumnLayout {
                    spacing: 2

                    Text {
                        text: kktComboBox.currentText
                        font.pixelSize: 14
                        font.bold: true
                        elide: Text.ElideRight
                    }

                    Text {
                        text: kktListModel.get(kktComboBox.currentIndex)?.modelName || ""
                        font.pixelSize: 11
                        color: "gray"
                        visible: kktComboBox.currentIndex >= 0
                    }
                }
            }
        }

        // Детальная информация о выбранной кассе
        GroupBox {
            title: "Детальная информация"
            Layout.fillWidth: true
            Layout.preferredHeight: 250

            ScrollView {
                anchors.fill: parent
                clip: true

                ColumnLayout {
                    width: parent.width - 20
                    spacing: 8

                    // Используем Repeater для отображения информации
                    Repeater {
                        model: ListModel {
                            id: detailsModel
                        }

                        Rectangle {
                            Layout.fillWidth: true
                            Layout.preferredHeight: 30
                            color: index % 2 === 0 ? "#f8f8f8" : "white"
                            radius: 3

                            RowLayout {
                                anchors.fill: parent
                                anchors.margins: 5
                                spacing: 10

                                Text {
                                    text: model.label + ":"
                                    font.pixelSize: 13
                                    font.bold: true
                                    color: "#555"
                                    Layout.preferredWidth: 150
                                }

                                Text {
                                    text: model.value || "Н/Д"
                                    font.pixelSize: 13
                                    color: model.value ? "#333" : "#999"
                                    Layout.fillWidth: true
                                    wrapMode: Text.WordWrap
                                }

                                // Специальный индикатор для статуса смены
                                Rectangle {
                                    width: 8
                                    height: 8
                                    radius: 4
                                    visible: model.label === "Состояние смены"
                                    color: {
                                        if (model.value === "Открыта") return "green"
                                        if (model.value === "Истекла") return "red"
                                        return "gray"
                                    }
                                }
                            }
                        }
                    }
                }
            }
        }

        // Статус бар
        Rectangle {
            Layout.fillWidth: true
            Layout.preferredHeight: 32
            color: statusBarColor
            radius: 4

            RowLayout {
                anchors.fill: parent
                anchors.margins: 8
                spacing: 8

                Text {
                    text: statusIcon
                    font.pixelSize: 14
                }

                Text {
                    id: statusText
                    text: "Готов"
                    color: "white"
                    font.pixelSize: 12
                    elide: Text.ElideRight
                    Layout.fillWidth: true
                }

                Text {
                    text: new Date().toLocaleTimeString()
                    color: "white"
                    font.pixelSize: 11
                    opacity: 0.8
                }
            }
        }
    }

    // Свойства для статус бара
    property string statusIcon: "✓"
    property string statusBarColor: "#4CAF50"

    // Счетчики для статистики
    property int openedShiftsCount: 0
    property int expiredShiftsCount: 0

    // Функция обновления списка касс
    function updateKktList() {
        busyIndicator.running = true
        statusText.text = "Загрузка списка касс..."
        statusIcon = "⟳"
        statusBarColor = "#2196F3"

        // Очищаем текущий список
        kktListModel.clear()
        openedShiftsCount = 0
        expiredShiftsCount = 0

        try {
            // Получаем данные через контроллер
            var result = kktController.getKktList()
            console.log("Получен результат:", JSON.stringify(result))

            if (result && result.length > 0) {
                for (var i = 0; i < result.length; i++) {
                    var kkt = result[i]

                    // Считаем статистику
                    if (kkt.shiftState === "Открыта") openedShiftsCount++
                    if (kkt.shiftState === "Истекла") expiredShiftsCount++

                    kktListModel.append({
                        display: kkt.kktSerial,
                        kktSerial: kkt.kktSerial,
                        fnSerial: kkt.fnSerial,
                        kktInn: kkt.kktInn,
                        kktRnm: kkt.kktRnm,
                        modelName: kkt.modelName,
                        dkktVersion: kkt.dkktVersion,
                        developer: kkt.developer,
                        manufacturer: kkt.manufacturer,
                        shiftState: kkt.shiftState
                    })
                }

                kktComboBox.currentIndex = 0
                updateDetails()

                statusText.text = "Загружено касс: " + kktListModel.count
                statusIcon = "✓"
                statusBarColor = "#4CAF50"
            } else {
                statusText.text = "Кассы не найдены"
                statusIcon = "⚠"
                statusBarColor = "#FF9800"
            }
        } catch (error) {
            console.error("Ошибка при загрузке касс:", error)
            statusText.text = "Ошибка: " + error
            statusIcon = "✗"
            statusBarColor = "#F44336"
        } finally {
            busyIndicator.running = false
        }
    }

    // Функция обновления детальной информации
    function updateDetails() {
        detailsModel.clear()

        if (kktComboBox.currentIndex < 0) return

        var currentKkt = kktListModel.get(kktComboBox.currentIndex)
        if (!currentKkt) return

        var details = [
            {label: "Серийный номер", value: currentKkt.kktSerial},
            {label: "Зав. номер ФН", value: currentKkt.fnSerial},
            {label: "ИНН", value: currentKkt.kktInn},
            {label: "РНМ", value: currentKkt.kktRnm},
            {label: "Модель", value: currentKkt.modelName},
            {label: "Версия ДККТ", value: currentKkt.dkktVersion},
            {label: "Разработчик", value: currentKkt.developer},
            {label: "Производитель", value: currentKkt.manufacturer},
            {label: "Состояние смены", value: currentKkt.shiftState}
        ]

        for (var i = 0; i < details.length; i++) {
            detailsModel.append(details[i])
        }
    }

    // Обновление деталей при выборе кассы
    Connections {
        target: kktComboBox
        function onCurrentIndexChanged() {
            updateDetails()
        }
    }

    // Автоматическая загрузка при старте
    Component.onCompleted: {
        updateKktList()
    }
}