import pygame

import settings
from block import Block

class Level:
    def __init__(self, level_path: str):
        self.display_surface = pygame.display.get_surface()

        self.dragging_block = False

        self.getBlocks(level_path)

    def getBlocks(self, level_path: str) -> None:
        self.blocks = BlockGroup()

        with open(f"levels/{level_path}", "r") as f:
            rows = f.read().split("\n")
        for row_i, row in enumerate(rows):
            for col_i, col in enumerate(row):
                if col == "1":
                    self.blocks.add(Block(self, (col_i, row_i), 1, 1, "yellow"))
                elif col == "2":
                    self.blocks.add(Block(self, (col_i, row_i), 1, 2, "blue"))
                elif col == "3":
                    self.blocks.add(Block(self, (col_i, row_i), 2, 1, "green"))
                elif col == "4":
                    self.main_block = Block(self, (col_i, row_i), 2, 2, "red")
                    self.blocks.add(self.main_block)

    def update(self):
        """called once per frame"""
        self.blocks.draw()
        self.blocks.update()

class BlockGroup(list):
    def __init__(self):
        """every object in this group must have a update and draw method"""
        super().__init__()

        self.display_surface = pygame.display.get_surface()
    
    def add(self, obj: object) -> None:
        """adds an object to the group"""
        self.append(obj)

    def draw(self) -> None:
        """draws each object in the group"""
        for obj in self:
            obj.draw(self.display_surface)
    
    def update(self) -> None:
        """updates each object in the group"""
        for obj in self:
            obj.update()