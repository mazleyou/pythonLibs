from matplotlib import pyplot as plt
import numpy as np

x = np.arange(1,10)
y = x*5

plt.xlim(0, 20)
plt.ylim(0, 100)
plt.plot(x,y,'o')
plt.show()
# plt.savefig('f1/fig1.png', dpi=300)