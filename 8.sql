-- Outputs the names of the people who starred in Toy Story
SELECT name FROM people
INNER JOIN stars ON people.id = stars.person_id
INNER JOIN movies ON stars.movie_id = movies.id
WHERE movies.title = "Toy Story";