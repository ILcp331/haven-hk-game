from typing import Literal

import pygame as pg

pg.init()


def draw_line(
    surface: pg.Surface,
    pos: tuple[float, float] | pg.Vector2,
    font: pg.font.Font,
    line: str,
    color: tuple[int, int, int] | pg.Color,
    *,
    background: tuple[int, int, int, int] | pg.Color = pg.Color(0, 0, 0, 0),
    alignment: Literal['left', 'centered', 'right'] = 'left',
) -> None:
    """Draws a line of text on a surface.

    Args:
        surface (pg.Surface): The surface to draw text onto.
        pos (tuple[float, float] | pg.Vector2): The position of the text.
        font (pg.font.Font): The font object used to render each line.
        line (str): The string to draw.
        color (tuple[int, int, int] | pg.Color): The color of the text.
        background (tuple[int, int, int, int] | pg.Color, optional): RGBA for the text's background. \
        Defaults to (0, 0, 0, 0).
        alignment (Literal['left', 'centered', 'right'], optional): The alignment of the text at \
        the provided position. Defaults to 'left'.
    """

    pos = pg.Vector2(pos)

    text = font.render(line, True, color)
    text_width = text.get_width()
    text_height = text.get_height()

    text_surf = pg.Surface((text_width, text_height), pg.SRCALPHA)
    text_surf.fill(background)
    text_surf.blit(text)

    if alignment == 'centered':
        pos.x -= text_width / 2

    elif alignment == 'right':
        pos.x -= text_width

    surface.blit(text_surf, pos)


def draw_lines(
    surface: pg.Surface,
    start_pos: tuple[float, float] | pg.Vector2,
    font: pg.font.Font,
    lines: list[str],
    color: tuple[int, int, int] | pg.Color,
    margin: float = 2,
    *,
    background: tuple[int, int, int, int] | pg.Color = pg.Color(0, 0, 0, 0),
    alignment: Literal['left', 'centered', 'right'] = 'left',
) -> None:
    """Draws multiple lines of text on a surface.

    _extended_summary_

    Args:
        surface (pg.Surface): The surface to blit onto.
        start_pos (tuple[float, float] | pg.Vector2): The position of the text.
        font (pg.font.Font): The font object used to render each line.
        lines (list[str]): A list of strings to draw. No '\\n' escape sequences are needed.
        color (tuple[int, int, int] | pg.Color): The color of the text.
        margin (float, optional): Margin between each line. Defaults to 2.
        background (tuple[int, int, int, int] | pg.Color, optional): RGBA for the text's background. Defaults to (0, 0, 0, 0).
        alignment (Literal['left', 'centered', 'right'], optional): The alignment of the lines of text at the provided position. Defaults to 'left'.
    """
    current_pos = pg.Vector2(start_pos)

    for line in lines:
        draw_line(surface, current_pos.copy(), font, line, color,
                  background=background, alignment=alignment)

        current_pos.y += font.get_linesize() + margin
