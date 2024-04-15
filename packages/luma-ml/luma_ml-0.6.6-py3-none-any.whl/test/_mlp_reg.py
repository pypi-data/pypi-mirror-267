import __local__
from luma.preprocessing.scaler import StandardScaler
from luma.model_selection.split import TrainTestSplit
from luma.neural.network import MLPRegressor
from luma.neural.optimizer import *
from luma.metric.regression import RootMeanSquaredError
from luma.visual.evaluation import ResidualPlot

from sklearn.datasets import load_diabetes
import matplotlib.pyplot as plt
import numpy as np

np.random.seed(42)

X, y = load_diabetes(return_X_y=True)

sc = StandardScaler()
X_std = sc.fit_transform(X)
y_std = sc.fit_transform(y)

X_train, X_test, y_train, y_test = TrainTestSplit(
    X_std,
    y_std,
    test_size=0.3,
    shuffle=True,
).get

X_train, X_val, y_train, y_val = TrainTestSplit(
    X_train,
    y_train,
    test_size=0.2,
    shuffle=True,
).get

X_all = np.vstack((X_train, X_val, X_test))
y_all = np.hstack((y_train, y_val, y_test))

optimizers = [
    SGDOptimizer,
    MomentumOptimizer,
    RMSPropOptimizer,
    AdamOptimizer,
    AdaGradOptimizer,
    AdaDeltaOptimizer,
    AdaMaxOptimizer,
    AdamWOptimizer,
    NAdamOptimizer,
]

param_dict = {
    "input_size": X.shape[1],
    "hidden_sizes": 16,
    "max_epoch": 1000,
    "batch_size": 100,
    "learning_rate": 0.001,
    "activation": "relu",
    "momentum": 0.3,
}

mlps = [MLPRegressor(**param_dict, optimizer=opt()) for opt in optimizers]

best_mlp = None
best_score = np.inf

fig = plt.figure(figsize=(12, 5))
ax1 = fig.add_subplot(1, 2, 1)
ax2 = fig.add_subplot(1, 2, 2)

for mlp in mlps:
    mlp.fit(X_train, y_train)
    val_score = mlp.score(X_val, y_val, metric=RootMeanSquaredError)
    print(f"Done fitting for {type(mlp.optimizer).__name__}")

    if val_score < best_score:
        best_score = val_score
        best_mlp = mlp

    ax1.plot(
        mlp.batch_losses_, lw=0.5, label=f"{type(mlp.optimizer).__name__}", alpha=0.7
    )

print(f"Best optimizer: {type(best_mlp.optimizer).__name__}")
best_score = best_mlp.score(X_test, y_test, metric=RootMeanSquaredError)

ax1.set_xlabel("Batches")
ax1.set_ylabel("Loss")
ax1.set_title(
    f"MLP for Various Optimizers [Best RMSE: {best_score:.4f}]"
)
ax1.legend()
ax1.grid(alpha=0.2)

res = ResidualPlot(best_mlp, X_all, y_all)
res.plot(ax=ax2, show=True)
