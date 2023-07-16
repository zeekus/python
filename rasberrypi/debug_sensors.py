from gpiozero import Button

sound_sensor_pin = 4
vibration_sensor_pin = 26

sound_sensor = Button(sound_sensor_pin)
vibration_sensor = Button(vibration_sensor_pin)

while True:
    if sound_sensor.is_pressed:
        print("Sound sensor activated")

    if vibration_sensor.is_pressed:
        print("Vibration sensor activated")
