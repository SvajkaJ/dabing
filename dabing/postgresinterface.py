#!/usr/bin/python3
# Autor: SvajkaJ
# Date:  21.2.2022

# PostgreSQL adapter for python
import psycopg2  # type: ignore


class PostgresInterface:
    def __init__(self):
        # Connect to your postgres DB
        self.conn = psycopg2.connect(
            dbname = "dabing",
            user = "pi"
        )

        # Open a cursor to perform database operations
        self.cur = self.conn.cursor()

    def __del__(self):
        # Close communication with the database
        self.cur.close()
        self.conn.close()

    def execureQuery(self, query):
        # Execute a query
        self.cur.execute(query)

        # Retrieve query results
        records = self.cur.fetchall()

        # Make the changes to the database persistent
        self.conn.commit()

        return records


if __name__ == "__main__":
    db = PostgresInterface()

    records = db.execureQuery("SELECT * FROM dabing")

    print(records)
