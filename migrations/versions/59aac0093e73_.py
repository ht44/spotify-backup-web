"""empty message

Revision ID: 59aac0093e73
Revises: 412dc368a477
Create Date: 2018-05-28 22:25:56.673185

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
from sqlalchemy.sql import text

revision = '59aac0093e73'
down_revision = '412dc368a477'
branch_labels = None
depends_on = None


def upgrade():
    conn = op.get_bind()
    conn.execute(
        text(
            """
                CREATE OR REPLACE FUNCTION get_artist(_artist_id int)
                RETURNS SETOF artist AS $$
                BEGIN
                  RETURN QUERY SELECT
                    artist.id,
                    artist.name
                  FROM
                    artist
                  WHERE
                    artist.id = _artist_id;
                END;
                $$ LANGUAGE plpgsql;
                
                
                CREATE OR REPLACE FUNCTION get_album(_album_id int)
                RETURNS SETOF album AS $$
                BEGIN
                  RETURN QUERY SELECT
                    album.id,
                    album.name,
                    album.artist_id
                  FROM
                    album
                  WHERE
                    album.id = _album_id;
                END;
                $$ LANGUAGE plpgsql;
                
                
                
                CREATE OR REPLACE FUNCTION get_song(_song_id int)
                RETURNS SETOF song AS $$
                BEGIN
                  RETURN QUERY SELECT
                    song.id,
                    song.name,
                    song.album_id
                  FROM
                    song
                  WHERE
                    song.id = _song_id;
                END;
                $$ LANGUAGE plpgsql;
                
                
                CREATE OR REPLACE FUNCTION get_artists()
                RETURNS SETOF artist AS $$
                BEGIN
                  RETURN QUERY SELECT
                    artist.id,
                    artist.name
                  FROM
                    artist
                  ORDER BY name ASC;
                END;
                $$ LANGUAGE plpgsql;
                
                
                CREATE OR REPLACE FUNCTION get_albums()
                RETURNS SETOF album AS $$
                BEGIN
                  RETURN QUERY SELECT
                    album.id,
                    album.name,
                    album.artist_id
                  FROM
                    album
                  ORDER BY name ASC;
                END;
                $$ LANGUAGE plpgsql;
                
                
                CREATE OR REPLACE FUNCTION get_songs()
                RETURNS SETOF song AS $$
                BEGIN
                  RETURN QUERY SELECT
                    song.id,
                    song.name,
                    song.album_id
                  FROM
                    song
                  ORDER BY name ASC;
                END;
                $$ LANGUAGE plpgsql;
                
                
                CREATE OR REPLACE FUNCTION search_songs(
                  _name VARCHAR(150) DEFAULT NULL
                )
                RETURNS SETOF song AS $$
                BEGIN
                  RETURN QUERY SELECT
                    song.id,
                    song.name,
                    song.album_id
                  FROM
                    song
                  WHERE
                    (_name IS NULL OR song.name LIKE _name || '%')
                  ORDER BY
                    song.name ASC;
                END
                $$ LANGUAGE plpgsql;
                
                
                CREATE OR REPLACE FUNCTION search_albums(
                  _name VARCHAR(150) DEFAULT NULL
                )
                RETURNS SETOF album AS $$
                BEGIN
                  RETURN QUERY SELECT
                    album.id,
                    album.name,
                    album.artist_id
                  FROM
                    album
                  WHERE
                    (_name IS NULL OR album.name LIKE _name || '%')
                  ORDER BY
                    album.name ASC;
                END
                $$ LANGUAGE plpgsql;
                
                
                CREATE OR REPLACE FUNCTION search_artists(
                  _name VARCHAR(150) DEFAULT NULL
                )
                RETURNS SETOF artist AS $$
                BEGIN
                  RETURN QUERY SELECT
                    *
                  FROM
                    artist
                  WHERE
                    (_name IS NULL OR artist.name LIKE _name || '%')
                  ORDER BY
                    artist.name ASC;
                END
                $$ LANGUAGE plpgsql;
                
                
                
                CREATE OR REPLACE FUNCTION get_artist_albums(_artist_id int)
                RETURNS SETOF album AS $$
                BEGIN
                  RETURN QUERY SELECT
                    album.id,
                    album.name,
                    album.artist_id
                  FROM
                    album
                  WHERE
                    album.artist_id = _artist_id
                  ORDER BY album.name ASC;
                end;
                $$ LANGUAGE plpgsql;
                
                
                CREATE OR REPLACE FUNCTION get_artist_songs(_artist_id int)
                RETURNS SETOF song AS $$
                BEGIN
                  RETURN QUERY SELECT
                    song.id,
                    song.name,
                    song.album_id
                  FROM
                    album INNER JOIN song on song.album_id = album.id
                  WHERE
                    album.artist_id = _artist_id
                  ORDER BY album ASC, song ASC;
                END;
                $$ LANGUAGE plpgsql;
                
                
                CREATE OR REPLACE FUNCTION get_artist_discography(_artist_id int)
                RETURNS TABLE(
                  song_id INT,
                  song_name VARCHAR(150),
                  album_id INT,
                  album_name VARCHAR(150)
                  ) AS $$
                BEGIN
                  RETURN QUERY SELECT
                    song.id as song_id,
                    song.name as song_name,
                    album.id as album_id,
                    album.name as album_name
                  FROM
                    album INNER JOIN song on song.album_id = album.id
                  WHERE
                    album.artist_id = _artist_id
                  ORDER BY album_name ASC, song_name ASC;
                END;
                $$ LANGUAGE plpgsql;
                
                
                CREATE OR REPLACE FUNCTION get_album_songs(_album_id int)
                RETURNS SETOF song AS $$
                BEGIN
                  RETURN QUERY SELECT
                    song.id,
                    song.name,
                    song.album_id
                  FROM
                    song
                  WHERE
                    song.album_id = _album_id
                  ORDER BY song.name ASC;
                END;
                $$ LANGUAGE plpgsql;
                
                
                CREATE OR REPLACE FUNCTION get_library()
                RETURNS TABLE(
                    song_id INT,
                    song_name VARCHAR(150),
                    album_id INT,
                    album_name VARCHAR(150),
                    artist_id INT,
                    artist_name VARCHAR(150)
                ) AS $$
                BEGIN
                  RETURN QUERY SELECT
                    song.id as song_id,
                    song.name as song_name,
                    album.id as album_id,
                    album.name as album_name,
                    artist.id as artist_id,
                    artist.name as artist_name
                  FROM
                    song
                  INNER JOIN
                    album ON song.album_id = album.id
                  INNER JOIN
                    artist ON album.artist_id = artist.id
                  ORDER BY artist_name ASC, album_name ASC, song_name ASC;
                END
                $$ LANGUAGE plpgsql;
                
                
                CREATE OR REPLACE FUNCTION search_library(
                  _song VARCHAR(150) DEFAULT NULL,
                  _album VARCHAR(150) DEFAULT NULL,
                  _artist VARCHAR(150) DEFAULT NULL
                )
                RETURNS TABLE(
                    song_id INT,
                    song_name VARCHAR(150),
                    album_id INT,
                    album_name VARCHAR(150),
                    artist_id INT,
                    artist_name VARCHAR(150)
                ) AS $$
                BEGIN
                  RETURN QUERY SELECT
                    song.id as song_id,
                    song.name as song_name,
                    album.id as album_id,
                    album.name as album_name,
                    artist.id as artist_id,
                    artist.name as artist_name
                  FROM
                    song
                  INNER JOIN
                    album ON song.album_id = album.id
                  INNER JOIN
                    artist ON album.artist_id = artist.id
                  WHERE
                    (_song IS NULL OR song.name ILIKE _song || '%')
                  AND
                    (_album IS NULL OR album.name ILIKE _album || '%')
                  AND
                    (_artist IS NULL OR artist.name ILIKE _artist || '%')
                  ORDER BY artist_name ASC, album_name ASC, song_name ASC;
                END
                $$ LANGUAGE plpgsql;
            """
        ))
    pass


def downgrade():
    conn = op.get_bind()
    conn.execute(
        text(
            """
                DROP FUNCTION get_library();
                DROP FUNCTION search_library(CHARACTER VARYING, CHARACTER VARYING, CHARACTER VARYING);
                DROP FUNCTION search_songs(CHARACTER VARYING);
                DROP FUNCTION search_artists(CHARACTER VARYING);
                DROP FUNCTION search_albums(CHARACTER VARYING);
                DROP FUNCTION get_artists();
                DROP FUNCTION get_albums();
                DROP FUNCTION get_songs();
                DROP FUNCTION get_artist(INTEGER);
                DROP FUNCTION get_song(INTEGER);
                DROP FUNCTION get_album(INTEGER);
                DROP FUNCTION get_artist_songs(INTEGER);
                DROP FUNCTION get_artist_albums(INTEGER);
                DROP FUNCTION get_album_songs(INTEGER);
                DROP FUNCTION get_artist_discography(INTEGER);
            """
        )
    )
    pass
