import ephem
from datetime import date, timedelta, datetime
#filename: track_moon_phase.py
#description: get the moon phase based on a date input

def get_moon_phase(date):
    # Create an observer object for your location
    observer = ephem.Observer()
    observer.lat = '38.98'
    observer.lon = '76.51'

    # Create a moon object for the given date
    moon = ephem.Moon()
    moon.compute(date)

    # Get the phase of the moon
    phase = round(moon.phase/100,4)
    print(f"phase: {phase}")

    # Determine the moon phase name
    if phase < .03 :
        moon_phase = "New Moon"
    elif 0.03 <= phase < 0.5:
        moon_phase = "First Quarter"
    elif 0.5 <= phase < 0.53:
        moon_phase = "Super Moon"
    elif 0.53 <= phase < 0.97:
        moon_phase = "Last Quarter"
    else:
        moon_phase = "Full Moon"

    return moon_phase

# Example usage
#mydate="2023/8/31 22:30"

# Read a date string from stdin
date_str = input("Enter a date (YYYY-MM-DD HH:MM) or press enter for today: ")
if date_str == "":
    now = datetime.now()
    date_str=now.strftime("%Y-%m-%d %H:%M")

# Convert the date string to a date object
date_obj = datetime.strptime(date_str, "%Y-%m-%d %H:%M")
#date_obj = datetime.strptime(date_str, "%Y-%m-%d %H:%M").date() #removes hour mins

date = ephem.date(date_obj)
print(f'debug: date selected: {date_obj}')
moon_phase = get_moon_phase(date_obj)
print(f"{date_obj} moon phase is/was/will-be: {moon_phase}")
