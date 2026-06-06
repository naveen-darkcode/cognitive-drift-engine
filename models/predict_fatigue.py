import sqlite3
import pandas as pd
import joblib

DB_NAME = "database/fatigue_logs.db"


def load_latest_features():

    conn = sqlite3.connect(DB_NAME)

    query = """
    SELECT *
    FROM features
    ORDER BY id DESC
    LIMIT 1
    """

    df = pd.read_sql_query(
        query,
        conn
    )

    conn.close()

    return df


def main():

    print(
        "\nLoading fatigue model..."
    )

    model = joblib.load(
        "models/fatigue_model.pkl"
    )

    df = load_latest_features()

    if df.empty:

        print(
            "No features found."
        )

        return

    print(
        "\nLatest Feature Row\n"
    )

    print(df)

    X = df[
        [
            "iki_variance",
            "backspace_ratio",
            "dwell_time",
            "mouse_activity",
            "app_switch_rate"
        ]
    ]

    prediction = model.predict(X)

    probabilities = model.predict_proba(X)

    confidence = (
        max(probabilities[0]) * 100
    )

    print(
        "\n===== FATIGUE PREDICTION ====="
    )

    print(
        f"Predicted Fatigue Level: "
        f"{prediction[0]}"
    )

    print(
        f"Confidence: "
        f"{confidence:.2f}%"
    )

    print(
        "\n=============================="
    )


if __name__ == "__main__":
    main()