import pandas as pd
date1 = '2011-05-03'
date2 = '2011-05-10'
#mydates = pd.date_range(date1, date2).tolist()
mydates = pd.date_range(date1, date2).tolist()
for ldate in mydates:
    print (ldate)

