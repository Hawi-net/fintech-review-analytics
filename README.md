# Fintech Review Analytics

## 📌 Project Overview

This project collects and analyzes user reviews from Google Play Store for Ethiopian banking applications.

## 📊 Data Collection

* Source: Google Play Store
* Library: google-play-scraper
* Apps:

  * Commercial Bank of Ethiopia (CBE)
  * Dashen Bank
  * Awash Bank
* Target: Minimum 400 reviews per bank (1,200 total)

## ⚙️ Methodology

* Reviews were scraped using pagination to ensure sufficient data.
* Data collected:

  * Review text
  * Rating (1–5)
  * Review date
  * Bank name
  * Source

## 🧹 Preprocessing

* Removed duplicate reviews using review_id
* Dropped rows with missing review or rating
* Normalized date format to YYYY-MM-DD
* Final dataset includes:
  review, rating, date, bank, source

## ⚠️ Limitations

* Some apps may have fewer available reviews
* API rate limits may restrict full data extraction
* Only English reviews were targeted

## ✅ KPIs Achieved

* 1,200+ reviews collected
* Less than 5% missing data
* Clean structured dataset
* CI/CD pipeline configured
