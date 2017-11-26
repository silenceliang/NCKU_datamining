from sklearn.ensemble import ExtraTreesClassifier


def Extra_tree(train_data, target):
    model = ExtraTreesClassifier()
    model.fit(train_data, target)
    print(model.feature_importances_)
