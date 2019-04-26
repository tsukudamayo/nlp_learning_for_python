from sklearn.datasets import load_iris
from sklearn.linear_model import LogisticRegression


X, y = load_iris(return_X_y=True)
clf = LogisticRegression(
    random_state=0,
    solver='liblinear',
).fit(X, y)
print('data')
print(X[:2, :])
print('predict_proba')
print(clf.predict_proba(X[:2, :]))
print('predict')
print(clf.predict(X[:2, :]))
