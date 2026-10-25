"""Hand-drawn nav-tile icons for glyphs that don't render reliably as emoji
(missing color-emoji font coverage shows these as blank boxes on some
systems, and even where the font IS present, a few of these glyphs --
notably control knobs -- fall back to an illegible monochrome form). Drawn
with QPainter instead, same approach as robot_face.py's Assistant icon.
"""
from __future__ import annotations

from PySide6.QtCore import QPointF, QRectF, Qt
from PySide6.QtGui import QColor, QPainter, QPen, QPixmap, QPolygonF

_ICON_COLOR = "#cfd3da"  # fallback; callers normally pass the active theme's icon color


def _new_pixmap(size: int, color: str) -> tuple[QPixmap, QPainter]:
    pixmap = QPixmap(size, size)
    pixmap.fill(Qt.GlobalColor.transparent)
    painter = QPainter(pixmap)
    painter.setRenderHint(QPainter.RenderHint.Antialiasing)
    pen = QPen(QColor(color))
    pen.setWidthF(size * 0.06)
    pen.setCapStyle(Qt.PenCapStyle.RoundCap)
    pen.setJoinStyle(Qt.PenJoinStyle.RoundJoin)
    painter.setPen(pen)
    return pixmap, painter


def draw_folder_icon(size: int, color: str = _ICON_COLOR) -> QPixmap:
    pixmap, painter = _new_pixmap(size, color)

    tab = QRectF(size * 0.14, size * 0.22, size * 0.32, size * 0.14)
    painter.drawRoundedRect(tab, size * 0.03, size * 0.03)

    body = QRectF(size * 0.14, size * 0.32, size * 0.72, size * 0.5)
    painter.drawRoundedRect(body, size * 0.05, size * 0.05)

    painter.end()
    return pixmap


def draw_spool_icon(size: int, color: str = _ICON_COLOR) -> QPixmap:
    """Side view of a thread spool: two flanges joined by a wound hub."""
    pixmap, painter = _new_pixmap(size, color)

    left = size * 0.22
    right = size * 0.78
    top_y = size * 0.2
    bottom_y = size * 0.8
    flange_h = size * 0.16

    top_rect = QRectF(left, top_y - flange_h / 2, right - left, flange_h)
    bottom_rect = QRectF(left, bottom_y - flange_h / 2, right - left, flange_h)
    painter.drawEllipse(top_rect)
    painter.drawEllipse(bottom_rect)

    painter.drawLine(QPointF(left, top_y), QPointF(left, bottom_y))
    painter.drawLine(QPointF(right, top_y), QPointF(right, bottom_y))

    # Wound filament: a single X between the flanges.
    inset = size * 0.08
    painter.drawLine(QPointF(left + inset, top_y), QPointF(right - inset, bottom_y))
    painter.drawLine(QPointF(right - inset, top_y), QPointF(left + inset, bottom_y))

    painter.end()
    return pixmap


def draw_jog_icon(size: int, color: str = _ICON_COLOR) -> QPixmap:
    """Four-direction d-pad, representing the Control screen's jog grid."""
    pixmap, painter = _new_pixmap(size, color)
    painter.setBrush(QColor(color))

    cx, cy = size * 0.5, size * 0.5
    arm = size * 0.16  # distance from center to each arrowhead's base
    tip = size * 0.36  # distance from center to each arrowhead's tip
    half_w = size * 0.1

    def arrow(dx: float, dy: float, perp_dx: float, perp_dy: float) -> QPolygonF:
        base_cx = cx + dx * arm
        base_cy = cy + dy * arm
        tip_x = cx + dx * tip
        tip_y = cy + dy * tip
        return QPolygonF(
            [
                QPointF(base_cx + perp_dx * half_w, base_cy + perp_dy * half_w),
                QPointF(base_cx - perp_dx * half_w, base_cy - perp_dy * half_w),
                QPointF(tip_x, tip_y),
            ]
        )

    painter.drawPolygon(arrow(0, -1, 1, 0))  # up
    painter.drawPolygon(arrow(0, 1, 1, 0))  # down
    painter.drawPolygon(arrow(-1, 0, 0, 1))  # left
    painter.drawPolygon(arrow(1, 0, 0, 1))  # right

    painter.setBrush(Qt.BrushStyle.NoBrush)
    painter.drawEllipse(QPointF(cx, cy), size * 0.08, size * 0.08)

    painter.end()
    return pixmap
