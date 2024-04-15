
def ensemble_classification():
    code = """

    import numpy as np
    import pandas as pd
    import os
    from sklearn.preprocessing import LabelEncoder
    import seaborn as sns
    from sklearn.model_selection import cross_val_score
    from sklearn.linear_model import LogisticRegression
    from sklearn.neighbors import KNeighborsClassifier
    from sklearn.ensemble import RandomForestClassifier, VotingClassifier
    from sklearn.svm import SVC
    from sklearn.datasets import make_classification

    # Load Iris dataset
    df = pd.read_csv('Iris.csv')
    df = df.iloc[:, 1:]  # Remove Id column

    # Label encode Species
    encoder = LabelEncoder()
    df['Species'] = encoder.fit_transform(df['Species'])

    # Visualize data
    sns.pairplot(df, hue='Species')

    # Prepare data for classification
    X = df.iloc[:, :2]
    y = df.iloc[:, -1]

    # Define classifiers
    clf1 = LogisticRegression()
    clf2 = RandomForestClassifier()
    clf3 = KNeighborsClassifier()

    # Perform cross-validation for individual classifiers
    estimators = [('lr', clf1), ('rf', clf2), ('knn', clf3)]
    for estimator in estimators:
        scores = cross_val_score(estimator[1], X, y, cv=10, scoring='accuracy')
        print(estimator[0], np.round(np.mean(scores), 2))

    # Perform cross-validation for Voting Classifier
    vc_hard = VotingClassifier(estimators=estimators, voting='hard')
    vc_soft = VotingClassifier(estimators=estimators, voting='soft')
    print("Hard Voting:", np.round(np.mean(cross_val_score(vc_hard, X, y, cv=10, scoring='accuracy')), 2))
    print("Soft Voting:", np.round(np.mean(cross_val_score(vc_soft, X, y, cv=10, scoring='accuracy')), 2))

    # Perform cross-validation for Weighted Voting Classifier
    for i in range(1, 4):
        for j in range(1, 4):
            for k in range(1, 4):
                weights = [i, j, k]
                vc_weighted = VotingClassifier(estimators=estimators, voting='soft', weights=weights)
                scores = cross_val_score(vc_weighted, X, y, cv=10, scoring='accuracy')
                print("Weights:", weights, "Accuracy:", np.round(np.mean(scores), 2))

    # Classifiers of the same algorithm (SVC)
    X, y = make_classification(n_samples=1000, n_features=20, n_informative=15, n_redundant=5, random_state=2)
    svm1 = SVC(probability=True, kernel='poly', degree=1)
    svm2 = SVC(probability=True, kernel='poly', degree=2)
    svm3 = SVC(probability=True, kernel='poly', degree=3)
    svm4 = SVC(probability=True, kernel='poly', degree=4)
    svm5 = SVC(probability=True, kernel='poly', degree=5)

    estimators_svm = [('svm1', svm1), ('svm2', svm2), ('svm3', svm3), ('svm4', svm4), ('svm5', svm5)]

    for estimator in estimators_svm:
        scores = cross_val_score(estimator[1], X, y, cv=10, scoring='accuracy')
        print(estimator[0], np.round(np.mean(scores), 2))

    vc_svm = VotingClassifier(estimators=estimators_svm, voting='soft')
    print("Soft Voting with SVMs:", np.round(np.mean(cross_val_score(vc_svm, X, y, cv=10, scoring='accuracy')), 2))
    """
    print(code)
