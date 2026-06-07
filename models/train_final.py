import sqlite3
import pandas as pd
import joblib

from sklearn.ensemble import ExtraTreesClassifier


DB_NAME = "database/fatigue_logs.db"
MODEL_PATH = "models/fatigue_model.pkl"


def convert_label(label):

    if label <= 3:
        return "LOW"

    elif label <= 6:
        return "MEDIUM"

    else:
        return "HIGH"


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

    print("\n===== TRAINING FINAL MODEL =====\n")

    print(
        f"Total Samples: {len(df)}"
    )

    if df.empty:

        print(
            "\nNo feature data found."
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

    y = df["fatigue_label"].apply(
        convert_label
    )

    print(
        "\n===== LABEL DISTRIBUTION =====\n"
    )

    print(
        y.value_counts()
    )

    model = ExtraTreesClassifier(
        n_estimators=200,
        class_weight="balanced",
        random_state=42
    )

    model.fit(
        X,
        y
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
        MODEL_PATH
    )

    print(
        "\n===== FINAL MODEL SAVED ====="
    )

    print(
        MODEL_PATH
    )

    print(
        "\nModel trained on ALL available data."
    )


if __name__ == "__main__":
    main()