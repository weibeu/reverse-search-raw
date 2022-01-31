from . import conn


def make_migrations():
    cur = conn.cursor()
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS title_akas (
           titleId TEXT,
           ordering INTEGER,
           title TEXT,
           region TEXT,
           language TEXT,
           types TEXT,
           attributes TEXT,
           isOriginalTitle INTEGER
        )
        """
    )
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS title_basics (
            tconst TEXT,
            titleType TEXT,
            primaryTitle TEXT,
            originalTitle TEXT,
            isAdult INTEGER ,
            startYear INTEGER,
            endYear INTEGER,
            runtimeMinutes INTEGER,
            genres TEXT
        )
        """
    )
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS title_crew (
            tconst TEXT,
            directors TEXT,
            writers TEXT
        )
        """
    )
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS episode (
            tconst TEXT,
            parentTconst TEXT,
            seasonNumber INTEGER,
            episodeNumber INTEGER
        )
        """
    )
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS principals (
            tconst TEXT,
            ordering INTEGER,
            nconst TEXT,
            category TEXT,
            job TEXT,
            characters TEXT
        )
        """
    )
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS ratings (
            tconst TEXT,
            averageRating FLOAT,
            numVotes INTEGER
        )
        """
    )
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS name_basics (
            nconst TEXT,
            primaryName TEXT,
            birthYear INTEGER,
            deathYear INTEGER,
            primaryProfession TEXT,
            knownForTitles TEXT
        )
        """
    )
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS title_subtitles (
            titleId TEXT,
            index_ INTEGER,
            start_ TEXT,
            end_ TEXT,
            dialogue TEXT
        )
        """
    )

    cur.execute("CREATE INDEX ON title_akas (titleId)")
    cur.execute("CREATE INDEX ON title_basics (tconst)")
    cur.execute("CREATE INDEX ON title_crew (tconst)")
    cur.execute("CREATE INDEX ON episode (tconst, parentTconst)")
    cur.execute("CREATE INDEX ON principals (tconst, ordering, nconst)")
    cur.execute("CREATE INDEX ON ratings (tconst)")
    cur.execute("CREATE INDEX ON name_basics (nconst)")
    cur.execute("CREATE INDEX ON title_subtitles (titleId, index_)")

    conn.commit()
    cur.close()
