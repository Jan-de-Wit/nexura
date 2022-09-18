-- Outputs the names of all people who starred in a movie in which Kevin Bacon also starred
SELECT name, id FROM people
WHERE id IN
(SELECT movies.id FROM movies
INNER JOIN stars ON movies.id = stars.movie_id
INNER JOIN people ON stars.person_id = people.id
WHERE people.name = "Kevin Bacon" AND birth = "1958");