import sqlite3
import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix
)

from sklearn.ensemble import (
    RandomForestClassifier,
    ExtraTreesClassifier,
    GradientBoostingClassifier
)


DB_NAME = "database/fatigue_logs.db"


def convert_label(label):

    if label <= 3:
        return "LOW"

    elif label <= 6:
        return "MEDIUM"

    else:
        return "HIGH"


def main():

    conn = sqlite3.connect(DB_NAME)

    df = pd.read_sql_query(
        "SELECT * FROM features",
        conn
    )

    conn.close()

    print(
        f"\nTotal Samples: {len(df)}"
    )

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

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.2,
        random_state=42,
        stratify=y
    )

    models = {

        "Random Forest":
        RandomForestClassifier(
            n_estimators=200,
            class_weight="balanced",
            random_state=42
        ),

        "Extra Trees":
        ExtraTreesClassifier(
            n_estimators=200,
            class_weight="balanced",
            random_state=42
        ),

        "Gradient Boosting":
        GradientBoostingClassifier(
            random_state=42
        )
    }

    results = {}

    best_model_name = None
    best_accuracy = 0
    best_predictions = None

    print(
        "\n===== MODEL COMPARISON =====\n"
    )

    for name, model in models.items():

        model.fit(
            X_train,
            y_train
        )

        preds = model.predict(
            X_test
        )

        acc = accuracy_score(
            y_test,
            preds
        )

        results[name] = acc

        print(
            f"{name}: "
            f"{acc:.4f}"
        )

        if acc > best_accuracy:

            best_accuracy = acc
            best_model_name = name
            best_predictions = preds

    print(
        "\n===== BEST MODEL =====\n"
    )

    print(
        f"{best_model_name}"
    )

    print(
        f"Accuracy: "
        f"{best_accuracy:.4f}"
    )

    print(
        "\n===== EXTRA TREES REPORT =====\n"
    )

    extra_trees = ExtraTreesClassifier(
        n_estimators=200,
        class_weight="balanced",
        random_state=42
    )

    extra_trees.fit(
        X_train,
        y_train
    )

    extra_preds = extra_trees.predict(
        X_test
    )

    print(
        classification_report(
            y_test,
            extra_preds,
            zero_division=0
        )
    )

    print(
        "\n===== EXTRA TREES CONFUSION MATRIX =====\n"
    )

    print(
        confusion_matrix(
            y_test,
            extra_preds
        )
    )


if __name__ == "__main__":
    main()