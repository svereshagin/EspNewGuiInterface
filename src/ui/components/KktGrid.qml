import QtQuick
import QtQuick.Controls
import QtQuick.Layouts

Item {
    ScrollView {
        anchors.fill: parent
        clip: true
        ScrollBar.horizontal.policy: ScrollBar.AlwaysOff

        Flow {
            width: parent.width
            spacing: 12

            Repeater {
                model: AppStorage.kktList

                Cash {
                    width: 280
                    height: 190
                    kktData: modelData
                    isSelected: AppStorage.currentSerial === modelData.kktSerial
                    onCardClicked: AppStorage.set_current_cash(modelData.kktSerial)
                }
            }
        }
    }
}