from unittest.mock import NonCallableMagicMock
import pygame

import settings

class Block:
    def __init__(self, level, start_topleft_units: tuple, unit_width: int, unit_height: int, colour: pygame.color):
        self.rect = pygame.rect.Rect(start_topleft_units[0]*settings.UNIT_SIZE, start_topleft_units[1]*settings.UNIT_SIZE, unit_width*settings.UNIT_SIZE, unit_height*settings.UNIT_SIZE)
        self.tlrect = pygame.rect.Rect(self.rect.topleft, (settings.UNIT_SIZE, settings.UNIT_SIZE))
        self.colour = colour

        self.level = level

        self.being_dragged = False
        self.drag_offset = pygame.math.Vector2()

    def draw(self, display_surface) -> None:
        """draws block visual to display surface"""
        disp_rect = self.rect.inflate(-5, -5)
        pygame.draw.rect(display_surface, self.colour, disp_rect, border_radius=10)
    
    def update(self) -> None:
        """called once per frame"""
        mouse_pos = pygame.mouse.get_pos()
        lmouse_pressed = pygame.mouse.get_pressed()[0]

        if lmouse_pressed and self.rect.collidepoint(mouse_pos) and not self.being_dragged and not self.level.dragging_block:
                self.being_dragged = True
                self.level.dragging_block = True
                self.drag_offset.x = self.rect.centerx - mouse_pos[0]
                self.drag_offset.y = self.rect.centery - mouse_pos[1]
        
        if lmouse_pressed and self.being_dragged:
            self.drag(mouse_pos, "horizontal")
            self.drag(mouse_pos, "vertical")

        if not lmouse_pressed and self.being_dragged:
            self.being_dragged = False
            self.level.dragging_block = False

            self.tlrect = pygame.rect.Rect(self.rect.topleft, (settings.UNIT_SIZE, settings.UNIT_SIZE))
            for row in range(5):
                for col in range(5):
                    grid_rect = pygame.rect.Rect(col*settings.UNIT_SIZE, row*settings.UNIT_SIZE, settings.UNIT_SIZE, settings.UNIT_SIZE)
                    if grid_rect.collidepoint(self.tlrect.center):
                        self.rect.topleft = grid_rect.topleft
            self.tlrect = pygame.rect.Rect(self.rect.topleft, (settings.UNIT_SIZE, settings.UNIT_SIZE))
    
    def drag(self, mouse_pos: tuple, direction: str) -> None:
        """attempts to drag in specified direction
        drag = [horizontal/vertical]"""
        next_rect = self.rect.copy()
        if direction == 'horizontal':
            next_rect.centerx = mouse_pos[0] + self.drag_offset.x

            if next_rect.left < 0 or next_rect.right > settings.WIDTH: return
        else:
            next_rect.centery = mouse_pos[1] + self.drag_offset.y

            if next_rect.top < 0 or next_rect.bottom > settings.HEIGHT: return
        
        can_move = True
        for block in self.level.blocks:
            if block == self: continue

            if block.rect.colliderect(next_rect):
                can_move = False
                break
                
        if can_move:
            self.rect = next_rect