import sqlite3
import pandas as pd
import json

# with sqlite3.connect("Movie_detail.db")as conn:
#     cursor=conn.cursor()
#     query="""create table Movie 
#             ( id int Not Null, Title varchar(250)); """
#     cursor.execute(query)
#     print("work Done")
#     conn.commit()
#     
# with sqlite3.connect("Movie_detail.db")as conn:
#     cursor=conn.cursor()
#     query='''CREATE TABLE IF NOT EXISTS Movie (
#             ID varchar(150) PRIMARY KEY,
#             Title varchar(250),
#             Year varchar(250),
#             Poster varchar(500),
#             Genre varchar(800),
#             Director varchar(200),
#             Rating float,
#             Awards varchar(500),
#             Budget int,
#             Revenue int); '''
#     data=pd.read_sql_query(query,conn)
#     print(data) 
#     conn.commit()
    
# with sqlite3.connect("Movie_detail.db") as conn:
#     cursor = conn.cursor()
#     cursor.execute("ALTER TABLE Movie ADD COLUMN popularity float ")
#     print('success')
#     conn.commit()

# 
# with sqlite3.connect("Movie_detail.db") as conn:
#     re=pd.read_sql_query("select * from Movie",conn)
#     print(re.columns)


def Insert_value(ID, Title, Year, Poster, Genre, Director, Rating, Awards, Budget, Revenue,Popularity):
    with sqlite3.connect("Movie_detail.db") as conn:
        cursor = conn.cursor()

        # Serialize genre if it's a list
        if isinstance(Genre, list):
            Genre = json.dumps(Genre)

        # Check if movie already exists
        cursor.execute("SELECT 1 FROM Movie WHERE ID = ?", (ID,))
        exists = cursor.fetchone()

        if not exists:
            query = '''
                INSERT INTO Movie 
                (ID, Title, Year, Poster, Genre, Director, Rating, Awards, Budget, Revenue,popularity )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?,?)
            '''
            cursor.execute(query, (
                ID, Title, Year, Poster, Genre, Director, Rating, Awards, Budget, Revenue,Popularity
            ))
        else:
            query = '''
                UPDATE Movie SET 
                    Title = ?, Year = ?, Poster = ?, Genre = ?, Director = ?, 
                    Rating = ?, Awards = ?, Budget = ?, Revenue = ?, popularity=?
                WHERE ID = ?
            '''
            cursor.execute(query, (
                Title, Year, Poster, Genre, Director,
                Rating, Awards, Budget, Revenue,Popularity, ID
            ))

        conn.commit()



def update_score(id, sentiment):
    with sqlite3.connect("Movie_detail.db") as conn:
        cursor = conn.cursor()

        # Check if movie_id already exists in Score
        cursor.execute("SELECT * FROM Score WHERE id = ?", (id,))
        record = cursor.fetchone()

        if record is None:
            # Insert new row
            if sentiment == 'positive':
                cursor.execute(
                    "INSERT INTO Score (id, Positive_score, Negative_score, Total_comment) VALUES (?, 1, 0, 1)",
                    (id,))
            else:
                cursor.execute(
                    "INSERT INTO Score (id, Positive_score, Negative_score, Total_comment) VALUES (?, 0, 1, 1)",
                    (id,))
        else:
            # Update existing record
            if sentiment == 'positive':
                cursor.execute("""
                    UPDATE Score
                    SET Positive_score = Positive_score + 1,
                        Total_comment = Total_comment + 1
                    WHERE id = ?
                """, (id,))
            else:
                cursor.execute("""
                    UPDATE Score
                    SET Negative_score = Negative_score + 1,
                        Total_comment = Total_comment + 1
                    WHERE id = ?
                """, (id,))

        conn.commit()

    
    
