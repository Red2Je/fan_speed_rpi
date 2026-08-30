import yaml
import psutil
import RPi.GPIO as GPIO
import time
import logging
from logging.handlers import TimedRotatingFileHandler


logger = logging.getLogger(__name__)

FAN_PIN = 14


def retrieve_config(): 
    with open("config.yml", 'r') as f: 
        data = yaml.load(f, Loader=yaml.SafeLoader)
    return data

def refresh_variables() : 
    configuration = retrieve_config()
    min_temp = configuration["temperature"]["min_temp"]
    max_temp = configuration["temperature"]["max_temp"]
    min_speed = configuration["temperature"]["min_speed"]
    max_speed = configuration["temperature"]["max_speed"]
    refresh_time = configuration["temperature"]["refresh_time"]
    log_retention = configuration["logging"]["log_retention_days"]
    
    

    return min_temp, max_temp, min_speed, max_speed, refresh_time, log_retention

def __main__() :
    
    #Setup the GPIO module to communicate with the pin number 14 on the raspberry
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(FAN_PIN, GPIO.OUT)
    pwm = GPIO.PWM(FAN_PIN, 100)

    configuration = retrieve_config()
    speed = configuration["temperature"]["min_speed"]
    #Setup logging
    log_retention = configuration["logging"]["log_retention_days"]
    handler = TimedRotatingFileHandler(filename="fan_speed.log", when = "D", interval = 1, backupCount=log_retention, delay=False)
    logger.addHandler(handler)
    logger.setLevel(logging.INFO)

    while 1 :
        actual_temperature = psutil.sensors_temperatures()["cpu_thermal"][0].current
        min_temp, max_temp, min_speed, max_speed, refresh_time, log_retention = refresh_variables()
        handler.backupCount = log_retention

        if actual_temperature < min_temp : 
            speed = min_speed
        elif actual_temperature > max_temp :
            speed = max_speed 
        else : 
            speed = round(min_speed + (max_speed - min_speed)*((actual_temperature-min_temp)/(max_temp-min_temp)))

        logger.info(f"Set fan speed to {speed} for temperature {actual_temperature}")
        pwm.start(speed)

        time.sleep(refresh_time)


__main__()