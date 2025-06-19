"""
Parquet data handler for storing and retrieving date-price data
"""

import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq
from typing import List, Tuple, Optional, Union, Sequence
from datetime import datetime, date
import os
from pathlib import Path


class ParquetDao:
    """
    A class to handle reading and writing date-price data to Parquet files.
    
    Supports:
    - Inserting date-price pairs
    - Reading data within date ranges
    - Automatic file creation and management
    """
    
    def __init__(self, file_path: str):
        """
        Initialize the ParquetDataHandler.
        
        Args:
            file_path (str): Path to the Parquet file
        """
        self.file_path = Path(file_path)
        self.file_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Define the schema for date-price data
        self.schema = pa.schema([
            ('date', pa.date32()),
            ('price', pa.float64())
        ])
        
        # Initialize empty DataFrame if file doesn't exist
        if not self.file_path.exists():
            self._create_empty_file()
    
    def _create_empty_file(self) -> None:
        """Create an empty Parquet file with the correct schema."""
        empty_df = pd.DataFrame({
            'date': pd.Series(dtype='datetime64[ns]'),
            'price': pd.Series(dtype='float64')
        })
        empty_df.to_parquet(self.file_path, index=False)
    
    def insert_data(self, data: List[Tuple[Union[date, datetime, str], float]]) -> None:
        """
        Insert a list of date-price pairs into the Parquet file.
        
        Args:
            data (List[Tuple]): List of (date, price) tuples. 
                               Date can be date, datetime, or string.
        """
        # Convert data to DataFrame
        dates, prices = zip(*data) if data else ([], [])
        df_new = pd.DataFrame({
            'date': dates,
            'price': prices
        })
        
        # Convert date column to datetime
        df_new['date'] = pd.to_datetime(df_new['date']).dt.date
        
        # Read existing data if file exists and has data
        if self.file_path.exists() and os.path.getsize(self.file_path) > 0:
            try:
                df_existing = pd.read_parquet(self.file_path)
                df_existing['date'] = pd.to_datetime(df_existing['date']).dt.date
                
                # Combine existing and new data
                df_combined = pd.concat([df_existing, df_new], ignore_index=True)
                
                # Remove duplicates based on date (keep the latest price for each date)
                df_combined = df_combined.drop_duplicates(subset=['date'], keep='last')
                
                # Sort by date
                df_combined = df_combined.sort_values('date')
                
            except Exception as e:
                print(f"Error reading existing file: {e}")
                df_combined = df_new
        else:
            df_combined = df_new
        
        # Save to Parquet file
        df_combined.to_parquet(self.file_path, index=False)
        print(f"Successfully inserted {len(data)} records. Total records: {len(df_combined)}")
    
    def read_date_range(self, start_date: Union[date, datetime, str], 
                       end_date: Union[date, datetime, str]) -> pd.DataFrame:
        """
        Read data within a specified date range.
        
        Args:
            start_date: Start date (inclusive)
            end_date: End date (inclusive)
            
        Returns:
            pd.DataFrame: DataFrame containing date and price columns
        """
        if not self.file_path.exists():
            print("File does not exist. Returning empty DataFrame.")
            return pd.DataFrame({
                'date': pd.Series(dtype='datetime64[ns]'),
                'price': pd.Series(dtype='float64')
            })
        
        try:
            # Read the Parquet file
            df = pd.read_parquet(self.file_path)
            
            # Convert date column to datetime for comparison
            df['date'] = pd.to_datetime(df['date'])
            
            # Convert input dates to datetime
            start_dt = pd.to_datetime(start_date)
            end_dt = pd.to_datetime(end_date)
            
            # Filter by date range
            mask = (df['date'] >= start_dt) & (df['date'] <= end_dt)
            filtered_df = df.loc[mask].copy()
            
            # Convert date back to date type for consistency
            filtered_df['date'] = filtered_df['date'].dt.date
            
            return filtered_df
            
        except Exception as e:
            print(f"Error reading data: {e}")
            return pd.DataFrame({
                'date': pd.Series(dtype='datetime64[ns]'),
                'price': pd.Series(dtype='float64')
            })
    
    def read_all_data(self) -> pd.DataFrame:
        """
        Read all data from the Parquet file.
        
        Returns:
            pd.DataFrame: DataFrame containing all date and price data
        """
        if not self.file_path.exists():
            print("File does not exist. Returning empty DataFrame.")
            return pd.DataFrame({
                'date': pd.Series(dtype='datetime64[ns]'),
                'price': pd.Series(dtype='float64')
            })
        
        try:
            df = pd.read_parquet(self.file_path)
            df['date'] = pd.to_datetime(df['date']).dt.date
            return df
        except Exception as e:
            print(f"Error reading data: {e}")
            return pd.DataFrame({
                'date': pd.Series(dtype='datetime64[ns]'),
                'price': pd.Series(dtype='float64')
            })
    
    def get_latest_price(self) -> Optional[float]:
        """
        Get the most recent price from the data.
        
        Returns:
            float or None: The latest price, or None if no data exists
        """
        df = self.read_all_data()
        if df.empty:
            return None
        
        return df.iloc[-1]['price']
    
    def get_price_on_date(self, target_date: Union[date, datetime, str]) -> Optional[float]:
        """
        Get the price for a specific date.
        
        Args:
            target_date: The date to get the price for
            
        Returns:
            float or None: The price for the specified date, or None if not found
        """
        df = self.read_all_data()
        if df.empty:
            return None
        
        target_dt = pd.to_datetime(target_date).date()
        matching_rows = df[df['date'] == target_dt]
        
        if matching_rows.empty:
            return None
        
        return matching_rows.iloc[0]['price']
    
    def get_data_info(self) -> dict:
        """
        Get information about the stored data.
        
        Returns:
            dict: Information about the data including count, date range, etc.
        """
        df = self.read_all_data()
        
        if df.empty:
            return {
                'total_records': 0,
                'date_range': None,
                'price_range': None,
                'file_size_mb': 0
            }
        
        file_size_mb = os.path.getsize(self.file_path) / (1024 * 1024) if self.file_path.exists() else 0
        
        return {
            'total_records': len(df),
            'date_range': {
                'start': df['date'].min().isoformat(),
                'end': df['date'].max().isoformat()
            },
            'price_range': {
                'min': float(df['price'].min()),
                'max': float(df['price'].max()),
                'mean': float(df['price'].mean())
            },
            'file_size_mb': round(file_size_mb, 2)
        } 