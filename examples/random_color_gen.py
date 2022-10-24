
import matplotlib.pyplot as plt
import random
no_of_colors=7
color=["#"+''.join([random.choice('0123456789ABCDEF') for i in range(8)])
       for j in range(no_of_colors)]
print(color)
for j in range(no_of_colors):
    plt.scatter(random.randint(0,100),random.randint(0,100),c=color[j],s=200)
plt.show()