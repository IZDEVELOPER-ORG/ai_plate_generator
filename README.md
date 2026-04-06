# AI Plate Generator
<img width="480" height="640" alt="image" src="https://github.com/user-attachments/assets/a49f5fdd-dc75-4657-a312-ef4d7b2a5824" />
<img width="480" height="640" alt="image" src="https://github.com/user-attachments/assets/6505a14b-a449-4fe1-a16e-0ff8bd8e969c" />
(изображения сгенерированных номеров)

AI Plate Generator — Генератор вариаций автомобильных номеров с использованием Google Gemini (image-to-image). Генерируется случайное 5-ти значное число.
Проект берет исходные изображения номеров и изменяет цифры, символы, сохраняя стиль и фон. 

## ⚙️ Установка
### 1. Python

+ Рекомендуется Python 3.10+

### 2. Установка зависимостей
```bash
pip install google-generativeai google-genai PyYAML tqdm fire
```
### 3. Структура проекта
```bash
ai_plate_generator/
│
├── configs/
│   └── config.yaml
│
├── images/
│
├── output/
│
├── API_key.txt
│
├── api_usage.log
│
└── main.py
```
## 🧩 Функционал
### Общие возможности
+ Обработка изображений из папки
+ Генерация вариаций через AI (Gemini)
+ Изменение только нужной части изображения (цифры)
+ Сохранение изображения + текстового label
+ Логирование использования API (токены)
+ Гибкая настройка через .yaml

## Параметры (configs/config.yaml):
```bash
images_folder: images/
save_folder: output/
API_key: API_key.txt
model: gemini-3.1-flash-image-preview
limit: 1
stacked_text: "P/F"
prompt: "Do not change the first two characters P and F, do not change background image. Only update the 5 digits that follow. The final number in the image MUST be exactly: "
```
### ⚠️ Важно:
+ images_folder — папка с входными изображениями
+ save_folder — папка для результатов 
+ API_key — путь к API ключу
+ limit — колличество копий для одного изображения, которые вы хотите сгенерировать
+ stacked_text — префикс для .txt файла c разметкой
+ prompt — основной prompt (к нему добавляются цифры)

### 🔑 API ключ:
Создай файл:
```bash
API_key.txt
```

И вставь туда:
```bash
YOUR_API_KEY_HERE
```

# ✨Как это работает:
```bash
python main.py config.yaml
или
python main.py --cfg=config.yaml
```
### Pipeline:
+ Загружаются изображения из images/
+ Для каждого изображения:
  - генерируется случайное число указанное в prompt
+ Отправка запроса в Gemini
+ Получение нового изображения
+ Сохранение результата

### 🧪 Генерация

Для каждого изображения:

+ создаётся новая вариация изображения:
  ```bash
  image_var0_<uuid>.jpg
  ```
+ создаётся .txt файл:
  ```bash
  image_var0_<uuid>.txt
  
  Внутри номер:
  P/F12345
  ```

### 📊 Логирование
Все запросы логируются в:
```bash
api_usage.log
```
Пример:
```bash
FILE: plate_1.png | Prompt Tokens: 120 | Candidates Tokens: 300 | Total Tokens: 420
```
### 📦 Поддерживаемые форматы
```bash
.png .jpg .jpeg .bmp .webp
```
