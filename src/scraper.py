from google_play_scraper import reviews, Sort
import pandas as pd

def scrape_app_reviews(app_id, bank_name, target_count=400):
    all_reviews = []
    continuation_token = None

    while len(all_reviews) < target_count:
        result, continuation_token = reviews(
            app_id,
            lang='en',
            country='us',
            sort=Sort.NEWEST,
            count=200,  # fetch in batches
            continuation_token=continuation_token
        )

        if not result:
            break  # no more reviews available

        for r in result:
            all_reviews.append({
                "review": r["content"],
                "rating": r["score"],
                "date": r["at"],
                "bank": bank_name,
                "source": "Google Play",
                "review_id": r["reviewId"]
            })

        print(f"{bank_name}: Collected {len(all_reviews)} reviews")

        if continuation_token is None:
            break  # reached end

    return pd.DataFrame(all_reviews[:target_count])

def scrape_all():
    apps = {
        "CBE": "com.combanketh.mobilebanking",
        "Dashen": "com.dashen.dashensuperapp",
        "Awash": "com.awashbank.mobile"
    }
    for name, app_id in apps.items():
        print(f"Scraping {name}...")
        df_list = []

    for bank, app_id in apps.items():
        df = scrape_app_reviews(app_id, bank, target_count=400)
        df_list.append(df)

    final_df = pd.concat(df_list, ignore_index=True)

    print(f"Total collected: {len(final_df)}")

    final_df.to_csv("data/raw_reviews.csv", index=False)

if __name__ == "__main__":
    scrape_all()