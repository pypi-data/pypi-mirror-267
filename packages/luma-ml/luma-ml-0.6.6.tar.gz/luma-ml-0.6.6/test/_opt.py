import __local__
from luma.neural.optimizer import NAdamOptimizer

import matplotlib.pyplot as plt
import numpy as np


x = np.linspace(-5, 5, 100)
y = np.linspace(-5, 5, 100)
x, y = np.meshgrid(x, y)
z = x**2 - y**2

x_cur, y_cur = 4.5, -0.1
x_path, y_path = [x_cur], [y_cur]

opt = NAdamOptimizer(learning_rate=0.01)

for i in range(500):
    grad_x = 2 * x_cur
    grad_y = -2 * y_cur

    x_opt, y_opt = opt.update(
        weights=[x_cur], biases=[y_cur], grad_weights=[grad_x], grad_biases=[grad_y]
    )
    x_cur, y_cur = x_opt[0], y_opt[0]

    if i % 50 == 0:
        x_path.append(x_cur)
        y_path.append(y_cur)

z_path = [x**2 - y**2 for x, y in zip(x_path, y_path)]

fig = plt.figure(figsize=(6, 5))
ax = fig.add_subplot(1, 1, 1, projection="3d")

ax.plot_surface(x, y, z, cmap="coolwarm", alpha=0.7, label="Loss Surface")
ax.plot(
    x_path,
    y_path,
    z_path,
    color="r",
    marker="o",
    markersize=5,
    label="Optimization Path",
)
ax.set_xlabel("$w_0$")
ax.set_ylabel("$w_1$")
ax.set_zlabel("Loss")
ax.set_xlim(-5, 5)
ax.set_ylim(-5, 5)
ax.set_zlim(z.min() - 5, z.max() + 5)
ax.set_title(f"{type(opt).__name__} Result")
ax.legend()

plt.tight_layout()
plt.show()
