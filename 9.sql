-- Outputs all of the names of the people who starred in a movie released in 2004
-- Ordered by birth year
SELECT DISTINCT(name) FROM people
INNER JOIN stars ON people.id = stars.person_id
INNER JOIN movies ON movies.id = stars.movie_id
WHERE movies.year = "2004"
ORDER BY people.birth;