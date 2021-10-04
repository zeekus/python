# quick start : Selenium

```
  pip3 install bs4
  pip3 install request
  pip3 install requests
  pip3 install chromedriver
  sudo pacman -Syuu chromium
```

basic code

```
#!/usr/bin/python
from bs4 import BeautifulSoup

with open ('home.html', 'r' ) as html_file:
   content = html_file.read()
   print(content)
```


split by price when everything on same line

```
sep = ','
con_price = price.split(sep, 1)[0]
converted_price = int(con_price.replace('.', ''))
```

weather example

```
page = requests.get("https://forecast.weather.gov/MapClick.php?lat=38.9768&lon=-76.4901")
soup = BeautifulSoup(page.content, 'html.parser')
seven_day = soup.find(id="seven-day-forecast")
forecast_items = seven_day.find_all(class_="tombstone-container")
tonight = forecast_items[0]
print(tonight.prettify())
```

weather example parse

```
period = tonight.find(class_="period-name").get_text()
short_desc = tonight.find(class_="short-desc").get_text()
temp = tonight.find(class_="temp").get_text()
print(period)
print(short_desc)
print(temp)
```

weather example parse2

```
img = tonight.find("img")
desc = img['title']
print(desc)
```

weather example parse3 panda parse frames

```
import pandas as pd
weather = pd.DataFrame({
    "period": periods,
    "short_desc": short_descs,
    "temp": temps,
    "desc":descs
})
weather
```





from 

source : https://www.youtube.com/watch?v=XVv6mJpFOb0

soruce : https://towardsdatascience.com/top-5-beautiful-soup-functions-7bfe5a693482