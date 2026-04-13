Отличный прогресс! Вот что нужно дописать в README.md:

## 📝 Обновленный README.md

```markdown
# ТС ПИоТ - GUI приложение

PySide6 приложение с QML интерфейсом для работы с ТС ПИоТ.

## 📋 Требования

- Python 3.12+
- Poetry или uv (рекомендуется)
- PySide6

## 🚀 Быстрый старт

### 1. Установка зависимостей

```bash
# Используя uv (рекомендуется)
uv sync

# Или используя pip
pip install -r requirements.txt
```

### 2. Запуск приложения

#### Режим разработки (QML из файлов)
```bash
python -m old_src.main --dev
```

#### Режим продакшена (скомпилированные ресурсы)
```bash
# Сначала скомпилировать ресурсы из корня репозитория 
uv run pyside6-rcc old_src/resources.qrc -o old_src/resources_rc.py

# Затем запустить
python -m old_src.main --compiled
```

## 📦 Ресурсы и компиляция

### Структура ресурсов
```
ui/
├── assets/          # Изображения
├── fonts/           # Шрифты
└── Gadget.ui.qml    # Главный QML файл
```

### Компиляция ресурсов
```bash
# Ручная компиляция
pyside6-rcc resources.qrc -o resources_rc.py

# Автоматизация (Makefile)
make resources    # скомпилировать ресурсы
make run-dev      # запуск в dev режиме
make run-prod     # запуск в prod режиме
```

### Добавление новых ресурсов

1. Добавьте файл в соответствующую папку (`ui/assets/` или `ui/fonts/`)
2. Пропишите путь в `resources.qrc`:
```xml
<RCC>
    <qresource prefix="/">
        <file>ui/assets/новый_файл.png</file>
        <file>ui/fonts/новый_шрифт.ttf</file>
    </qresource>
</RCC>
```
3. Перекомпилируйте ресурсы

## 🔧 Сборка исполняемых файлов

### Для Windows (.exe)

```bash
# Установка PyInstaller
pip install pyinstaller

# Компиляция ресурсов
pyside6-rcc resources.qrc -o resources_rc.py

# Сборка в один файл (WINDOWS)
pyinstaller --onefile --windowed `
    --name "ТС-ПИоТ" `
    --add-data "src;src" `
    --hidden-import PySide6.QtQml `
    --hidden-import PySide6.QtCore `
    --hidden-import PySide6.QtGui `
    --hidden-import PySide6.QtQuick `
    --hidden-import PySide6.QtQuickWidgets `
    --collect-data PySide6 `
    --paths . `
    old_src/main.py

# Готовый .exe будет в папке dist/
```

### Для Linux (AppImage)

#### На Ubuntu/Debian:
```bash
# 1. Компиляция ресурсов
pyside6-rcc resources.qrc -o resources_rc.py

# 2. Сборка с PyInstaller
pyinstaller --onefile --windowed \
    --name "ТС-ПИоТ" \
    --add-data "src:src" \
    --hidden-import PySide6.QtQml \
    --hidden-import PySide6.QtCore \
    --hidden-import PySide6.QtGui \
    --hidden-import PySide6.QtQuick \
    --hidden-import PySide6.QtQuickWidgets \
    --collect-data PySide6 \
    --paths . \
    old_src/main.py

# 3. Упаковка в AppImage (опционально)
# Скачать linuxdeployqt и создать AppImage
wget https://github.com/probonopd/linuxdeployqt/releases/download/continuous/linuxdeployqt-continuous-x86_64.AppImage
chmod +x linuxdeployqt*.AppImage

# Создать .desktop файл и иконку, затем:
./linuxdeployqt*.AppImage dist/ТС-ПИоТ -appimage
```

#### Кроссплатформенная сборка (из Windows в Linux)
```bash
# Использование Docker
docker run --rm -v ${PWD}:/app -w /app \
    python:3.12-slim bash -c "
    pip install pyinstaller pyside6 &&
    pyside6-rcc resources.qrc -o resources_rc.py &&
    pyinstaller --onefile --windowed \
                --name 'ТС-ПИоТ' \
                --add-data 'ui:ui' \
                src/main.py
    "
```

### Для macOS (.app)

```bash
# На macOS
pyinstaller --onefile --windowed \
            --name "ТС ПИоТ" \
            --add-data "ui:ui" \
            --icon path/to/icon.icns \
            --hidden-import PySide6.QtQml \
            old_src/main.py
```

## 🐳 Docker сборка

### Dockerfile для Linux сборки
```dockerfile
FROM python:3.12-slim

WORKDIR /app

RUN pip install pyinstaller pyside6

COPY . .

RUN pyside6-rcc resources.qrc -o resources_rc.py && \
    pyinstaller --onefile --windowed \
                --name "tspiot-gui" \
                --add-data "ui:ui" \
                src/main.py

CMD ["/app/dist/tspiot-gui"]
```

Сборка:
```bash
docker build -t TSPIOT.qml-builder .
docker run --rm -v ${PWD}/dist:/app/dist TSPIOT.qml-builder
```

## 📁 Структура проекта

```
├── src/
│   ├── main.py                 # Точка входа
│   ├── application/            # Контроллеры приложения
│   ├── core/                   # Ядро (настройки, логирование)
│   └── infrastructure/         # Инфраструктура (QML загрузчик)
├── ui/
│   ├── assets/                 # Изображения
│   ├── fonts/                  # Шрифты
│   └── Gadget.ui.qml          # Главный QML файл
├── resources.qrc               # Список ресурсов
├── resources_rc.py             # Скомпилированные ресурсы
├── pyproject.toml              # Зависимости
├── Makefile                    # Автоматизация
└── README.md                   # Документация
```

## 🔧 Makefile команды

```makefile
.PHONY: help resources run-dev run-prod clean dist-windows dist-linux

help:          # Показать справку
resources:     # Скомпилировать ресурсы
run-dev:       # Запустить в режиме разработки
run-prod:      # Запустить в продакшн режиме
clean:         # Очистить временные файлы
dist-windows:  # Собрать .exe для Windows
dist-linux:    # Собрать исполняемый файл для Linux
```

Использование:
```bash
make resources      # компиляция ресурсов
make run-dev        # запуск разработки
make dist-linux     # сборка для Linux
```

## ⚙️ Конфигурация

Настройки приложения сохраняются в:
- **Linux**: `~/.esp/esm/esm-gui/gui_settings.json`
- **Windows**: `C:\ProgramData\esp\esm\esm-gui\gui_settings.json`

Основные параметры:
- `port` - порт оркестратора (по умолчанию: 51077)

## 🐛 Отладка

### Проверка загрузки ресурсов
```bash
# Проверить, что QML грузится из файлов
python -m old_src.main --dev

# Проверить скомпилированные ресурсы
python -m old_src.main --compiled
```

### Логи
Логи приложения сохраняются в директории конфигурации:
- **Linux**: `~/.esp/esm/esm-gui/log/gui.log`
- **Windows**: `C:\ProgramData\esp\esm\esm-gui\log\gui.log`

## 📦 Релизы

Готовые собранные версии доступны в [Releases](https://github.com/svereshagin/EspNewGuiInterface/releases)

Для создания нового релиза:
1. Обновите версию в `pyproject.toml`
2. Соберите исполняемые файлы для всех платформ
3. Создайте релиз на GitHub и прикрепите файлы

## 🤝 Участие в разработке

1. Форкните репозиторий
2. Создайте ветку для фичи
3. Внесите изменения
4. Запустите тесты
5. Создайте Pull Request

## 📄 Лицензия

MIT
```

## 🔧 Makefile для автоматизации

Создайте `Makefile` в корне проекта:

```makefile
.PHONY: help resources run-dev run-prod clean dist-windows dist-linux

NAME = "ТС ПИоТ"

help:
	@echo "Доступные команды:"
	@echo "  make resources     - скомпилировать ресурсы"
	@echo "  make run-dev       - запуск в режиме разработки"
	@echo "  make run-prod      - запуск в продакшн режиме"
	@echo "  make clean         - очистить временные файлы"
	@echo "  make dist-windows  - собрать .exe для Windows"
	@echo "  make dist-linux    - собрать для Linux"

resources:
	pyside6-rcc resources.qrc -o resources_rc.py
	@echo "✅ Ресурсы скомпилированы"

run-dev:
	python -m src.main --dev

run-prod: resources
	python -m src.main --compiled

clean:
	rm -rf build/ dist/ __pycache__/ src/__pycache__/
	rm -f *.spec resources_rc.py
	@echo "✅ Временные файлы удалены"

dist-windows: resources
	pyinstaller --onefile --windowed \
		--name $(NAME) \
		--add-data "ui;ui" \
		--hidden-import PySide6.QtQml \
		--hidden-import PySide6.QtCore \
		--hidden-import PySide6.QtGui \
		src/main.py
	@echo "✅ Windows сборка готова: dist/$(NAME).exe"

dist-linux: resources
	pyinstaller --onefile --windowed \
		--name $(NAME) \
		--add-data "ui:ui" \
		--hidden-import PySide6.QtQml \
		--hidden-import PySide6.QtCore \
		--hidden-import PySide6.QtGui \
		src/main.pymake 
	@echo "✅ Linux сборка готова: dist/$(NAME)"
```

Теперь у вас полная документация по сборке под разные платформы!