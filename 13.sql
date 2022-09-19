-- Outputs the names of all people who starred in a movie in which Kevin Bacon also starred
SELECT name FROM people
WHERE id IN (
    -- Gets all person ids of who starred in a movie in which Kevin Bacon also starred
    SELECT person_id FROM stars
    WHERE movie_id IN (
        -- Gets all movie ids in which Kevin Bacon starred
        SELECT movie_id FROM stars
        INNER JOIN people ON stars.person_id = people.id
        WHERE people.name = "Kevin Bacon" AND people.birth = "1958"
    )
)
AND name != "Kevin Bacon";