-- Outputs the titles of the movies in which both Johnyy Depp
-- and Helena Bonham Carter are starred
SELECT title FROM movies
INNER JOIN stars ON movies.id = stars.movie_id
INNER JOIN people ON stars.person_id = people.id
WHERE people.name = "Johnyy Depp" OR people.name = "Helena Bonham Carter";