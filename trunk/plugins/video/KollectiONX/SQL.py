GENRE = """
  SELECT * FROM moviexgenre
   LEFT JOIN genre
    ON genre.id = moviexgenre.genreid
  WHERE movieid = %s
"""

STUDIO = """
  SELECT * FROM moviexstudio
   LEFT JOIN studio
    on studio.id = moviexstudio.studioid
  WHERE movieid = %s
"""

STUDIO_LIST = """
SELECT *, COUNT( studioid ) AS MovieCount
FROM moviexstudio
LEFT JOIN studio ON studio.id = moviexstudio.studioid
GROUP BY studioid
ORDER BY displayname
"""

WRITER = """
  SELECT * FROM moviexwriter
   LEFT JOIN writer
    ON writer.id = moviexwriter.writerid
  WHERE movieid = %s
"""

WRITER_LIST = """
SELECT * ,
 IF( lastname =  '',
     displayname,
     CONCAT( lastname,  ", ", name ) ) AS WriterName,
 COUNT( movieid ) as MovieCount
FROM moviexwriter
LEFT JOIN writer ON writer.id = writerid
GROUP BY writerid
ORDER BY writername
"""

DIRECTOR = """
  SELECT * FROM moviexdirector
   LEFT JOIN director
    ON director.id = moviexdirector.directorid
  WHERE movieid = %s
"""

DIRECTOR_LIST = """
SELECT * ,
 IF( lastname =  '',
     displayname,
     CONCAT( lastname,  ", ", name ) ) AS DirectorName,
 COUNT( movieid ) as MovieCount
FROM moviexdirector
LEFT JOIN director ON director.id = directorid
GROUP BY directorid
ORDER BY directorname
"""

ACTORS = """
  SELECT actor.id AS actorid,
         partxactor.name AS label2,
         IF(lastname='',
            actor.displayname,
            CONCAT_WS(', ',lastname,actor.name)) AS label1,
         IF(partxactor.name='',
            actor.displayname,
            CONCAT_WS('|',actor.displayname,partxactor.name)) AS ActorAsPart
  FROM `partxmovie`
   LEFT JOIN partxactor
    ON partxmovie.partid = partxactor.partid
   LEFT JOIN actor
    ON partxactor.actorid = actor.id
  WHERE movieid = %s
  ORDER BY label1
"""

ALL_MOVIES = """
  SELECT movie.id AS movieid,
         title,
         frontcover,
         plot,
         year.displayname AS year,
         IMDbRating,
         RunningTime,
         audiencerating.displayname AS AudienceRating,
         IF(COUNT(url)=1,url,"") AS movieurl
  FROM movie
   LEFT JOIN moviexlinks
    ON movie.id = moviexlinks.movieid
       AND linktype="movie"
   LEFT JOIN year
    ON moviereleaseyear = year.id
   LEFT JOIN audiencerating
    ON audiencerating = audiencerating.id
  %s
  GROUP BY moviexlinks.movieid
  ORDER BY IF(titlesort = "", title, titlesort)
"""

YEAR_WHERE = """
  WHERE moviereleaseyear = %d
"""

GENRE_WHERE = """
  WHERE movie.id IN(
   SELECT
    movieid
    FROM
     moviexgenre
    WHERE genreid IN(
     %s
    )
 )
"""

IGNORE_GENRE_WHERE = """
  WHERE movie.id NOT IN(
   SELECT movieid
   FROM moviexgenre
   WHERE genreid IN(%s)
  )
"""

ACTOR_WHERE = """
  WHERE movie.id IN(
   SELECT
    movieid
    FROM partxactor
      LEFT JOIN partxmovie
       ON partxmovie.partid = partxactor.partid
    WHERE actorid = %s
 )
"""

STUDIO_WHERE = """
  WHERE movie.id IN(
   SELECT movieid
   FROM moviexstudio
   WHERE studioid = %s)
"""

DIRECTOR_WHERE = """
 WHERE movie.id IN(
  SELECT movieid
  FROM moviexdirector
  WHERE directorid = %s)
"""

WRITER_WHERE = """
 WHERE movie.id IN(
  SELECT movieid
  FROM moviexwriter
  WHERE writerid = %s)
"""

SINGLE_MOVIE = """
  SELECT * FROM movie
  WHERE id = %s
  LIMIT 1
"""

MOVIE_LINKS = """
  SELECT * FROM moviexlinks
  WHERE movieid = %s
        AND linktype = 'movie'
  ORDER BY linksid
"""


ACTORS_LIST = """
  SELECT ActorID,
         IF(lastname="",
            displayname,
            CONCAT(lastname, ", ", actor.name)
           ) AS ActorName,
         DisplayName,
         actor.name AS firstname,
         lastname,
         COUNT( actorid ) AS MovieCount
  FROM partxactor
   LEFT JOIN actor
    ON actor.id = partxactor.actorid
   LEFT JOIN partxmovie
    ON partxmovie.partid = partxactor.partid
   LEFT JOIN movie
    ON movie.id = partxmovie.movieid
  WHERE IF(lastname="",
            displayname,
            CONCAT(lastname, ", ", actor.name)
           ) LIKE "%s%%"
  GROUP BY actorid
  ORDER BY ActorName
"""

ACTOR_LETTER_LIST = """
  SELECT LEFT(
    IF(lastname="",
       displayname,
       CONCAT(lastname,
              ", ",
              actor.name
             )
      ),
    1) AS letter,
   COUNT(displayname) as letter_count
  FROM partxactor
   LEFT JOIN actor
    ON actor.id = partxactor.actorid
   LEFT JOIN partxmovie
    ON partxmovie.partid = partxactor.partid
   LEFT JOIN movie
    ON movie.id = partxmovie.movieid
  GROUP BY letter
  ORDER BY letter
"""

YEAR_LIST = """
  SELECT MovieReleaseYear, DisplayName, COUNT( movie.id ) as MovieCount
  FROM movie
  LEFT JOIN YEAR ON year.id = moviereleaseyear
  GROUP BY moviereleaseyear
  ORDER BY displayname"""

GENRE_LIST = """
  SELECT GenreID, DisplayName, COUNT( movieid ) AS MovieCount
  FROM moviexgenre
   LEFT JOIN genre
    ON genre.id = moviexgenre.genreid
  GROUP BY moviexgenre.genreid
  ORDER BY displayname
"""

