-- Active: 1752195989840@@127.0.0.1@3306@sakila
USE sakila;

SHOW TABLES;

DESC film_actor;
-- 배우별 영화
SELECT CONCAT(a.first_name, ' ', a.last_name) AS 이름, f.title AS 영화제목
FROM actor AS a
INNER JOIN film_actor AS fa USING (actor_id)
INNER JOIN film AS f USING (film_id)
ORDER BY a.first_name
limit 100;


-- 특정 배우 영화
SELECT CONCAT(a.first_name, ' ', a.last_name) AS 이름, f.title AS 영화제목, f.description AS 설명
FROM actor AS a
INNER JOIN film_actor AS fa USING (actor_id)
INNER JOIN film AS f USING (film_id)
WHERE CONCAT(a.first_name, ' ', a.last_name) = 'MATTHEW CARREY'
limit 100;


-- 배우별 영화갯수
SELECT CONCAT(a.first_name, ' ', a.last_name) AS 이름, COUNT(f.title) AS 영화갯수
FROM actor AS a
INNER JOIN film_actor AS fa USING (actor_id)
INNER JOIN film AS f USING (film_id)
GROUP BY a.first_name, a.last_name, actor_id
ORDER BY 영화갯수 DESC;

-- 언제 주로 빌렸는지
SELECT f.title AS 영화제목, YEAR(r.rental_date) AS 빌린연도, COUNT(*) AS 빌린횟수
FROM rental AS r
INNER JOIN inventory AS i USING (inventory_id)
INNER JOIN film AS f USING (film_id)
GROUP BY 빌린연도, f.title
ORDER BY 빌린횟수 DESC, 빌린연도 DESC, 영화제목 DESC;


-- 어떤 영화들이 있는지
SELECT title AS 영화제목
FROM film
ORDER BY 영화제목;


-- 언어별 영화갯수
SELECT
    l.name AS 언어,
    COUNT(f.film_id) AS 영화개수
FROM
    language AS l
INNER JOIN
    film AS f ON l.language_id = f.language_id 
GROUP BY
    l.name
ORDER BY
    영화개수 DESC, 언어 ASC;


-- 영화별 개봉시기 뭐야 죄다 2006년이잖아
SELECT release_year AS 개봉시기, COUNT(film_id) AS 개수
FROM film
GROUP BY 개봉시기
ORDER BY 개봉시기;

-- 영화 길이 60분 미만
SELECT title, `length` 
FROM film
WHERE length < 60
ORDER BY length;


-- 연도별 인기 많았던 영화 장르
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
ORDER BY rental_year ASC, rental_count DESC;


-- 2005년 sports 장르 영화 10개 뽑기
SELECT
    f.film_id,
    f.title,
    f.release_year,
    COUNT(r.rental_id) AS rental_count
FROM film AS f
JOIN film_category AS fc ON f.film_id = fc.film_id
JOIN category AS c ON fc.category_id = c.category_id
JOIN inventory AS i ON f.film_id = i.film_id
JOIN rental AS r ON i.inventory_id = r.inventory_id
WHERE c.name = 'Sports'
  AND YEAR(r.rental_date) = 2005
GROUP BY f.film_id, f.title, f.release_year
ORDER BY rental_count DESC
LIMIT 10;


-- 인기 많은 영화 10개
SELECT f.title AS movie_title,
        COUNT(r.rental_id) AS total_rental_count
FROM film AS f
JOIN inventory AS i ON f.film_id = i.film_id
JOIN rental AS r ON i.inventory_id = r.inventory_id
GROUP BY f.film_id, f.title
ORDER BY total_rental_count DESC
LIMIT 15;