import os

from PySide6.QtGui import QFontDatabase, QIcon
from PySide6.QtWidgets import QMainWindow


class TSPIoTQmlLoader(QMainWindow):
    def __init__(self,
                 window_size: tuple,
                 app_icon_path: str,
                 header_name: str,
                 fonts_path: str
                 ):
        """
        Args:
            fonts_path: Путь к папке со шрифтами.
                       Если None - шрифты не загружаются
        """
        super().__init__()
        self.app_icon_path = app_icon_path
        self.header_name = header_name
        self.window_size = window_size

        #подгружаем стили
        if fonts_path:
            self.__load_fonts(fonts_path)

        #запрещаем растягивание окна
        self.setFixedSize(window_size[0], window_size[1])
        self.__load_fonts(fonts_path)
        self.__set_header()
        self.__set_app_icon()



    def __set_app_icon(self):
        icon_path = os.path.abspath(self.app_icon_path)
        if os.path.exists(icon_path):
            self.setWindowIcon(QIcon(icon_path))
            print(f"Иконка загружена: {icon_path}")
        else:
            print(f"Иконка не найдена: {icon_path}")

    def __set_header(self):
        self.setWindowTitle(self.header_name)


    def __load_fonts(self, fonts_dir):
        """Загружает шрифты из указанной директории"""
        if not os.path.exists(fonts_dir):
            print(f"Папка со шрифтами не найдена: {fonts_dir}")
            return

        print(f"Загружаем шрифты из: {fonts_dir}")
        for font_file in os.listdir(fonts_dir):
            if font_file.endswith(('.ttf', '.otf', '.ttc')):
                font_path = os.path.join(fonts_dir, font_file)
                font_id = QFontDatabase.addApplicationFont(font_path)
                if font_id != -1:
                    font_families = QFontDatabase.applicationFontFamilies(font_id)
                    print(f"  Загружен: {font_file} -> {font_families}")
                else:
                    print(f"  Ошибка загрузки: {font_file}")

    def __load_qml_file(self, qml_file_path):
        ...