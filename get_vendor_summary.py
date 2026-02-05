import pandas as pd
import logging
import sqlite3
import os
from sqlalchemy import create_engine
from ingestion_db import ingest_db

# make logs folder if it does not exist
if not os.path.exists("Logs"):
    os.makedirs("Logs")

# Create a custom logger
logger = logging.getLogger("get_vendor_summary")
logger.setLevel(logging.DEBUG)

# Prevent duplicate logs if handlers already exist
if not logger.handlers:
    # File handler
    fh = logging.FileHandler("Logs/get_vendor_summary.log", mode="a")
    fh.setLevel(logging.DEBUG)

    # Formatter
    formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
    fh.setFormatter(formatter)

    # Add handler to logger
    logger.addHandler(fh)

engine = create_engine("sqlite:///vendor_performance.db")

def create_vendor_summary(conn):
    ''''this function will merge the different tables to get the overall vendor summary and adding new columns in the resultant data'''
    logger.info("Running create_vendor_summary...")
    df = pd.read_sql_query("""WITH FreightSummary AS (
        SELECT
            VendorNumber, 
            SUM(Freight) as TotalFreightCost
        FROM vendor_invoice
        GROUP BY VendorNumber
    ),
    
    PurchaseSummary AS (
        SELECT
            p.VendorNumber,
            p.VendorName,
            p.Brand,
            p.Description,
            p.PurchasePrice,
            pp.Volume,
            pp.Price as ActualPrice,
            SUM(p.Quantity) as TotalPurchaseQuantity,
            SUM(p.Dollars) as TotalPurchaseDollars
        FROM purchases p
        JOIN purchase_prices pp
            ON p.Brand = pp.Brand
        WHERE p.PurchasePrice>0
        GROUP BY p.VendorNumber, p.VendorName, p.Brand, p.Description, p.PurchasePrice, pp.Price, pp.Volume
    ),
    
    SalesSummary AS (
        SELECT
            VendorNo,
            Brand,
            SUM(SalesDollars) as TotalSalesDollars,
            SUM(SalesPrice) as TotalSalesPrice,
            SUM(SalesQuantity) as TotalSalesQuantity,
            SUM(ExciseTax) as TotalExciseTax
        FROM sales
        GROUP BY VendorNo, Brand
    )
        
    SELECT
        ps.VendorNumber,
        ps.VendorName,
        ps.Brand,
        ps.Description,
        ps.PurchasePrice,
        ps.ActualPrice,
        ps.Volume,
        ps.TotalPurchaseQuantity,
        ps.TotalPurchaseDollars,
        ss.TotalSalesQuantity,
        ss.TotalSalesDollars,
        ss.TotalSalesPrice,
        ss.TotalExciseTax,
        fs.TotalFreightCost
    FROM PurchaseSummary ps
    LEFT JOIN SalesSummary ss
        ON ps.VendorNumber = ss.VendorNo
        AND ps.Brand = ss.Brand
    LEFT JOIN FreightSummary fs
        ON ps.VendorNumber = fs.VendorNumber
    ORDER BY ps.TotalPurchaseDollars DESC""", conn)

    return df

def clean_data(df):
    """this function will clean the data"""
    logger.info("Cleaning data...")
    #changing data type to float
    df['Volume'] = df['Volume'].astype('float64')
    
    #filling missing values with 0
    df.fillna(0, inplace = True)

    #removing spaces from categorical columns
    df['VendorName'] = df['VendorName'].str.strip()
    df['Description'] = df['Description'].str.strip()

    #creating new columns for better analysis
    df['GrossProfit'] = df['TotalSalesDollars'] - df['TotalPurchaseDollars']
    df['ProfitMargin'] = df['GrossProfit']/df['TotalSalesDollars']
    df['StockTurnover'] = df['TotalSalesQuantity']/df['TotalPurchaseQuantity']
    df['SalesToPurchaseRatio'] = df['TotalSalesDollars']/df['TotalPurchaseDollars']

    return(df)

if __name__ == '__main__':
    #creating  database connection 
    conn = sqlite3.connect('vendor_performance.db')

    logger.info('Creating Vendor Summary Table....')
    summary_df = create_vendor_summary(conn)
    logger.info(summary_df.head())

    logger.info('Cleaning Data....')
    clean_df = clean_data(summary_df)
    logger.info(clean_df.head())

    logger.info('Ingesting Data....')
    ingest_db(clean_df, 'vendor_sales_summary', engine)
    logger.info('Completed')

conn.close()