import QtQuick
import QtQuick.Shapes
import "components"



Window {
    width: 829
    height: 646
    visible: true
    title: "EspNewGuiInterface"


Image {
    id: image_97
    x: 19
    y: 101
    z: 0
    source: Qt.resolvedUrl("assets/image_97.png")
}
Image {
    id: image_99
    x: 24
    y: 244
    z: 0
    source: Qt.resolvedUrl("assets/image_99.png")
}
Image {
    id: image_98
    x: 7
    y: 400
    z: 0
    source: Qt.resolvedUrl("assets/image_98.png")
}

ToolBar {
    x: 0
    y: 0
    width: parent.width
    height: 70
    z: 1
}

TspIot {
    x: 70              // ← сдвиг вправо, чтобы не перекрывалось картинкой "ТС ПИоТ"
    y: 70
    width: parent.width - 70
    height: 170
    instanceInfo: null
    z: 1
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