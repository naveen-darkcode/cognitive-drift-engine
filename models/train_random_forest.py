import sqlite3
import pandas as pd

from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

import joblib


DB_NAME = "database/fatigue_logs.db"


def load_features():

    conn = sqlite3.connect(DB_NAME)

    df = pd.read_sql_query(
        "SELECT * FROM features",
        conn
    )

    conn.close()

    return df


def main():

    df = load_features()

    print("\n===== DATASET LOADED =====\n")

    print(df)

    print(
        f"\nTotal Samples: {len(df)}"
    )

    if len(df) < 10:

        print(
            "\nNot enough training data.\n"
            "Collect more sessions first."
        )

        return

    X = df[
        [
            "iki_variance",
            "backspace_ratio",
            "dwell_time",
            "mouse_activity",
            "app_switch_rate"
        ]
    ]

    y = df["fatigue_label"]

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.2,
        random_state=42
    )

    print(
        f"\nTraining Samples: {len(X_train)}"
    )

    print(
        f"Testing Samples: {len(X_test)}"
    )

    model = RandomForestClassifier(
        n_estimators=100,
        random_state=42
    )

    model.fit(
        X_train,
        y_train
    )

    predictions = model.predict(
        X_test
    )

    accuracy = accuracy_score(
        y_test,
        predictions
    )

    print(
        f"\nAccuracy: {accuracy:.2f}"
    )

    print(
        "\n===== FEATURE IMPORTANCE =====\n"
    )

    feature_names = [
        "iki_variance",
        "backspace_ratio",
        "dwell_time",
        "mouse_activity",
        "app_switch_rate"
    ]

    importances = (
        model.feature_importances_
    )

    for name, importance in zip(
        feature_names,
        importances
    ):

        print(
            f"{name}: "
            f"{importance:.4f}"
        )

    joblib.dump(
        model,
        "models/fatigue_model.pkl"
    )

    print(
        "\n===== MODEL SAVED ====="
    )

    print(
        "models/fatigue_model.pkl"
    )


if __name__ == "__main__":
    main()