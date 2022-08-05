import matplotlib.pyplot as plt
year=[ 1950, 1970, 1990, 2010, 2020]
pop=[2.519, 3.692, 5.263, 6.972, 7.9] #billions

#add data from wikiopedia found later
year=[1800,1850,1900] + year
pop = [1.0,1.262, 1.650] + pop


plt.xlabel('Year')
plt.ylabel('Total World Population')
plt.title('World Population Projections')
#plt.yticks([0,2,4,6,8,10])#make it clear the population starts with 0
plt.yticks([0,2,4,6,8,10],
           ['0','2B','4B','6B','8B','10B']) #map strings to numbers
col={ 0:'green',
      2:'green',
      4:'yellow',
      6:'yellow',
      8:'red',
      10:'red'
}
#plt.plot(year,pop) #line plot
plt.scatter(year,pop,alpha=0.8) #scatter plot
plt.show()