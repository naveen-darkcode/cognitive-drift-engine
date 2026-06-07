import pandas as pd

from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

import joblib


def load_dataset():

    return pd.read_csv(
        "combined_features.csv"
    )


def main():

    df = load_dataset()

    print("\n===== COMBINED DATASET =====\n")

    print(df.head())

    print(
        f"\nTotal Samples: {len(df)}"
    )

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
        f"\nAccuracy: {accuracy:.4f}"
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

    for name, importance in zip(
        feature_names,
        model.feature_importances_
    ):

        print(
            f"{name}: {importance:.4f}"
        )

    joblib.dump(
        model,
        "models/fatigue_model_combined.pkl"
    )

    print(
        "\nModel saved:"
    )

    print(
        "models/fatigue_model_combined.pkl"
    )


if __name__ == "__main__":
    main()