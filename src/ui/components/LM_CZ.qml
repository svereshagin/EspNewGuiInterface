import QtQuick 2.15
import QtQuick.Controls 2.15
import QtQuick.Layouts 1.15

Rectangle {

    property string address: "127.0.0.1";
    property int local_module_controller_port: 50063;
    property string regime_login: "admin";
    property string regime_password: "admin";
    property string controllerVersion: 0;
    property int code: 1; //not configured
    property string osInfo: ""; //операционная система, где стоит лм контроллер(там же и regime)
    property string lmStatus: "";
    property string lastSync: "";
    property string lm_cz_error: "";


}
