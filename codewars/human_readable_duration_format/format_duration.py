

def format_duration(n):
    import re
    
    text=[]
    and_deliminated_text=[]

    year= n // ( 24 * 3600 * 365)
    if year>1:
      text.append(str(year) + " years")
    elif year==1:
      text.append(str(year) + " year")
    else:
      pass

    if year>=1:
      day = n // (24 * 3600)
      day = day - (365 * year) #remove the days counted as years
    else:
      day = n // (24 * 3600)
    
    if day>1:
      text.append(str(day) + " days")
    elif day==1: 
      text.append(str(day) + " day")
    else:
      pass

    n = n % (24 * 3600)
    hour = n // 3600

    if hour ==1: 
      text.append(str(hour) + " hour")
    elif hour>1:
      text.append(str(hour) + " hours")
    else: 
      pass

    n %= 3600
    minutes = n // 60

    if minutes ==1: 
      text.append(str(minutes) + " minute")
    elif minutes >1:
      text.append(str(minutes) + " minutes")
    else: 
      pass

    n %= 60
    seconds = n

    if seconds > 1:
      text.append(str(seconds) + " seconds")
    elif seconds==1:
      text.append(str(seconds) + " second")
    else:
      pass
      
    
    #Format sillyness
    if len(text) > 1:
        last_part=text[-1]
        first_part=text.remove(last_part)
        first_part=(", ". join(text))#joined by ', '
        return first_part + " and " + last_part
        
    elif len(text) ==0:
        return 'now'
    else:
        return text[-1]
    