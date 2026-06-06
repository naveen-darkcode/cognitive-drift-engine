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

    print("\nDataset Loaded\n")
    print(df)

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

    joblib.dump(
        model,
        "models/fatigue_model.pkl"
    )

    print(
        "\nModel saved as:"
    )

    print(
        "models/fatigue_model.pkl"
    )


if __name__ == "__main__":
    main()