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
            "typing_speed",
            "mouse_activity",
            "click_count",
            "app_switch_rate"
        ]
    ]

    prediction = model.predict(X)

    probabilities = model.predict_proba(X)

    confidence = round(
        max(probabilities[0]) * 100,
        1
    )

    confidence = min(
        confidence,
        95.0
    )

    result = {

        "fatigue_level":
        str(prediction[0]),

        "confidence":
        confidence,

        "features": {

            "iki_variance":
            float(df.iloc[0]["iki_variance"]),

            "backspace_ratio":
            float(df.iloc[0]["backspace_ratio"]),

            "dwell_time":
            float(df.iloc[0]["dwell_time"]),

            "typing_speed":
            float(df.iloc[0]["typing_speed"]),

            "mouse_activity":
            int(df.iloc[0]["mouse_activity"]),

            "click_count":
            int(df.iloc[0]["click_count"]),

            "app_switch_rate":
            int(df.iloc[0]["app_switch_rate"])
        }
    }

    print(
        "\n===== FATIGUE PREDICTION =====\n"
    )

    print(result)

    print(
        "\n=============================="
    )


if __name__ == "__main__":
    main()