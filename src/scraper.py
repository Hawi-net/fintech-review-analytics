apps = {
    "CBE": "com.combanketh.mobilebanking",
    "Dashen": "com.dashen.dashensuperapp",
    "Awash": "com.awashbank.mobile"
}
from google_play_scraper import reviews, Sort
import pandas as pd

def scrape_app_reviews(app_id, app_name, count=1000):
    result, _ = reviews(
        app_id,
        lang='en',
        country='us',
        sort=Sort.NEWEST,
        count=count
    )

    data = []
    for r in result:
        data.append({
            "app_name": app_name,
            "review": r["content"],
            "rating": r["score"],
            "date": r["at"]
        })

    return pd.DataFrame(data)


def scrape_all_apps():
    apps = {
        "Bank1": "com.example.bank1",
        "Bank2": "com.example.bank2",
        "Bank3": "com.example.bank3"
    }

    df_list = []

    for name, app_id in apps.items():
        print(f"Scraping {name}...")
        df = scrape_app_reviews(app_id, name)
        df_list.append(df)

    final_df = pd.concat(df_list, ignore_index=True)

    final_df.to_csv("data/raw_reviews.csv", index=False)
    print("Saved to data/raw_reviews.csv")

    return final_df


if __name__ == "__main__":
    scrape_all_apps()