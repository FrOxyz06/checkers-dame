"""Pygame interface. Run with: python Board.py"""
from pathlib import Path
import pygame
from game import Game, SIZE

CELL = 60
BASE = Path(__file__).resolve().parent

def draw(screen, game, selected, sprites, font):
    for row in range(SIZE):
        for col in range(SIZE):
            color = (78, 89, 76) if (row + col) % 2 else (232, 222, 200)
            pygame.draw.rect(screen, color, (col * CELL, row * CELL, CELL, CELL))
    if selected is not None:
        row, col = selected
        pygame.draw.rect(screen, (240, 194, 60), (col * CELL, row * CELL, CELL, CELL), 4)
        for row, col in game.legal_moves(selected):
            pygame.draw.circle(screen, (90, 205, 150), (col * CELL + 30, row * CELL + 30), 9)
    for (row, col), piece in game.board.items():
        screen.blit(sprites[piece.color], (col * CELL + 5, row * CELL + 5))
        if piece.king:
            label = font.render("K", True, (220, 100, 25))
            screen.blit(label, label.get_rect(center=(col * CELL + 30, row * CELL + 30)))
    pygame.draw.rect(screen, (30, 36, 40), (0, 600, 600, 60))
    status = f"{game.winner.title()} wins! Press R to restart." if game.winner else f"{game.turn.title()}'s turn"
    if game.forced_piece is not None:
        status += " - continue capturing"
    screen.blit(font.render(status, True, (245, 245, 240)), (15, 612))
    screen.blit(pygame.font.Font(None, 20).render("Click a piece, then a green destination. R: restart | Esc: quit", True, (195, 200, 205)), (15, 640))

def main():
    pygame.init()
    try:
        screen = pygame.display.set_mode((600, 660))
        pygame.display.set_caption("Checkers / Dame")
        sprites = {
            color: pygame.transform.smoothscale(pygame.image.load(BASE / "Assets" / f"{color}_piece.png").convert_alpha(), (50, 50))
            for color in ("black", "white")
        }
        font = pygame.font.Font(None, 28)
        clock = pygame.time.Clock()
        game = Game()
        selected = None
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False
                    elif event.key == pygame.K_r:
                        game, selected = Game(), None
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    col, row = event.pos[0] // CELL, event.pos[1] // CELL
                    target = (row, col)
                    if selected is not None and game.move(selected, target):
                        selected = game.forced_piece
                    elif game.legal_moves(target):
                        selected = target
                    elif game.forced_piece is None:
                        selected = None
            draw(screen, game, selected, sprites, font)
            pygame.display.flip()
            clock.tick(60)
    finally:
        pygame.quit()

if __name__ == "__main__":
    main()
