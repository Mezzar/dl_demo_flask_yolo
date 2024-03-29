# Демо-проект Flask + YOLO5 detection

Для курса Deep Learning School от МФТИ, часть 1 (провинутый поток)

## 1 Выбор фреймворка и модели для детектора

Проект выполняется на PyTorch и модели YOLO5s [https://github.com/ultralytics/yolov5]

Используется младшая (s=small) модель, поскольку планируется размещение проекта на vds хостинге без GPU и с ограниченным объемом памяти.

В папке проекта создадим виртуальное окружение

```
python -m venv env
env\Scripts\activate
```

Установим YOLO5 с Github

```
git clone https://github.com/ultralytics/yolov5
cd yolov5
pip install -qr requirements.txt
```

Проверка функциональности модели

```python
import torch
from yolov5 import utils
display = utils.notebook_init()
```

## 2 Запуск детектора на случайных изображениях

Обработать набор изображений удобнее в пакетном режиме:
- поместить изображения в папку yolov5\data\images\
- выполнить команду `python detect.py --weights yolov5s.pt --img 640 --conf 0.25 --source data/images`
- обработанные изображения будет помещены в папку runs\detect\

Примеры работы детектора:

<img src="https://raw.githubusercontent.com/Mezzar/dl_demo_flask_yolo/master/static/demo1.jpg" width="700">

<img src="https://raw.githubusercontent.com/Mezzar/dl_demo_flask_yolo/master/static/demo2.jpg" width="700">

<img src="https://raw.githubusercontent.com/Mezzar/dl_demo_flask_yolo/master/static/demo3.jpg" width="700">

<img src="https://raw.githubusercontent.com/Mezzar/dl_demo_flask_yolo/master/static/demo4.jpg" width="700">

YOLO5 предобучена на датасете COCO. Скачаем валидационный сет картинок COCO-2017 и посмотрим как хорошо модель его предсказывает.

```
import torch
torch.hub.download_url_to_file('https://ultralytics.com/assets/coco2017val.zip', 'tmp.zip')
!unzip -q tmp.zip -d /datasets && rm tmp.zip
!python val.py --weights yolov5s.pt --workers 1 --data coco.yaml --img 640 --iou 0.65 --half --verbose
```

Получим для классов такую confusion matrix:

<img src="https://raw.githubusercontent.com/Mezzar/dl_demo_flask_yolo/master/static/confusion_matrix.png">

Очень даже неплохо, учитывая, что используем довольно слабую модель из семейства YOLO. Классы модель не путает, распознает достаточно устойчиво. Основные ошибки - когда не опознает объект и обозначает его пиксели как бэкграунд.

## 3 Выбор фреймворка для разработки веб-демо (Сценарий 1)

Демо выполняется на микрофреймворке Flask.

## 4-5 Разработка демо и встраивание модели-детектора в демо

Схема работы проекта достаточно простая. Имеется одна страница с формой для загрузки изображения. После загрузки файл обрабатывается и передается в модель. Модель генерирует изображение с граничными рамками и классами. Сохраняем изображение в файл и имя этого файла передаем в шаблон для отображения результата.

Требуемые для работы проекта пакеты python устанавливаются в виртуальное окружение. Их список содержится в файле `requrements.txt` и устанавливается командой `pip install -r requirements.txt`.

Структура файлов:

- data/
	- img_in/ - временная папка для загружаемых файлов
	- img_out/ - сюда сохраняются обработанные изображения с результатом детекции
- static/ - статичный файлы (доступны браузеру)	
- templates/ - папка шаблонов
	- base.html - базовый шаблон
	- index.html - шаблон страницы с формой, расширяет базовый
- app.py - основной файл проекта со скриптами обработки формы и отображения страницы
- config.py - файл-конфигурации Flask и параметры для скриптов
- ml.py - обработка изображения, создание модели и передача ей картинки, сохранение результата
- README.md - этот документ
- requrements.txt - список необходимых для работы пакетов

## 6 Тестирование демо

Веб-демо проекта протестирована локально и на VDS сервере. Функционирует корректно. 

<img src="https://raw.githubusercontent.com/Mezzar/dl_demo_flask_yolo/master/static/screenshot_1.jpg">

<img src="https://raw.githubusercontent.com/Mezzar/dl_demo_flask_yolo/master/static/screenshot_5.jpg">

<img src="https://raw.githubusercontent.com/Mezzar/dl_demo_flask_yolo/master/static/screenshot_2.jpg">


## 7 Оформление демо для показа другим людям

Для улучшения визуального оформления элементов формы и реализации курусели изображений использован css-фреймворк Bootstrap.

Дополнителньый функционал: для наглядности и удобства использования добавил сохранение в cookie ссылок на 7 (число меняется в конфиге) последних обработанных изображения и компонент Bootstrap carousel для их просмотра. Чтобы пользователь мог видеть не только последнее обработанное изображение но и предыдущие.

Демо-проект был развернут на VDS-сервере.
