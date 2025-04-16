#!/usr/bin/env python3
"""
Traveling Salesman Problem Game - Main Entry Point
"""
import sys
from gui.game_window import GameWindow

if __name__ == "__main__":
    app = GameWindow()
    sys.exit(app.run())