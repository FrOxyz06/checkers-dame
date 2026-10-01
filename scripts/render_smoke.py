"""Render the real interface without opening a window."""
import os
from pathlib import Path
import sys
os.environ.setdefault("SDL_VIDEODRIVER", "dummy")
os.environ.setdefault("SDL_AUDIODRIVER", "dummy")
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
import pygame
from Board import draw
from game import Game

pygame.init()
try:
    screen = pygame.display.set_mode((600, 660))
    sprites = {
        color: pygame.transform.smoothscale(pygame.image.load(ROOT / "Assets" / f"{color}_piece.png").convert_alpha(), (50, 50))
        for color in ("black", "white")
    }
    draw(screen, Game(), (2, 1), sprites, pygame.font.Font(None, 28))
    if "--save" in sys.argv:
        (ROOT / "docs").mkdir(exist_ok=True)
        pygame.image.save(screen, ROOT / "docs" / "screenshot.png")
    pygame.display.flip()
    # Also exercise the main event loop and clean shutdown.
    pygame.event.post(pygame.event.Event(pygame.QUIT))
    from Board import main
    main()
finally:
    pygame.quit()
print("Interface rendered and quit successfully.")
