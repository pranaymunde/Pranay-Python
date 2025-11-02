# First, install matplotlib if not already installed
# pip install matplotlib

import matplotlib.pyplot as plt  # ✅ You need to import matplotlib.pyplot

# Line Graph
x = [1, 2, 3, 4, 5]
y = [2, 4, 6, 8, 10]

# ✅ 'market' should be 'marker'
plt.plot(x, y, color='blue', marker='o')

plt.title("Line Plot")
plt.xlabel("X-axis")
plt.ylabel("Y-axis")

plt.show()
