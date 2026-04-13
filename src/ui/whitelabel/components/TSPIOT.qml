import QtQuick

Item {
    id: root
    width: 829
    height: 646

    property var instanceInfo: null

    // ID
    Text {
        id: iD_label
        x: 92
        y: 139
        color: "#000000"
        font.family: "Inter"
        font.pixelSize: 16
        text: "ID:"
    }

    Text {
        id: element
        x: 92
        y: 158
        height: 19
        width: 200
        color: instanceInfo && instanceInfo.regData && instanceInfo.regData.tspiotId
               ? "#000000" : "#a39b9b"
        font.family: "Inter"
        font.pixelSize: 16
        text: instanceInfo && instanceInfo.regData && instanceInfo.regData.tspiotId
              ? instanceInfo.regData.tspiotId : "Нет информации"
        wrapMode: Text.WordWrap
    }

    // Лицензия — заголовок
    Text {
        id: element_2
        x: 94
        y: 111
        color: "#000000"
        font.family: "Inter"
        font.pixelSize: 16
        font.weight: Font.Bold
        text: "Лицензия"
    }

    // Лицензия — статус
    Text {
        id: element_3
        x: 189
        y: 111
        font.family: "Inter"
        font.pixelSize: 14
        font.weight: Font.Bold
        color: {
            if (!instanceInfo || !instanceInfo.licenses || instanceInfo.licenses.length === 0)
                return "#a39b9b"
            return instanceInfo.licenses[0].isActive ? "#2a9d2a" : "#de2626"
        }
        text: {
            if (!instanceInfo || !instanceInfo.licenses || instanceInfo.licenses.length === 0)
                return "Нет информации"
            var lic = instanceInfo.licenses[0]
            var datePart = lic.activeTill.split(" ")[0]
            var parts = datePart.split("-")
            var formatted = parts[2] + "." + parts[1] + "." + parts[0]
            return lic.isActive ? "Активна до " + formatted : "Неактивна"
        }
    }

    // Версия — заголовок
    Text {
        id: element_4
        x: 443
        y: 111
        height: 18
        color: "#000000"
        font.family: "Inter"
        font.pixelSize: 15
        font.weight: Font.Bold
        text: "Версия"
    }

    // Версия — значение
    Text {
        id: v1_2_3_
        x: 443
        y: 150
        color: "#000000"
        font.family: "Inter"
        font.pixelSize: 12
        text: instanceInfo ? instanceInfo.version : "—"
    }

    // Состояние (state)
    Text {
        id: element_8
        x: 311
        y: 258
        color: "#000000"
        font.family: "Inter"
        font.pixelSize: 14
        text: instanceInfo ? instanceInfo.state : "Нет информации"
    }

    // ИНН
    Text {
        id: element_18
        x: 259
        y: 319
        color: instanceInfo && instanceInfo.regData ? "#000000" : "#a39b9b"
        font.family: "Inter"
        font.pixelSize: 16
        text: instanceInfo && instanceInfo.regData
              ? instanceInfo.regData.kktInn : "Нет информации"
    }

    // Port
    Text {
        id: portText
        x: 445
        y: 319
        color: instanceInfo ? "#000000" : "#a39b9b"
        font.family: "Inter"
        font.pixelSize: 16
        text: instanceInfo ? String(instanceInfo.clientPort) : "Нет информации"
    }

    // Последняя синхронизация
    Text {
        id: element_27
        x: 443
        y: 535
        color: instanceInfo && instanceInfo.licenses && instanceInfo.licenses.length > 0
               ? "#000000" : "#a39b9b"
        font.family: "Inter"
        font.pixelSize: 16
        text: {
            if (!instanceInfo || !instanceInfo.licenses || instanceInfo.licenses.length === 0)
                return "Нет информации"
            return instanceInfo.licenses[0].lastSync
        }
    }
}