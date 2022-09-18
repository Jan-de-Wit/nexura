-- Outputs the names of the songs from Post Malone
SELECT name FROM songs WHERE artist_id = (SELECT id FROM artists WHERE name = "Post Malone");