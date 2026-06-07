import sqlite3
import pandas as pd

from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import GroupShuffleSplit
from sklearn.metrics import accuracy_score

import joblib

DB_NAME = "database/fatigue_logs.db"


def load_features():

    conn = sqlite3.connect(
        DB_NAME
    )

    df = pd.read_sql_query(
        "SELECT * FROM features",
        conn
    )

    conn.close()

    return df


def main():

    df = load_features()

    print(
        f"\nTotal Samples: {len(df)}"
    )

    print(
        f"Total Sessions: "
        f"{df['session_id'].nunique()}"
    )

    if len(df) < 20:

        print(
            "\nNot enough data for "
            "session-level evaluation."
        )

        return

    X = df[
        [
            "iki_variance",
            "backspace_ratio",
            "dwell_time",
            "typing_speed",
            "mouse_activity",
            "click_count",
            "app_switch_rate"
        ]
    ]

    y = df["fatigue_label"]

    groups = df["session_id"]

    splitter = GroupShuffleSplit(
        n_splits=1,
        test_size=0.2,
        random_state=42
    )

    train_idx, test_idx = next(
        splitter.split(
            X,
            y,
            groups
        )
    )

    X_train = X.iloc[
        train_idx
    ]

    X_test = X.iloc[
        test_idx
    ]

    y_train = y.iloc[
        train_idx
    ]

    y_test = y.iloc[
        test_idx
    ]

    print(
        f"\nTraining Samples: "
        f"{len(X_train)}"
    )

    print(
        f"Testing Samples: "
        f"{len(X_test)}"
    )

    print(
        f"Training Sessions: "
        f"{df.iloc[train_idx]['session_id'].nunique()}"
    )

    print(
        f"Testing Sessions: "
        f"{df.iloc[test_idx]['session_id'].nunique()}"
    )

    model = RandomForestClassifier(
        n_estimators=200,
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
        f"\nSession-Level Accuracy: "
        f"{accuracy:.4f}"
    )

    print(
        "\n===== FEATURE IMPORTANCE =====\n"
    )

    feature_names = [
        "iki_variance",
        "backspace_ratio",
        "dwell_time",
        "typing_speed",
        "mouse_activity",
        "click_count",
        "app_switch_rate"
    ]

    for name, importance in zip(
        feature_names,
        model.feature_importances_
    ):

        print(
            f"{name}: "
            f"{importance:.4f}"
        )

    joblib.dump(
        model,
        "models/fatigue_model_session.pkl"
    )

    print(
        "\n===== MODEL SAVED ====="
    )

    print(
        "models/fatigue_model_session.pkl"
    )


if __name__ == "__main__":
    main()