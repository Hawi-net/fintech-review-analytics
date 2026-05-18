import pandas as pd
import re

def clean_text(text):
    text = text.lower()
    text = re.sub(r'http\S+', '', text)   # remove URLs
    text = re.sub(r'[^a-z\s]', '', text)  # remove special chars
    text = re.sub(r'\s+', ' ', text).strip()
    return text


def preprocess_data(input_path="data/raw_reviews.csv"):
    df = pd.read_csv(input_path)

    df.dropna(subset=["review"], inplace=True)

    df["clean_review"] = df["review"].apply(clean_text)

    df["date"] = pd.to_datetime(df["date"])

    df.to_csv("data/clean_reviews.csv", index=False)

    print("Clean dataset saved to data/clean_reviews.csv")

    return df


if __name__ == "__main__":
    preprocess_data()