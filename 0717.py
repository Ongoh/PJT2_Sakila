import marimo

__generated_with = "0.14.11"
app = marimo.App(width="medium")


@app.cell
def _():
    import os
    import sqlalchemy

    _password = os.environ.get("MYSQL_PASSWORD", "lucky!!916")
    DATABASE_URL = f"mysql+pymysql://root:{_password}@127.0.0.1:3306/sakila"
    engine = sqlalchemy.create_engine(DATABASE_URL)
    return (engine,)


@app.cell
def _():
    import marimo as mo
    return (mo,)


@app.cell
def _(category, engine, film, film_category, inventory, mo, rental):
    year_pop_genre = mo.sql(
        f"""
        SELECT
            fcat.name AS genre_name,           
            YEAR(r.rental_date) AS rental_year, 
            COUNT(r.rental_id) AS rental_count  
        FROM rental AS r
        INNER JOIN inventory AS i USING (inventory_id)
        INNER JOIN film AS f USING (film_id)  
        INNER JOIN film_category AS fc USING (film_id)
        INNER JOIN category AS fcat USING (category_id)
        WHERE YEAR(r.rental_date) = 2005
        GROUP BY genre_name, rental_year 
        ORDER BY rental_year ASC, rental_count DESC LIMIT 100;
        """,
        engine=engine
    )
    return (year_pop_genre,)


@app.cell
def _(plt, year_pop_genre):
    plt.figure(figsize=(10, 6))
    plt.bar(year_pop_genre["genre_name"], year_pop_genre["rental_count"], color="skyblue")
    plt.xlabel("Genre")
    plt.ylabel("Rental Count")
    plt.title("2005 Rental Count by Genre")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()
    return


@app.cell
def _(year_pop_genre):
    import matplotlib.pyplot as plt
    import pandas as pd

    genre_names = year_pop_genre["genre_name"]
    rental_counts = year_pop_genre["rental_count"]

    genres_to_highlight = ["Sports", "Animation", "Action", "Sci-Fi", "Family"]

    colors = ["skyblue"] * len(genre_names)

    for i, genre in enumerate(genre_names):
        if genre in genres_to_highlight:
            colors[i] = "red"

    plt.figure(figsize=(10, 6))
    plt.bar(genre_names, rental_counts, color=colors)
    plt.xlabel("Genre")
    plt.ylabel("Rental Count")
    plt.title("2005 Rental Count by Genre")
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.show()
    return (plt,)


@app.cell
def _(category, engine, film, film_category, inventory, mo, rental):
    pop_ren = mo.sql(
        f"""
        SELECT
            f.film_id,
            f.title,
            COUNT(r.rental_id) AS rental_count
        FROM film AS f
        JOIN film_category AS fc ON f.film_id = fc.film_id
        JOIN category AS c ON fc.category_id = c.category_id
        JOIN inventory AS i ON f.film_id = i.film_id
        JOIN rental AS r ON i.inventory_id = r.inventory_id
        WHERE c.name = 'Sports'
          AND YEAR(r.rental_date) = 2005
        GROUP BY f.film_id, f.title
        ORDER BY rental_count DESC
        LIMIT 10;
        """,
        engine=engine
    )
    return (pop_ren,)


@app.cell
def _(pop_ren):
    pop_ren
    return


@app.cell
def _(engine, mo):
    _df = mo.sql(
        f"""
        -- 영화 길이 60분 미만
        SELECT title, `length` 
        FROM film
        WHERE length < 60
        ORDER BY length;
        """,
        engine=engine
    )
    return


@app.cell
def _(engine, film, inventory, mo, rental):
    _df = mo.sql(
        f"""
        -- 인기 많은 영화 10개
        SELECT f.title AS movie_title,
                COUNT(r.rental_id) AS total_rental_count
        FROM film AS f
        JOIN inventory AS i ON f.film_id = i.film_id
        JOIN rental AS r ON i.inventory_id = r.inventory_id
        GROUP BY f.film_id, f.title
        ORDER BY total_rental_count DESC
        LIMIT 15;
        """,
        engine=engine
    )
    return


@app.cell
def _(category, engine, film, film_category, inventory, mo, rental):
    _df = mo.sql(
        f"""
        WITH FilmRentalCounts AS (
            SELECT
                f.film_id,
                f.title AS movie_title,
                c.name AS genre_name,
                COUNT(r.rental_id) AS total_rental_count
            FROM
                film AS f
            JOIN
                film_category AS fc ON f.film_id = fc.film_id
            JOIN
                category AS c ON fc.category_id = c.category_id
            JOIN
                inventory AS i ON f.film_id = i.film_id
            JOIN
                rental AS r ON i.inventory_id = r.inventory_id
            WHERE
                c.name IN ('Sports', 'Animation', 'Action', 'Sci-Fi', 'Family')
            GROUP BY
                f.film_id, f.title, c.name
        ),
        RankedFilms AS (
            SELECT
                movie_title,
                genre_name,
                total_rental_count,
                ROW_NUMBER() OVER (PARTITION BY genre_name ORDER BY total_rental_count DESC) AS rnk
            FROM
                FilmRentalCounts
        )
        SELECT
            genre_name,
            movie_title,
            total_rental_count
        FROM
            RankedFilms
        WHERE
            rnk <= 2
        ORDER BY
            genre_name, total_rental_count DESC;
        """,
        engine=engine
    )
    return


@app.cell
def _(engine, film, inventory, mo, rental):
    _df = mo.sql(
        f"""
        SELECT
            f.title AS movie_title,
            f.length AS movie_length_minutes, -- 영화 길이를 함께 출력하여 확인
            COUNT(r.rental_id) AS total_rental_count
        FROM
            film AS f
        JOIN
            inventory AS i ON f.film_id = i.film_id
        JOIN
            rental AS r ON i.inventory_id = r.inventory_id
        WHERE
            f.length < 60 -- 영화 길이가 60분 미만인 영화만 선택
        GROUP BY
            f.film_id, f.title, f.length
        ORDER BY
            total_rental_count DESC
        LIMIT 10;
        """,
        engine=engine
    )
    return


if __name__ == "__main__":
    app.run()
