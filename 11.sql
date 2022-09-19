-- Outputs the top 5 highest rated movies (in order)
-- that Chadwick Boseman starred in, starting with the highest rated
SELECT title FROM movies
INNER JOIN stars ON movies.id = stars.movie_id
INNER JOIN ratings ON movies.id = ratings.movie_id
WHERE stars.person_id = (SELECT id FROM people WHERE name = "Chadwick Boseman")
ORDER BY ratings.rating DESC
LIMIT 5;