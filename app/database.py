import sqlite3
from .schemas import ShipmentCreate, ShipmentUpdate
from typing import Any, Optional
from contextlib import contextmanager

class Database:
    def connect_to_db(self):
        #make the conn
        self.conn = sqlite3.connect("app/sqlite.db", check_same_thread = False)
        self.cur = self.conn.cursor()
        print("-"*5, "connected to DB", "-"*5)

    def create_table(self):
        #1. create a table.
        self.cur.execute("CREATE TABLE IF NOT EXISTS shipment (id INTEGER PRIMARY KEY, content TEXT, weight REAL, destination INTEGER, status TEXT, estimated_delivery TEXT)")
    
    def create(self, shipment: ShipmentCreate) -> int:
        self.cur.execute("SELECT MAX(id) from shipment")
        result = self.cur.fetchone()

        new_id = result[0] + 1

        # 2. INSERT SHIPMENT DATA.
        shipment_data = shipment.model_dump()
        self.cur.execute(""" 
            INSERT INTO shipment VALUES (:id, :content, :weight, :destination, :status, :estimated_delivery)
        """, {
            "id": new_id, 
            "content": shipment_data["content"],
            "weight": shipment_data["weight"],
            "destination": shipment_data.get("destination"),
            "status": "placed",
            "estimated_delivery": None,
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
            "destination" : row[3],
            "status" : row[4],
            "estimated_delivery" : row[5]
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
                "destination": row[3],
                "status": row[4],
                "estimated_delivery": row[5]
            } for row in data
        ]

    def update(self, id, shipment: ShipmentUpdate) -> Optional[dict[str, Any]]:
        # Build dynamic update query for non-None fields
        update_data = shipment.model_dump(exclude_none=True)
        if not update_data:
            return self.get_by_id(id)
        
        set_clause = ", ".join([f"{key} = :{key}" for key in update_data.keys()])
        query = f"UPDATE shipment SET {set_clause} WHERE id = :id"
        
        self.cur.execute(query, {
            "id": id,
            **update_data
        })
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
        print("connection closed....")
        self.conn.close()
    
    # def __enter__(self):
    #     print("Entering the context")
    #     self.connect_to_db()
    #     self.create_table()
    #     return self
    
    # def __exit__(self, *args):
    #     print("exiting the context")
    #     self.close()

# Usage
@contextmanager
def managed_db():
    db = Database()
    #setup
    print("entering the context")
    db.connect_to_db()
    db.create_table()

    yield db

    #Dispose
    print("exiting the context")
    db.close()
