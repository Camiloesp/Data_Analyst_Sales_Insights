from sqlalchemy import create_engine, Column, Integer, String, DateTime, Float, Table, MetaData, select, func, desc
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker # ORM = Object relation map to map from classes to table

import os
import pandas as pd
from datetime import datetime
from collections import defaultdict

# Table Class ====================================================
Base = declarative_base()
class Order(Base):
    __tablename__ = "orders"
    #Row ID,Order ID,Order Date,Ship Date,Ship Mode,Customer ID,Customer Name,Segment,Country,City,State,Postal Code,Region,Product ID,Category,Sub-Category,Product Name,Sales,Quantity,Discount,Profit
    row_id = Column("Row ID", Integer, primary_key=True)
    order_id = Column("Order ID", String)
    order_date = Column("Order Date", DateTime)
    ship_date = Column("Ship Date", DateTime)
    ship_mode = Column("Ship Mode", String)
    customer_id = Column("Customer ID", String)
    customer_name = Column("Customer Name", String)
    segment = Column("Segment", String)
    country = Column("Country", String)
    city = Column("City", String)
    state = Column("State", String)
    postal_code = Column("Postal Code", String)  # Postal codes may start with zero
    region = Column("Region", String)
    product_id = Column("Product ID", String)
    category = Column("Category", String)
    sub_category = Column("Sub-Category", String)
    product_name = Column("Product Name", String)
    sales = Column("Sales", Float)
    quantity = Column("Quantity", Integer)
    discount = Column("Discount", Float)
    profit = Column("Profit", Float)

# Functional Class ====================================================
class SalesDB:
    
    def __init__(self, csv_path, table_name): # db_path is .csv file
        # Create .db file name. Should be the same as the .csv
        db_file_name = os.path.splitext(csv_path)[0] + ".db"
        print(f"db_file_name: {db_file_name}     csv_path {csv_path}")
        
        # Create Engine
        self.engine = create_engine(f'sqlite:///{db_file_name}', echo=True)  # engine = db.create_engine('dialect+driver://user:pass@host:port/db')
        
        if os.path.exists(db_file_name):
            print(f'Database {db_file_name} already exists. Skipping CSV load')
        else:
            # db file not found! Create a new one
            # Read CSV
            df = pd.read_csv(csv_path, encoding='ISO-8859-1')  # or try 'cp1252'
            
            # Write to database
            df.to_sql(table_name, self.engine, index=False)
            print(f'Database created at {db_file_name} and table {table_name} loaded. DB will be saved to: {os.path.abspath(db_file_name)}')
        
    
    def get_top_popular_products(self, top_amount):
        metadata = MetaData()
        orders = Table("orders", metadata, autoload_with=self.engine)

        stmt = (
            select(orders.c["Product Name"], func.sum(orders.c.Quantity).label("total_quantity"))
            .group_by(orders.c["Product Name"])
            .order_by(desc("total_quantity"))
            .limit(top_amount)
        )

        with self.engine.connect() as conn:
            result = conn.execute(stmt).fetchall()

        return result
    
    def get_top_spenders(self, top_amount):
        metadata = MetaData()
        orders = Table("orders", metadata, autoload_with=self.engine)
        
        stmt = (
            select(orders.c["Customer ID"], func.sum(orders.c.Sales * orders.c.Quantity).label("total_spent"))
            .group_by(orders.c["Customer ID"])
            .order_by(desc("total_spent"))
            .limit(top_amount)
        )
        
        with self.engine.connect() as conn:
            result = conn.execute(stmt).fetchall()
        return result
    
    def get_monthly_sells(self):
        metadata = MetaData()
        orders = Table("orders", metadata, autoload_with=self.engine)

        stmt = select(orders.c["Order Date"], orders.c.Sales)

        with self.engine.connect() as conn:
            rows = conn.execute(stmt).mappings().fetchall()

        monthly_totals = defaultdict(float)

        for row in rows:
            # parse 'M/D/YYYY' string to date
            dt = datetime.strptime(row["Order Date"], "%m/%d/%Y")
            key = f"{dt.month}/{dt.year}"
            monthly_totals[key] += row["Sales"]

        # Sort keys by year, then month
        sorted_totals = sorted(
            monthly_totals.items(),
            key=lambda x: (int(x[0].split('/')[1]), int(x[0].split('/')[0]))
        )

        result = [{"order_date": k, "total_sales": round(v, 2)} for k, v in sorted_totals]
        return result


    # CRUD operations. ?