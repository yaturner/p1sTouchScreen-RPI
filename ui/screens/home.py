from __future__ import annotations

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QGridLayout, QLabel, QPushButton, QVBoxLayout, QWidget

from state import GcodeState, PrinterState
from ui.theme import palette
from ui.widgets.nav_icons import draw_folder_icon, draw_jog_icon, draw_spool_icon
from ui.widgets.nav_tile import NavTile
from ui.widgets.robot_face import draw_robot_face

_ASSISTANT_ICON_SIZE = 72
_NAV_ICON_SIZE = 96

# Drawn icons for glyphs that don't render reliably as emoji (missing
# color-emoji font coverage shows these as blank boxes on some systems,
# and control knobs in particular falls back to an illegible monochrome
# form even where the font IS present) -- see ui/widgets/nav_icons.py.
_DRAWN_ICONS = {
    "print_files": draw_folder_icon,
    "filament_ams": draw_spool_icon,
    "control": draw_jog_icon,
}


class HomeScreen(QWidget):
    def __init__(self, main_window) -> None:
        super().__init__()
        self._main_window = main_window
        self.setObjectName("homeScreen")

        root = QVBoxLayout(self)
        root.setContentsMargins(24, 24, 24, 24)
        root.setSpacing(16)

        self._banner = QPushButton()
        self._banner.setObjectName("printBanner")
        self._banner.clicked.connect(lambda: self._main_window.navigate_to("print_monitor"))
        self._banner.hide()
        root.addWidget(self._banner)

        grid = QGridLayout()
        grid.setSpacing(16)
        tiles = [
            ("🗂", "Print Files", "print_files"),
            # Reachable anytime (not just via the print-progress banner
            # while something's actually printing), matching the Android
            # port's Home tile grid -- lets you check the camera feed/
            # status screen preemptively.
            ("▶", "Print Monitor", "print_monitor"),
            ("🧵", "Filament", "filament_ams"),
            ("🕹", "Control", "control"),
            ("⚙", "Settings", "settings"),
            ("🩺", "Assistant", "assistant"),
        ]
        self._assistant_tile: NavTile | None = None
        self._drawn_tiles: dict[str, NavTile] = {}
        columns = 3
        icon_color = palette(main_window.config.app.theme)["icon"]
        for i, (icon, label, target) in enumerate(tiles):
            tile = NavTile(icon, label)
            tile.clicked.connect(lambda t=target: self._main_window.navigate_to(t))
            grid.addWidget(tile, i // columns, i % columns)
            if target == "assistant":
                self._assistant_tile = tile
                tile.set_icon_pixmap(draw_robot_face(sad=False, size=_ASSISTANT_ICON_SIZE))
            elif target in _DRAWN_ICONS:
                self._drawn_tiles[target] = tile
                tile.set_icon_pixmap(_DRAWN_ICONS[target](_NAV_ICON_SIZE, icon_color))
        rows = -(-len(tiles) // columns)  # ceil division
        for r in range(rows):
            grid.setRowStretch(r, 1)
        for c in range(columns):
            grid.setColumnStretch(c, 1)
        root.addLayout(grid, 1)

    def apply_state(self, state: PrinterState) -> None:
        if state.gcode_state in (GcodeState.RUNNING, GcodeState.PAUSE):
            pct = state.print_percent if state.print_percent is not None else 0
            name = state.current_file or "print job"
            status = "Paused" if state.gcode_state == GcodeState.PAUSE else "Printing"
            self._banner.setText(f"{status}: {name} — {pct}%  (tap to view)")
            self._banner.show()
        else:
            self._banner.hide()

        if self._assistant_tile is not None:
            self._assistant_tile.set_icon_pixmap(
                draw_robot_face(sad=bool(state.hms_errors), size=_ASSISTANT_ICON_SIZE)
            )

    def apply_theme(self, mode: str) -> None:
        """Re-draws the hand-painted nav icons in the new theme's icon color.

        Only needed for these three -- robot_face's colors are fixed
        (red/green read fine on both light and dark) and the rest of the
        screen's styling comes from the QSS stylesheet, which MainWindow
        re-applies separately.
        """
        icon_color = palette(mode)["icon"]
        for target, tile in self._drawn_tiles.items():
            tile.set_icon_pixmap(_DRAWN_ICONS[target](_NAV_ICON_SIZE, icon_color))
