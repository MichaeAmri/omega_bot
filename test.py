# подключаем необходимые библиотеки
from picamera import PiCamera
from time import sleep
# создаём объект для работы с камерой
camera = PiCamera()
# запускаем просмотр сигнала с камеры на экране поверх всех окон
camera.start_preview()
# 10 секунд смотрим на экран
sleep(10)
# выключаем просмотр
camera.stop_preview()