import matplotlib.pyplot as plt
import numpy as np

# 生成自定义的 x 值数组
x_values = np.arange(0, 3.1, 0.5)

# 绘制数据
y_values = [2, 3, 5, 7, 11, 13, 17]
plt.plot(x_values, y_values)

# 添加标题和轴标签
plt.title('Plot with Custom X-axis Sampling Points')
plt.xlabel('X-axis')
plt.ylabel('Y-axis')

# 在每个数据点处添加 x 值的标签
for x, y in zip(x_values, y_values):
    plt.text(x, y, f'{x:.2f}', ha='center', va='bottom')

# 显示图形
plt.show()