
def adaboost():
    code = """

    import matplotlib.pyplot as plt
    import numpy as np
    from sklearn.datasets import make_circles
    from sklearn.ensemble import AdaBoostClassifier
    from sklearn.model_selection import cross_val_score, GridSearchCV
    from sklearn.model_selection import train_test_split
    from sklearn.preprocessing import StandardScaler

    np.random.seed(42)
    X, y = make_circles(n_samples=500, factor=0.1, noise=0.35, random_state=42)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

    abc = AdaBoostClassifier()
    np.mean(cross_val_score(abc, X, y, scoring='accuracy', cv=10))

    abc.fit(X, y)

    def plot_decision_boundary(clf):
        plt.figure(figsize=(12, 8))
        x_range = np.linspace(X.min(), X.max(), 100)
        xx1, xx2 = np.meshgrid(x_range, x_range)
        y_hat = clf.predict(np.c_[xx1.ravel(), xx2.ravel()])
        y_hat = y_hat.reshape(xx1.shape)
        plt.contourf(xx1, xx2, y_hat, alpha=0.2)
        plt.scatter(X[:,0], X[:,1], c=y, cmap='viridis', alpha=.7)
        plt.title("Adaboost Classifier")
        plt.show()

    plot_decision_boundary(abc)

    abc = AdaBoostClassifier(n_estimators=1500, learning_rate=0.1)
    abc.fit(X, y)
    plot_decision_boundary(abc)

    grid = dict()
    grid['n_estimators'] = [10, 50, 100, 500]
    grid['learning_rate'] = [0.0001, 0.001, 0.01, 0.1, 1.0]
    grid['algorithm'] = ['SAMME', 'SAMME.R']

    grid_search = GridSearchCV(estimator=AdaBoostClassifier(), param_grid=grid, n_jobs=-1, cv=10, scoring='accuracy')
    grid_result = grid_search.fit(X, y)
    print("Best: %f using %s" % (grid_result.best_score_, grid_result.best_params_))
    """
    print(code)
