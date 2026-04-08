import QtQuick 2.15
import QtQuick.Controls 2.15
import QtQuick.Layouts 1.15

Rectangle {
    property string status: "";
    property string gismt_error: ""; //возможность убрать, оставив только статус
    property string licence_id: "";
    property bool gismt_licence_is_active: False; //возможно убрать, нужно понять что по просроку может возвращаться

    //Минорные данные с запроса
    property string last_sync: "";

    //Отдельное окно Настроек GISMT
    property string gismtAddress: "";
    property bool compatibilityMode: False;
    property bool allowRemoteConnection: False;


}
