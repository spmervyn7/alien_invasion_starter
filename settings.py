"""
Program Name: settings.py
Author: Mervyn S. Philip
Purpose: This saves all the game's settings (like screen size, 
         speeds, and colors) in one central place. That way, 
         other parts of the game can easily use them instead 
         of repeating the numbers everywhere.
Starter Code: Adapted from the in-class Alien Invasion tutorial
             (base repo: https://github.com/RedBeard41/alien_Invasion_starter.git).
             It sets up the game screen, tells the game where to find pictures and
             sounds, and controls how the game gets harder over time for a special
             project milestone.
Date: 2026-07-31
"""

from pathlib import Path
import pygame
import sys


class Settings:
    """Stores all static and dynamic settings for Alien Invasion.

    Some game settings never change once they are set up (like 
    screen size and colors). Other settings change during the 
    game (like speed and lives)—they restart when a new game 
    begins and get harder as you play better.
    """

    def __init__(self) -> None:
        """Initialize the game's static settings and asset paths.

        All file paths use pathlib so the game runs correctly on
        both Windows and macOS.
        """
        self.name: str = "Alien Invasion"
        self.screen_w = 1200
        self.screen_h = 800
        self.fps = 60
        self.bg_file = Path.cwd() / 'Assets' / 'images' / 'Starbasesnow.png'
        self.difficulty_scale = 1.1
        self.scores_file = Path.cwd() / 'Assets' / 'file' / 'scores.json'

        self.ship_file = Path.cwd() / 'Assets' / 'images' / 'ship2(no bg).png'
        self.ship_w = 60
        self.ship_h = 90

        self.bullet_file = Path.cwd() / 'Assets' / 'images' / 'laserBlast.png'
        self.laser_sound = Path.cwd() / 'Assets' / 'sound' / 'laser.mp3'
        self.impact_sound = Path.cwd() / 'Assets' / 'sound' / 'impactSound.mp3'
        self.bullet_w = 25
        self.bullet_h = 80

        self.alien_file = Path.cwd() / 'Assets' / 'images' / 'enemy_4.png'
        self.fleet_direction = 1
        self.alien_w = 40
        self.alien_h = 40

        self.button_w = 200
        self.button_h = 50
        self.button_color = (0, 160, 220)

        self.text_color = (255, 255, 255)
        self.button_font_size = 48
        self.HUD_font_size = 20
        self.font_style = Path.cwd() / 'Assets' / 'Fonts' / 'Silkscreen' / 'Silkscreen-Bold.ttf'

    def initialize_dynamic_settings(self) -> None:
        """This resets the changing game settings back to their original
         starting values.

        It runs when the game first starts and every time you click the 
        Play button for a new game, making sure old difficulty levels 
        don't carry over from your last game.
        """
        self.ship_speed = 10
        self.starting_ship_count = 3

        self.bullet_w = 25
        self.bullet_h = 80
        self.bullet_speed = 10
        self.bullet_amount = 5

        self.fleet_speed = 2
        self.fleet_drop_speed = 40
        self.alien_points = 50

    def increase_difficulty(self) -> None:
        """Makes the ship, bullets, and aliens move faster based
         on the difficulty level.

        This happens every time you clear a whole group of aliens,
         making each new level a little faster than the last.
        """
        self.ship_speed *= self.difficulty_scale
        self.bullet_speed *= self.difficulty_scale
        self.fleet_speed *= self.difficulty_scale