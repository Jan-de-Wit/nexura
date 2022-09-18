-- Outputs the average energy of songs by Drake
SELECT AVG(energy) FROM songs WHERE artist_id = (SELECT id FROM artists WHERE name = "Drake")