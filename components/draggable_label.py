from PySide6.QtWidgets import QLabel
from PySide6.QtCore import Qt, QPoint


class DraggableLabel(QLabel):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._dragging = False
        self._drag_offset = QPoint()

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self._dragging = True
            # Offset between mouse position and widget top-left
            self._drag_offset = event.position().toPoint()
            self.setCursor(Qt.CursorShape.ClosedHandCursor)
            event.accept()
        else:
            super().mousePressEvent(event)

    def mouseMoveEvent(self, event):
        if self._dragging:
            # Move relative to parent
            new_pos = self.mapToParent(event.position().toPoint() - self._drag_offset)
            parent_rect = self.parent().rect()
            new_pos.setX(max(0, min(new_pos.x(), parent_rect.width() - self.width())))
            new_pos.setY(max(0, min(new_pos.y(), parent_rect.height() - self.height())))
            self.move(new_pos)
            event.accept()
        else:
            super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self._dragging = False
            self.setCursor(Qt.CursorShape.ArrowCursor)
            event.accept()
        else:
            super().mouseReleaseEvent(event)
