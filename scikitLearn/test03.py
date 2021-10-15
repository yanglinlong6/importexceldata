from sklearn import datasets
from sklearn.datasets import load_iris

iris = datasets.load_iris()  # 导入数据集
X = iris.data  # 获得其特征向量
y = iris.target  # 获得样本label

X, y = load_iris(return_X_y=True)
print(X.shape, y.shape, type(X))
data = load_iris(return_X_y=False)
print(type(data))
