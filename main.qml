import QtQuick 2.15
import QtQuick.Window 2.15
import QtQuick.Controls 2.15

Window {
    width: 1000
    height: 800
    visible: true
    color: "#f6f7f7"
    title: qsTr("Hello World")

    Text {
        id: text1
        x: 283
        y: 33
        width: 434
        height: 66
        color: "#090808"
        text: qsTr("Brain Tumor Clasification")
        font.pixelSize: 30
        horizontalAlignment: Text.AlignHCenter
        verticalAlignment: Text.AlignVCenter
        fontSizeMode: Text.HorizontalFit
        minimumPixelSize: 25
    }
}
