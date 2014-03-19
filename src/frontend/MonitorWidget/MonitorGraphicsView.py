# -*- coding: utf-8 -*-

from PyQt5.QtCore import QPointF
from PyQt5.QtGui import QPolygonF, QPen, QBrush, QLinearGradient
from PyQt5.Qt import Qt
from PyQt5.QtWidgets import QGraphicsView, QGraphicsScene

class MonitorGraphicsView(QGraphicsView):
    monitorWin = None

    SIZE = (50.0, 50.0)
    MAXSPEED = 1024 * 1024 # 1mb in bytes

    _progressText = None
    _speedsPolygon = None
    _speedsPen = None
    _speedsBrush = None

    def __init__(self, parent = None):
        super().__init__(parent)
        self.monitorWin = parent
        self.scene = QGraphicsScene(self)
        self.scene.setSceneRect(0, 0, self.SIZE[0], self.SIZE[1])
        self.setScene(self.scene)

        self._speedsPen = QPen(Qt.white)

        gradient = QLinearGradient(0, 0, self.SIZE[0], self.SIZE[1])
        gradient.setColorAt(0.0, Qt.darkGreen)
        gradient.setColorAt(1.0, Qt.yellow)
        self._speedsBrush = QBrush(gradient)

        # add elements to the scene
        self._speedsPolygon = self.scene.addPolygon(QPolygonF(),
                                                    self._speedsPen,
                                                    self._speedsBrush)
        self._progressText = self.scene.addText("")
        self._progressText.setPos(10, 0)

    def mousePressEvent(self, qMouseEvent):
        self.monitorWin.mousePressEvent(qMouseEvent)

    def mouseMoveEvent(self, qMouseEvent):
        self.monitorWin.mouseMoveEvent(qMouseEvent)

    def mouseReleaseEvent(self, qMouseEvent):
        self.monitorWin.mouseReleaseEvent(qMouseEvent)

    def _setSpeeds(self, speeds):
        polygon = QPolygonF()
        polygon.append(QPointF(0, self.SIZE[1])) # start the polygon

        nSamples = len(speeds)
        xPerSample = self.SIZE[0] / nSamples

        for i, speed in enumerate(speeds):
            y = self._translateSpeedToPosY(speed)
            polygon.append(QPointF(xPerSample * i, y))
            polygon.append(QPointF(xPerSample * (i+1), y))
        polygon.append(QPointF(*self.SIZE)) # close the polygon

        self._speedsPolygon.setPolygon(polygon)

    def _setProgress(self, process): # 10000 means 100%
        self._progressText.setPlainText("{:.1f}%".format(process / 100))

    @classmethod
    def _translateSpeedToPosY(cls, speed):
        return cls.SIZE[1] * (1.0 - speed / cls.MAXSPEED)
