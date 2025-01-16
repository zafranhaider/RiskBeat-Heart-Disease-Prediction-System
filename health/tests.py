# from django.test import TestCase
# from sklearn.model_selection import train_test_split
# from sklearn.model_selection import GridSearchCV
# from xgboost import XGBClassifier
# from views import *
# # Split the dataset
# X_train, X_test, y_train, y_test = train_test_split(
#     X[['age', 'sex', 'cp', 'trestbps', 'chol', 'fbs', 'restecg', 'thalach', 'exang', 'oldpeak', 'slope', 'ca', 'thal']],
#     y,
#     train_size=0.8,
#     random_state=0
# )



# # Define the parameter grid
# param_grid = {
#     'n_estimators': [50, 100, 200],
#     'learning_rate': [0.01, 0.1, 0.2],
#     'max_depth': [3, 5, 7],
#     'min_child_weight': [1, 3, 5],
#     'gamma': [0, 0.1, 0.2],
#     'subsample': [0.8, 0.9, 1.0],
#     'colsample_bytree': [0.8, 0.9, 1.0]
# }

# # Initialize the model
# xgb = XGBClassifier(random_state=0)

# # Perform Grid Search
# grid_search = GridSearchCV(estimator=xgb, param_grid=param_grid, cv=3, scoring='accuracy', verbose=2)
# grid_search.fit(X_train, y_train)

# # Retrieve the best parameters
# best_params = grid_search.best_params_
# print("Best Parameters:", best_params)


# # Train the XGBoost model with the best parameters
# xgb_optimized = XGBClassifier(**best_params, random_state=0)
# xgb_optimized.fit(X_train, y_train)


# from sklearn.metrics import accuracy_score, classification_report

# # Predict on the test set
# y_pred = xgb_optimized.predict(X_test)

# # Evaluate accuracy
# accuracy = accuracy_score(y_test, y_pred)
# print(f"Test Set Accuracy: {accuracy * 100:.2f}%")

# # Detailed classification report
# print(classification_report(y_test, y_pred))
