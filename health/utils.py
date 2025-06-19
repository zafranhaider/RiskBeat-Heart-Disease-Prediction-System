import pandas as pd
import numpy as np
from xgboost import XGBClassifier
import os

FEATURE_NAME_MAP = {}  # Optional: name mappings for UI

def prdict_heart_disease(list_data):
    # 1. Load dataset
    df = pd.read_csv('./Machine_Learning/heart.csv')
    df['target'] = np.where(df['thalach'] > 220, 1, df['target'])

    X = df.drop("target", axis=1)
    y = df['target']

    from sklearn.model_selection import train_test_split
    X_train, X_test, y_train, y_test = train_test_split(X, y, train_size=0.92, random_state=0)

    # 2. Define model path
    model_path = './Machine_Learning/heart.json'

    # 3. Create model
    model = XGBClassifier(
        n_estimators=62,
        max_depth=3,
        learning_rate=0.09,
        subsample=0.94,
        colsample_bytree=0.95,
        reg_alpha=0.68,
        reg_lambda=4.78,
        random_state=0,
        use_label_encoder=False,
        eval_metric="logloss"
    )

    # 4. Load or train model
    if os.path.exists(model_path):
        model.load_model(model_path)
        print("✅ Model loaded.")
    else:
        print("⚠️ Model not found, training...")
        model.fit(X_train, y_train)
        model.save_model(model_path)
        print("✅ Model trained & saved.")

    # 5. Predict
    list_data = np.array([list_data], dtype=np.float32)
    pred = model.predict(list_data)

    # 6. Feature importance
    feature_importances = model.feature_importances_
    feature_names = X.columns
    important_factors = sorted(
        [(FEATURE_NAME_MAP.get(feature_names[i], feature_names[i]), feature_importances[i]) for i in range(len(feature_names))],
        key=lambda x: x[1],
        reverse=True
    )

    accuracy = model.score(X_test, y_test) * 100
    return accuracy, pred, important_factors
