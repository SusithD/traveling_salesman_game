"""
Database manager for the Traveling Salesman Problem game
"""
import sqlite3
import os
import json
from datetime import datetime

class DatabaseManager:
    def __init__(self, db_file="tsp_game.db"):
        """Initialize the database manager"""
        # Check if the database directory exists
        db_dir = os.path.dirname(db_file)
        if db_dir and not os.path.exists(db_dir):
            os.makedirs(db_dir)
        
        self.db_file = db_file
        self.initialize_db()
    
    def initialize_db(self):
        """Initialize the database schema"""
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()
        
        # Create game_results table if it doesn't exist
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS game_results (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            player_name TEXT NOT NULL,
            home_city TEXT NOT NULL,
            cities_visited INTEGER NOT NULL,
            route TEXT NOT NULL,
            route_length REAL NOT NULL,
            algorithm TEXT NOT NULL,
            execution_time REAL NOT NULL,
            timestamp TEXT NOT NULL
        )
        ''')
        
        conn.commit()
        conn.close()
    
    def save_game_result(self, player_name, home_city, cities_visited, route, route_length, algorithm, execution_time):
        """Save a game result to the database"""
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()
        
        # Convert route list to JSON string
        route_json = json.dumps(route)
        
        # Get current timestamp
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # Insert the result
        cursor.execute('''
        INSERT INTO game_results 
        (player_name, home_city, cities_visited, route, route_length, algorithm, execution_time, timestamp)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (player_name, home_city, cities_visited, route_json, route_length, algorithm, execution_time, timestamp))
        
        conn.commit()
        conn.close()
    
    def get_high_scores(self, limit=10):
        """Get the top scores from the database"""
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()
        
        cursor.execute('''
        SELECT player_name, home_city, cities_visited, route_length, algorithm, execution_time
        FROM game_results
        ORDER BY route_length ASC, execution_time ASC
        LIMIT ?
        ''', (limit,))
        
        results = cursor.fetchall()
        conn.close()
        
        return results
    
    def get_player_history(self, player_name):
        """Get history of a specific player"""
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()
        
        cursor.execute('''
        SELECT home_city, cities_visited, route_length, algorithm, execution_time, timestamp
        FROM game_results
        WHERE player_name = ?
        ORDER BY timestamp DESC
        ''', (player_name,))
        
        results = cursor.fetchall()
        conn.close()
        
        return results
    
    def get_algorithm_stats(self):
        """Get statistics about algorithm performance"""
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()
        
        cursor.execute('''
        SELECT algorithm, 
               AVG(execution_time) as avg_time,
               MIN(execution_time) as min_time,
               MAX(execution_time) as max_time,
               COUNT(*) as usage_count
        FROM game_results
        GROUP BY algorithm
        ORDER BY avg_time ASC
        ''')
        
        results = cursor.fetchall()
        conn.close()
        
        return results