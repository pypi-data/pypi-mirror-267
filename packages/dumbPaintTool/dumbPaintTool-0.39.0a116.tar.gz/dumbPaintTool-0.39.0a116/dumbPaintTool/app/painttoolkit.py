# MIT License
#
# Copyright (c) 2024 Eugenio Parodi <ceccopierangiolieugenio AT googlemail DOT com>
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

__all__ = ['PaintToolKit']

import os

import TermTk as ttk

from .paintarea import *
from .glbls     import glbls

class PaintToolKit(ttk.TTkContainer):
    __slots__ = ('_rSelect', '_rPaint', '_lgliph',
                 '_cbFg', '_cbBg',
                 '_bpFg', '_bpBg', '_bpDef',
                 '_sbDx','_sbDy','_sbDw','_sbDh',
                 '_sbLx','_sbLy','_sbLw','_sbLh',
                 #Signals
                 'updatedTrans')
    def __init__(self, *args, **kwargs):
        ttk.TTkUiLoader.loadFile(os.path.join(os.path.dirname(os.path.abspath(__file__)),"../tui/paintToolKit.tui.json"),self)
        self.updatedTrans = ttk.pyTTkSignal(ttk.TTkColor)
        self._lgliph  = self.getWidgetByName("lglyph")
        self._cbFg    = self.getWidgetByName("cbFg")
        self._cbBg    = self.getWidgetByName("cbBg")
        self._bpFg    = self.getWidgetByName("bpFg")
        self._bpBg    = self.getWidgetByName("bpBg")
        self._bpDef   = self.getWidgetByName("bpDef")

        self._sbDx = self.getWidgetByName("sbDx")
        self._sbDy = self.getWidgetByName("sbDy")
        self._sbDw = self.getWidgetByName("sbDw")
        self._sbDh = self.getWidgetByName("sbDh")
        self._sbLx = self.getWidgetByName("sbLx")
        self._sbLy = self.getWidgetByName("sbLy")
        self._sbLw = self.getWidgetByName("sbLw")
        self._sbLh = self.getWidgetByName("sbLh")

        self._bpDef.setColor(ttk.TTkColor.bg('#FF00FF'))
        self._cbFg.toggled.connect(self._refreshColor)
        self._cbBg.toggled.connect(self._refreshColor)

        self._bpFg.colorSelected.connect(self._refreshColor)
        self._bpBg.colorSelected.connect(self._refreshColor)
        self._bpDef.colorSelected.connect(self.updatedTrans.emit)

        glbls.brush.glyphChanged.connect(   lambda:self._refreshColor(False))
        glbls.brush.colorChanged.connect(   self.setColor)

        self._refreshColor(emit=False)

    @ttk.pyTTkSlot(CanvasLayer)
    def updateLayer(self, layer:CanvasLayer):
        lx,ly = layer.pos()
        lw,lh = layer.size()
        self._sbLx.setValue(lx)
        self._sbLy.setValue(ly)
        self._sbLw.setValue(lw)
        self._sbLh.setValue(lh)

    @ttk.pyTTkSlot()
    def _refreshColor(self, emit=True):
        glyph = glbls.brush.glyph()
        color = self.color()
        self._lgliph.setText(
                ttk.TTkString("Glyph: '") +
                ttk.TTkString(glyph,color) +
                ttk.TTkString("'"))
        if emit:
            glbls.brush.setColor(color)

    def color(self):
        color = ttk.TTkColor()
        if self._cbFg.checkState() == ttk.TTkK.Checked:
            color += self._bpFg.color().invertFgBg()
        if self._cbBg.checkState() == ttk.TTkK.Checked:
           color += self._bpBg.color()
        return color

    @ttk.pyTTkSlot(ttk.TTkColor)
    def setColor(self, color:ttk.TTkColor):
        if fg := color.foreground():
            self._cbFg.setCheckState(ttk.TTkK.Checked)
            self._bpFg.setEnabled()
            self._bpFg.setColor(fg.invertFgBg())
        else:
            self._cbFg.setCheckState(ttk.TTkK.Unchecked)
            self._bpFg.setDisabled()

        if bg := color.background():
            self._cbBg.setCheckState(ttk.TTkK.Checked)
            self._bpBg.setEnabled()
            self._bpBg.setColor(bg)
        else:
            self._cbBg.setCheckState(ttk.TTkK.Unchecked)
            self._bpBg.setDisabled()
        self._refreshColor(emit=False)
