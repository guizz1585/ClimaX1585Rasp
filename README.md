ta de sacanagem github por isso so nerd usa esse krl 


If you have any questions, call me, always willing to learn and teach



não consegui fazer o upload dos outros arquivos, exece o limite de 25MB, tem o codigo abaixo com o PyInstaller comentado na primeira linha
I couldn't upload the other files, it exceeds the 25MB limit, there is the code below with PyInstaller commented on the first line





Documentation for Climate Control System Code
Overview

This Python code is designed to control a climate environment for plant cultivation. The system monitors temperature, humidity, and light levels, and it controls several devices such as fans, humidifiers, lights, and artificial rain through GPIO pins on a Raspberry Pi. The user can adjust light intensity and humidity levels manually via a graphical user interface (GUI) built using PyQt5, and the system will provide real-time data updates and alerts if values go out of acceptable ranges.
Requirements

To ensure that everything functions correctly, you will need the following hardware and software components:

    Raspberry Pi with GPIO access for controlling external devices.
    External devices (e.g., fans, humidifiers, lights, artificial rain systems) connected to the Raspberry Pi GPIO pins.
    Sensors:
        Temperature sensor (simulated in the code).
        Humidity sensor (simulated in the code).
        Light sensor (simulated in the code).
    Libraries:
        PyQt5: For creating the graphical interface.
            Install using pip install pyqt5.
        RPi.GPIO: For controlling the Raspberry Pi GPIO pins.
            Install using pip install RPi.GPIO.
    Operating System: Raspberry Pi OS or any Linux-based system that supports GPIO.

Code Explanation

    Imports:
        sys, time: For system functions and time delays.
        PyQt5.QtWidgets, PyQt5.QtCore: For creating and handling the GUI.
        RPi.GPIO: To control the GPIO pins of the Raspberry Pi.

    Sensor Classes:
        Simulated classes for temperature, humidity, and light sensors:
            TemperatureSensor: Returns a fixed temperature of 25°C.
            HumiditySensor: Returns a fixed humidity level of 45%.
            LightSensor: Returns a fixed light intensity of 500 lux.

    GPIO Configuration:
        The GPIO pins are assigned to control devices:
            RAIN_PIN for rain simulation.
            HUMIDIFIER_PIN for controlling the humidifier.
            INTAKE_PIN and EXHAUST_PIN for controlling air intake and exhaust fans.
            LIGHT_PIN for controlling the artificial lighting.
        GPIO pins are set to output mode using GPIO.setup.

    ClimateControlThread Class:
        This is a separate thread that handles the climate control logic.
        The thread reads sensor values, controls devices based on sensor data, and updates the GUI every 5 seconds.
        Controls are:
            Temperature: If too high, the exhaust fan is activated; if too low, the intake fan is activated.
            Humidity: If below the manual setting, the humidifier is activated.
            Light: Controlled based on a simulated day/night cycle (6 AM to 6 PM) or manually using the slider.
            Rain: Activated if humidity drops below 30%.
        The thread also sends alerts when temperature or humidity go outside predefined safe ranges.

    ClimateControlApp Class:
        The main GUI window, built using PyQt5.
        Displays real-time data for temperature, humidity, and light.
        Includes sliders to manually adjust the light intensity and humidity levels.
        The GUI provides a "Stop Control" button that halts the climate control thread and cleans up the GPIO pins.

    Alert System:
        If temperature or humidity go outside safe ranges (15°C < temperature < 35°C and 30% < humidity < 70%), a warning message box is displayed.

    Manual Adjustments:
        Users can manually adjust light intensity (0–100%) and humidity level (0–100%) through sliders in the GUI.

    GPIO Cleanup:
        When the application is stopped, GPIO.cleanup() is called to reset the GPIO pins to a safe state.

How to Make It Work

    Hardware Setup:
        Ensure all necessary sensors and devices (fans, lights, etc.) are connected to the correct GPIO pins on the Raspberry Pi.

    Software Setup:
        Install the necessary Python packages using the following commands:

        bash

    pip install pyqt5
    pip install RPi.GPIO

Running the Application:

    Execute the Python script on your Raspberry Pi with sudo since GPIO requires root access:

    bash

    sudo python3 climate_control.py

Manual Adjustments:

    The light intensity and humidity levels can be adjusted manually using the sliders in the GUI. The system will control devices based on these settings and the sensor readings.

Stopping the Application:

    Click the "Stop Control" button in the GUI to safely terminate the climate control and release the GPIO pins.
