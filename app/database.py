import sqlite3
from .schemas import ShipmentCreate, ShipmentUpdate
from typing import Any, Optional

class Database:
    def __init__(self):
        #make the conn
        self.conn = sqlite3.connect("app/sqlite.db", check_same_thread = False)
        self.cur = self.conn.cursor()
        print("-"*5, "connected to DB", "-"*5)

        #create database if not exist
        self.create_table()


    def create_table(self):
        #1. create a table.
        self.cur.execute("CREATE TABLE IF NOT EXISTS shipment (id INTEGER PRIMARY KEY, content TEXT, weight REAL, status TEXT)")
    
    def create(self, shipment: ShipmentCreate) -> int:
        self.cur.execute("SELECT MAX(id) from shipment")
        result = self.cur.fetchone()

        new_id = result[0] + 1

        # 2. INSERT SHIPMENT DATA.
        self.cur.execute(""" 
            INSERT INTO shipment VALUES (:id, :content, :weight, :status)
        """, {
            "id": new_id, 
            **shipment.model_dump(),
            "status": "placed",
        })
        self.conn.commit()

        return new_id
    
    def get_by_id(self, id: int) -> Optional[dict[str, Any]]:
        #3. FETCH Shipment data by id.
        self.cur.execute("""
            SELECT * FROM shipment where id = ?
        """, (id, )
        )
        row = self.cur.fetchone()
        
        return {
            "id" : row[0],
            "content" : row[1],
            "weight" : row[2],
            "status" : row[3]
        } if row else None
    
    def get_all(self) -> Optional[list]:
        self.cur.execute(
            """ SELECT * FROM shipment """
        )

        data = self.cur.fetchall()
        
        return [
            {
                "id": row[0],
                "content": row[1],
                "weight": row[2],
                "status": row[3]
            } for row in data
        ]

    def update(self, id, shipment: ShipmentUpdate) -> Optional[dict[str, Any]]:
        self.cur.execute( # method 1 for passing parameter.
            """ UPDATE shipment set status = :status where id= :id """, {
                "id": id,
                **shipment.model_dump()
            }
        )
        self.conn.commit()

        return self.get_by_id(id)

    def delete(self, id: int):
        # #4. DELETE a shipment.
        self.cur.execute(""" 
            DELETE FROM shipment where id = ?
        """, (id, ))
        self.conn.commit()

    def close(self):
        #close the conn
        self.conn.close()
