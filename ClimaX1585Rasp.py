# pyinstaller --onefile --windowed "/home/notebook/Área de trabalho/Programas/newenv/ClimaX1585Rasp.py"
## Credit to Guizz1585
### Contribua com testes e atualizações
#### reddit.com/user/GLeme1/
##### github.com/guizz1585/



import sys
import time
from PyQt5.QtWidgets import (
    QApplication, QLabel, QVBoxLayout, QWidget, QPushButton, QSlider, QMessageBox
)
from PyQt5.QtCore import QThread, pyqtSignal, QTime, Qt
import RPi.GPIO as GPIO

# Simulações para os sensores
class TemperatureSensor:
    def read_temperature(self):
        return 25  # Valor fictício

class HumiditySensor:
    def read_humidity(self):
        return 45  # Valor fictício

class LightSensor:
    def read_light_level(self):
        return 500  # Valor fictício

# Pinos GPIO dos dispositivos
RAIN_PIN = 17
HUMIDIFIER_PIN = 27
INTAKE_PIN = 22
EXHAUST_PIN = 23
LIGHT_PIN = 24

# Configuração dos GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(RAIN_PIN, GPIO.OUT)
GPIO.setup(HUMIDIFIER_PIN, GPIO.OUT)
GPIO.setup(INTAKE_PIN, GPIO.OUT)
GPIO.setup(EXHAUST_PIN, GPIO.OUT)
GPIO.setup(LIGHT_PIN, GPIO.OUT)

# Classe de Thread para controle de clima
class ClimateControlThread(QThread):
    update_data = pyqtSignal(str, str, str)  # Sinal para atualizar a interface
    alert_signal = pyqtSignal(str)  # Sinal para enviar alertas

    def __init__(self):
        super().__init__()
        self.temp_sensor = TemperatureSensor()
        self.humidity_sensor = HumiditySensor()
        self.light_sensor = LightSensor()
        self.running = True
        self.manual_light_intensity = 100  # Intensidade da luz manual (0-100)
        self.manual_humidity_level = 50  # Nível de umidade manual (0-100)

    def run(self):
        while self.running:
            temp = self.temp_sensor.read_temperature()
            humidity = self.humidity_sensor.read_humidity()
            light_level = self.light_sensor.read_light_level()

            # Controle de dispositivos
            self.control_devices(temp, humidity, light_level)

            # Emitir sinal para atualizar interface
            self.update_data.emit(f"Temperatura: {temp}°C", 
                                  f"Umidade: {humidity}%", 
                                  f"Luminosidade: {light_level} lux")
            
            # Checar por alertas
            self.check_alerts(temp, humidity)

            time.sleep(5)

    def control_devices(self, temp, humidity, light_level):
        # Controle de temperatura
        if temp > 28:
            GPIO.output(EXHAUST_PIN, GPIO.HIGH)
        elif temp < 20:
            GPIO.output(INTAKE_PIN, GPIO.HIGH)

        # Controle de umidade manual
        if humidity < self.manual_humidity_level:
            GPIO.output(HUMIDIFIER_PIN, GPIO.HIGH)

        # Controle de luz artificial com ciclo dia/noite ou ajuste manual
        current_time = QTime.currentTime()
        if 6 <= current_time.hour() < 18:  # Horário entre 6h e 18h
            if self.manual_light_intensity > 50:  # Ajuste manual com um valor limite
                GPIO.output(LIGHT_PIN, GPIO.HIGH)  # Liga luz artificial
            else:
                GPIO.output(LIGHT_PIN, GPIO.LOW)
        else:
            GPIO.output(LIGHT_PIN, GPIO.LOW)  # Desliga luz artificial fora do horário

        # Controle de chuva artificial
        if humidity < 30:
            GPIO.output(RAIN_PIN, GPIO.HIGH)

    def check_alerts(self, temp, humidity):
        # Definir os limites para temperatura e umidade
        if temp < 15 or temp > 35:
            self.alert_signal.emit(f"Alerta: Temperatura fora do intervalo ({temp}°C)!")
        if humidity < 30 or humidity > 70:
            self.alert_signal.emit(f"Alerta: Umidade fora do intervalo ({humidity}%)!")

    def set_manual_light_intensity(self, intensity):
        self.manual_light_intensity = intensity

    def set_manual_humidity_level(self, level):
        self.manual_humidity_level = level

# Interface gráfica com PyQt5
class ClimateControlApp(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Controle de Clima para Cultivo")
        self.setGeometry(100, 100, 400, 400)

        # Layout da interface
        layout = QVBoxLayout()

        # Rótulos para exibir dados
        self.temp_label = QLabel("Temperatura: --°C")
        self.humidity_label = QLabel("Umidade: --%")
        self.light_label = QLabel("Luminosidade: -- lux")

        # Sliders para ajuste manual
        self.light_slider = QSlider(Qt.Horizontal)
        self.light_slider.setRange(0, 100)
        self.light_slider.setValue(100)
        self.light_slider.setTickPosition(QSlider.TicksBelow)
        self.light_slider.setTickInterval(10)
        self.light_slider.valueChanged.connect(self.adjust_light)

        self.humidity_slider = QSlider(Qt.Horizontal)
        self.humidity_slider.setRange(0, 100)
        self.humidity_slider.setValue(50)
        self.humidity_slider.setTickPosition(QSlider.TicksBelow)
        self.humidity_slider.setTickInterval(10)
        self.humidity_slider.valueChanged.connect(self.adjust_humidity)

        # Botão para parar o controle
        self.stop_button = QPushButton("Parar Controle")
        self.stop_button.clicked.connect(self.stop_control)

        # Adicionar widgets ao layout
        layout.addWidget(self.temp_label)
        layout.addWidget(self.humidity_label)
        layout.addWidget(self.light_label)
        layout.addWidget(QLabel("Ajuste de Intensidade da Luz:"))
        layout.addWidget(self.light_slider)
        layout.addWidget(QLabel("Ajuste de Umidade:"))
        layout.addWidget(self.humidity_slider)
        layout.addWidget(self.stop_button)

        self.setLayout(layout)

        # Iniciar o controle de clima em uma thread separada
        self.climate_thread = ClimateControlThread()
        self.climate_thread.update_data.connect(self.update_labels)
        self.climate_thread.alert_signal.connect(self.show_alert)
        self.climate_thread.start()

    # Atualizar rótulos com dados dos sensores
    def update_labels(self, temp, humidity, light):
        self.temp_label.setText(temp)
        self.humidity_label.setText(humidity)
        self.light_label.setText(light)

    # Parar o controle de clima
    def stop_control(self):
        self.climate_thread.running = False
        GPIO.cleanup()  # Limpar pinos GPIO
        self.climate_thread.quit()

    # Ajustar a intensidade da luz manualmente
    def adjust_light(self, value):
        self.climate_thread.set_manual_light_intensity(value)

    # Ajustar o nível de umidade manualmente
    def adjust_humidity(self, value):
        self.climate_thread.set_manual_humidity_level(value)

    # Exibir alertas de temperatura ou umidade
    def show_alert(self, message):
        QMessageBox.warning(self, "Alerta de Clima", message)

# Inicialização da aplicação
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ClimateControlApp()
    window.show()
    sys.exit(app.exec_())





                                                                                # Jesus #