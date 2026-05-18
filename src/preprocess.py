import pandas as pd

def preprocess():
    df = pd.read_csv("data/raw_reviews.csv")

    print(f"Original size: {len(df)}")

    # ✅ Remove duplicates using review_id
    df = df.drop_duplicates(subset=["review_id"])

    # ✅ Handle missing values
    before = len(df)
    df = df.dropna(subset=["review", "rating"])
    after = len(df)

    print(f"Removed {before - after} rows with missing values")

    # ✅ Normalize date
    df["date"] = pd.to_datetime(df["date"]).dt.strftime("%Y-%m-%d")

    # ✅ Keep only required columns
    df = df[["review", "rating", "date", "bank", "source"]]

    print(f"Final dataset size: {len(df)}")

    df.to_csv("data/clean_reviews.csv", index=False)

if __name__ == "__main__":
    preprocess()