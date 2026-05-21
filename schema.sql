-- Verification Query 1: Count reviews per bank
SELECT b.bank_name, COUNT(r.review_id) AS total_reviews
FROM reviews r
JOIN banks b ON r.bank_id = b.bank_id
GROUP BY b.bank_name;

-- Verification Query 2: Compute average rating per bank
SELECT b.bank_name, AVG(r.rating) AS average_star_rating
FROM reviews r
JOIN banks b ON r.bank_id = b.bank_id
GROUP BY b.bank_name;

-- Verification Query 3: Structural Integrity Check for Null Data fields
SELECT COUNT(*) AS corrupt_records 
FROM reviews 
WHERE bank_id IS NULL OR rating IS NULL;