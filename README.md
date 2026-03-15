resources.qrc (XML файл со списком ресурсов)
       ↓
pyside6-rcc resources.qrc -o resources_rc.py (команда)
       ↓
resources_rc.py (сгенерированный Python файл с бинарными данными)
       ↓
import resources_rc (в вашем коде)

для подключения новых qml нужно использовать его

а также перекомпилировать при изменениях qml.

компиляция
pyside6-rcc resources.qrc -o resources_rc.py


2. Работа с ресурсами
A. Создаем resources.qrc:
```qrc
<RCC>
    <qresource prefix="/">
        <!-- Все картинки -->
        <file>ui/assets/unit.png</file>
        <file>ui/assets/unit_1.png</file>
        <file>ui/assets/unit_2.png</file>
        
        <!-- Шрифты -->
        <file>ui/fonts/inter-regular.ttf</file>
        <file>ui/fonts/playfairdisplay-semibold.ttf</file>
    </qresource>
</RCC>
```

два режима запуска:

разработка (без компиляции исходяников)
python -m src.main --dev

с компиляцией ui
python -m src.main --compiled