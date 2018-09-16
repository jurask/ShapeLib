# Shape library for KLayout GDS editor
# Copyright (C) 2018  Jiri Babocky
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

import pya
import math

class TText(pya.PCellDeclarationHelper):

  def __init__(self):
    # Important: initialize the super class
    super(TText, self).__init__()
    db = pya.QFontDatabase()
    fonts = []
    for font in db.families():
      fonts.append([font, font])
    # declare the parameters
    self.param("l", self.TypeLayer, "Layer", default = pya.LayerInfo(1, 0))
    self.param("text", self.TypeString, "Text", default = "")
    self.param("f", self.TypeList, "Font", choices = fonts)
    self.param("w", self.TypeList, "Weight", default = 50, choices = [["Thin", 0], ["Extra light", 12], ["Light", 25], ["Normal", 50], ["Medium", 57], ["Demi Bold", 63], ["Bold", 75], ["Extra Bold", 81], ["Black", 87]])
    self.param("s", self.TypeList, "Style", default = 0, choices = [["Normal", 0], ["Italic", 1], ["Oblique", 2]])
    self.param("q", self.TypeInt, "Resolution", default = 20)

  def display_text_impl(self):
    return "Text(" + self.text + ")"
  
  def coerce_parameters_impl(self):
    pass  
    
  def can_create_from_shape_impl(self):
    return self.shape.is_text()
  
  def parameters_from_shape_impl(self):
    self.text = self.shape.text.string
    
  def transformation_from_shape_impl(self):
    return pya.Trans(self.shape.bbox().center())
  
  def produce_impl(self):
    dbu = self.layout.dbu
    path = pya.QPainterPath()
    font =  pya.QFont(self.f, self.q, self.w, False)
    if self.s == 0:
      font.setStyle(pya.QFont.StyleNormal)
    elif self.s == 1:
      font.setStyle(pya.QFont.StyleItalic)
    else:
      font.setStyle(pya.QFont.StyleOblique)
    path.addText(0, 0, font, self.text)
    polygons = path.toSubpathPolygons()
    # gen polygon data
    source = []
    for polygon in polygons:
      points = []
      for point in polygon:
        points.append(pya.Point.from_dpoint(pya.DPoint(point.x/dbu/self.q, -point.y/dbu/self.q)))
      source.append([points, []])
    # generate parent tree
    for polygon in source:
      for suspectedParent in source:
        if polygon != suspectedParent:
          inside = True
          for point in polygon[0]:
            if not pya.Polygon(suspectedParent[0]).inside(point):
              inside = False
          if inside:
            polygon[1].append(suspectedParent)
    # generate KLayout polygons
    outpoly = []
    i = 0
    while len(source):
      # find top
      for poly in source:
        if len(poly[1]) == 0:
          source.remove(poly)
          top = pya.Polygon(poly[0])
          break
      remove = []
      # add corresponding holes
      for polygon in source:
        if poly in polygon[1]:
          if len(polygon[1]) == 1:
            remove.append(polygon)
            top.insert_hole(polygon[0])
          polygon[1].remove(poly)
      for polygon in remove:
        source.remove(polygon)
      self.cell.shapes(self.l_layer).insert(top)