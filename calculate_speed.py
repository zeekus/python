#/usr/bin/python3
#filename: calculate_speed.py
#description: calculate the avg speed. 

def calculate_speed(distance, time):
    speed = distance / (time / 60)  # Convert time to hours
    return speed

distance = float(input("Enter the distance in miles: "))
time_minutes = float(input("Enter the time in minutes: "))

speed = calculate_speed(distance, time_minutes)
speed=round(speed,2)
print(f"Speed: {speed} mph")
