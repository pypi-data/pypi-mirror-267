from sklearn.datasets import make_classification
from sklearn.model_selection import train_test_split
from SAMMEC2 import AdaBoostClassifier_C2V2
from SAMMEC2 import GA_SAMMEC2

X,y = make_classification(n_samples=10000, n_features=50, n_informative=50, n_redundant=0, n_repeated=0, n_classes=3,
                          n_clusters_per_class=2,class_sep=2,flip_y=0,weights=[0.96,0.035,0.005], random_state=16)

X_train,X_test,y_train,y_test=train_test_split(X,y,random_state=1)

GA_SAMMEC2(n_class=3,
           err=0.01,
           size=2,
           generations=2,
           n_estimators=200,
           random_state=50).fit(X_train,y_train,X_test,y_test)