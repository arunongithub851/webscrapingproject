import sqlite3

def connect(dbname):
    conn=sqlite3.connect(dbname)

    conn.execute("CREATE TABLE IF NOT EXISTS FLPKRT_LAPTOPS (NAME TEXT,RATING TEXT,AMENITIES TEXT)")
    print("table created successfully!")

    conn.close()

def insert_in_to_table(dbname,values):
    conn=sqlite3.connect(dbname)
    print("Inserted into tables:"+str(values))
    insert_sql="INSERT INTO FLPKRT_LAPTOPS (NAME,RATING,AMENITIES) VALUES (?, ?, ?)"

    conn.execute(insert_sql,values)

    conn.commit()
    conn.close()

def get_laptop_info(dbname):
    conn=sqlite3.connect(dbname)
    cur=conn.cursor()

    cur.execute("SELECT * FROM FLPKRT_LAPTOPS")

    table_data=cur.fetchall()

    for record in table_data:
        print(record)

    conn.close()
