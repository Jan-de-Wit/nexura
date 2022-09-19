-- Outputs all movies released in 2010 and their ratings in descending order by rating
-- If ratings are the same it will be ordered alphabetically
SELECT movies.title, ratings.rating FROM movies
INNER JOIN ratings ON movies.id = ratings.movie_id
WHERE year = "2010"
ORDER BY ratings.rating DESC, movies.title;