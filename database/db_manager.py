"""
Database manager for the Traveling Salesman Problem game
Handles storage and retrieval of game results and statistics
"""
import logging
import sqlite3
import os
import json
from datetime import datetime
from typing import List, Dict, Any, Optional

logger = logging.getLogger("DatabaseManager")

class DatabaseManager:
    """
    Manager for database operations related to the TSP game
    """
    
    def __init__(self, db_file='tsp_game.db'):
        """Initialize database connection and create tables if needed"""
        self.db_file = db_file
        self._ensure_tables_exist()
        
    def _ensure_tables_exist(self):
        """Create necessary tables if they don't exist"""
        try:
            conn = sqlite3.connect(self.db_file)
            cursor = conn.cursor()
            
            # Create the game_results table if it doesn't exist
            cursor.execute('''
            CREATE TABLE IF NOT EXISTS game_results (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                player_name TEXT NOT NULL,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                home_city TEXT NOT NULL,
                cities_visited INTEGER NOT NULL,
                route TEXT NOT NULL,
                route_length REAL NOT NULL,
                winning_algorithm TEXT NOT NULL,
                execution_time REAL NOT NULL,
                is_prediction_correct BOOLEAN,
                prediction_algorithm TEXT
            )
            ''')
            
            conn.commit()
            logger.info(f"Database tables initialized in {self.db_file}")
        except sqlite3.Error as e:
            logger.error(f"Database error: {e}")
        finally:
            if conn:
                conn.close()
    
    def save_game_result(self, player_name: str, home_city: str, cities_visited: int,
                       route: List[str], route_length: float, algorithm: str,
                       execution_time: float, prediction_algorithm: str = None) -> bool:
        """
        Save a game result to the database
        
        Args:
            player_name: Name of the player
            home_city: Home city for the journey
            cities_visited: Number of cities visited
            route: List of cities in the optimal route
            route_length: Total distance of the route
            algorithm: Name of the winning algorithm
            execution_time: Time taken by the algorithm
            prediction_algorithm: Algorithm predicted by the player (optional)
        
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            conn = sqlite3.connect(self.db_file)
            cursor = conn.cursor()
            
            # Serialize the route list to JSON
            route_json = json.dumps(route)
            
            # Determine if the prediction was correct
            is_prediction_correct = None
            if prediction_algorithm:
                is_prediction_correct = (prediction_algorithm == algorithm)
            
            # Insert the result into the database
            cursor.execute('''
            INSERT INTO game_results 
            (player_name, home_city, cities_visited, route, route_length, 
             winning_algorithm, execution_time, is_prediction_correct, prediction_algorithm)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (player_name, home_city, cities_visited, route_json, route_length,
                  algorithm, execution_time, is_prediction_correct, prediction_algorithm))
            
            conn.commit()
            logger.info(f"Game result saved for player {player_name}")
            return True
        
        except sqlite3.Error as e:
            logger.error(f"Error saving game result: {e}")
            return False
        
        finally:
            if conn:
                conn.close()
                
    def get_recent_results(self, limit: int = 10) -> List[Dict[str, Any]]:
        """
        Get the most recent game results
        
        Args:
            limit: Maximum number of results to retrieve
        
        Returns:
            List of dictionaries containing game results
        """
        try:
            conn = sqlite3.connect(self.db_file)
            conn.row_factory = sqlite3.Row  # This enables column access by name
            cursor = conn.cursor()
            
            cursor.execute('''
            SELECT * FROM game_results
            ORDER BY timestamp DESC
            LIMIT ?
            ''', (limit,))
            
            results = []
            for row in cursor.fetchall():
                result = dict(row)
                # Parse the route from JSON
                result['route'] = json.loads(result['route'])
                results.append(result)
            
            return results
        
        except sqlite3.Error as e:
            logger.error(f"Error retrieving recent results: {e}")
            return []
        
        finally:
            if conn:
                conn.close()
    
    def get_player_statistics(self, player_name: str) -> Dict[str, Any]:
        """
        Get statistics for a specific player
        
        Args:
            player_name: Name of the player
        
        Returns:
            Dictionary containing player statistics
        """
        try:
            conn = sqlite3.connect(self.db_file)
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            
            # Get total games played
            cursor.execute('''
            SELECT COUNT(*) as games_played FROM game_results
            WHERE player_name = ?
            ''', (player_name,))
            
            result = dict(cursor.fetchone())
            games_played = result['games_played']
            
            if games_played == 0:
                return {"player_name": player_name, "games_played": 0}
            
            # Get correct predictions
            cursor.execute('''
            SELECT COUNT(*) as correct_predictions FROM game_results
            WHERE player_name = ? AND is_prediction_correct = 1
            ''', (player_name,))
            
            result = dict(cursor.fetchone())
            correct_predictions = result['correct_predictions']
            
            # Get algorithm distribution
            cursor.execute('''
            SELECT winning_algorithm, COUNT(*) as count FROM game_results
            WHERE player_name = ?
            GROUP BY winning_algorithm
            ORDER BY count DESC
            ''', (player_name,))
            
            algorithm_distribution = {}
            for row in cursor.fetchall():
                algorithm_distribution[row['winning_algorithm']] = row['count']
            
            # Get average route length
            cursor.execute('''
            SELECT AVG(route_length) as avg_length FROM game_results
            WHERE player_name = ?
            ''', (player_name,))
            
            result = dict(cursor.fetchone())
            avg_route_length = result['avg_length']
            
            return {
                "player_name": player_name,
                "games_played": games_played,
                "correct_predictions": correct_predictions,
                "prediction_accuracy": (correct_predictions / games_played) if games_played > 0 else 0,
                "algorithm_distribution": algorithm_distribution,
                "average_route_length": avg_route_length
            }
        
        except sqlite3.Error as e:
            logger.error(f"Error retrieving player statistics: {e}")
            return {"player_name": player_name, "error": str(e)}
        
        finally:
            if conn:
                conn.close()
    
    def get_leaderboard(self, limit: int = 10) -> List[Dict[str, Any]]:
        """
        Get a leaderboard of players based on their prediction accuracy
        
        Args:
            limit: Maximum number of players to include
        
        Returns:
            List of dictionaries containing player rankings
        """
        try:
            conn = sqlite3.connect(self.db_file)
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            
            cursor.execute('''
            SELECT 
                player_name,
                COUNT(*) as games_played,
                SUM(CASE WHEN is_prediction_correct = 1 THEN 1 ELSE 0 END) as correct_predictions
            FROM game_results
            GROUP BY player_name
            HAVING games_played >= 3
            ORDER BY (correct_predictions * 1.0 / games_played) DESC, games_played DESC
            LIMIT ?
            ''', (limit,))
            
            leaderboard = []
            for i, row in enumerate(cursor.fetchall(), 1):
                entry = dict(row)
                entry['rank'] = i
                entry['accuracy'] = (entry['correct_predictions'] / entry['games_played']) if entry['games_played'] > 0 else 0
                leaderboard.append(entry)
            
            return leaderboard
        
        except sqlite3.Error as e:
            logger.error(f"Error retrieving leaderboard: {e}")
            return []
        
        finally:
            if conn:
                conn.close()
    
    def clear_data(self) -> bool:
        """
        Clear all data from the database (for testing or resetting)
        
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            conn = sqlite3.connect(self.db_file)
            cursor = conn.cursor()
            
            cursor.execute('DELETE FROM game_results')
            conn.commit()
            
            logger.info("All game data cleared from database")
            return True
        
        except sqlite3.Error as e:
            logger.error(f"Error clearing database: {e}")
            return False
        
        finally:
            if conn:
                conn.close()
    
    def save_session(self, player_name: str, game_state_data: Dict[str, Any]) -> bool:
        """
        Save the current game session for later continuation
        
        Args:
            player_name: Name of the player
            game_state_data: Dictionary containing serializable game state data
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            conn = sqlite3.connect(self.db_file)
            cursor = conn.cursor()
            
            # Create sessions table if it doesn't exist
            cursor.execute('''
            CREATE TABLE IF NOT EXISTS sessions (
                player_name TEXT PRIMARY KEY,
                session_data TEXT NOT NULL,
                last_updated DATETIME DEFAULT CURRENT_TIMESTAMP
            )
            ''')
            
            # Serialize the game state to JSON
            session_data = json.dumps(game_state_data)
            
            # Insert or update the session
            cursor.execute('''
            INSERT OR REPLACE INTO sessions 
            (player_name, session_data, last_updated)
            VALUES (?, ?, CURRENT_TIMESTAMP)
            ''', (player_name, session_data))
            
            conn.commit()
            logger.info(f"Game session saved for player {player_name}")
            return True
        
        except sqlite3.Error as e:
            logger.error(f"Error saving game session: {e}")
            return False
        
        finally:
            if conn:
                conn.close()
    
    def load_session(self, player_name: str) -> Optional[Dict[str, Any]]:
        """
        Load a previously saved game session
        
        Args:
            player_name: Name of the player
            
        Returns:
            Dictionary containing game state data or None if no session found
        """
        try:
            conn = sqlite3.connect(self.db_file)
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            
            # Check if sessions table exists
            cursor.execute('''
            SELECT name FROM sqlite_master 
            WHERE type='table' AND name='sessions'
            ''')
            
            if not cursor.fetchone():
                logger.info("No sessions table exists yet")
                return None
                
            # Get the session data
            cursor.execute('''
            SELECT session_data, last_updated FROM sessions
            WHERE player_name = ?
            ''', (player_name,))
            
            row = cursor.fetchone()
            if not row:
                logger.info(f"No saved session found for player {player_name}")
                return None
                
            # Parse the session data from JSON
            session_data = json.loads(row['session_data'])
            
            # Add last_updated information
            session_data['last_updated'] = row['last_updated']
            
            logger.info(f"Game session loaded for player {player_name}")
            return session_data
        
        except sqlite3.Error as e:
            logger.error(f"Error loading game session: {e}")
            return None
        
        except json.JSONDecodeError as e:
            logger.error(f"Error decoding session data: {e}")
            return None
            
        finally:
            if conn:
                conn.close()
                
    def delete_session(self, player_name: str) -> bool:
        """
        Delete a saved game session
        
        Args:
            player_name: Name of the player
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            conn = sqlite3.connect(self.db_file)
            cursor = conn.cursor()
            
            # Check if sessions table exists
            cursor.execute('''
            SELECT name FROM sqlite_master 
            WHERE type='table' AND name='sessions'
            ''')
            
            if not cursor.fetchone():
                logger.info("No sessions table exists")
                return False
            
            # Delete the session
            cursor.execute('''
            DELETE FROM sessions
            WHERE player_name = ?
            ''', (player_name,))
            
            conn.commit()
            
            if cursor.rowcount > 0:
                logger.info(f"Game session deleted for player {player_name}")
                return True
            else:
                logger.info(f"No session found to delete for player {player_name}")
                return False
        
        except sqlite3.Error as e:
            logger.error(f"Error deleting game session: {e}")
            return False
            
        finally:
            if conn:
                conn.close()