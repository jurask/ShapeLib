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

class Arrow(pya.PCellDeclarationHelper):

  def __init__(self):
    # Important: initialize the super class
    super(Arrow, self).__init__()
    # declare the parameters
    self.param("l", self.TypeLayer, "Layer", default = pya.LayerInfo(1, 0))
    self.param("hb", self.TypeShape, "", default = pya.DPoint(0.5, -6))
    self.param("hh", self.TypeShape, "", default = pya.DPoint(0, 4))
    self.param("ha", self.TypeShape, "", default = pya.DPoint(2.2314069574087765, 0))
    self.param("b", self.TypeDouble, "Body length", default = 6)
    self.param("h", self.TypeDouble, "Head length", default = 4)
    self.param("a", self.TypeDouble, "Head angle", default = 45)
    self.param("w", self.TypeDouble, "Body width", default = 1)
    self.param("b_", self.TypeDouble, "Body length", default = 6, hidden = True)
    self.param("h_", self.TypeDouble, "Head length", default = 4, hidden = True)
    self.param("a_", self.TypeDouble, "Head angle", default = 45, hidden = True)
    self.param("w_", self.TypeDouble, "Body width", default = 1, hidden = True)

  def display_text_impl(self):
    return "Arrow(B=" + str('%.1f' % self.b) + ", H=" + ('%.1f' % self.h) + ", A=" + ('%.1f' % self.a) + ")"
  
  def coerce_parameters_impl(self):
    if self.b < 0:
      self.b *= -1
    if self.h < 0:
      self.h *= -1
    if self.a < 0:
      self.a *= -1
    if self.w < 0:
      self.w *= -1
    if self.b_ != self.b or self.h_ != self.h or self.w_ != self.w or self.a_ != self.a:
      # update handle
      self.hh = pya.DPoint(0, self.h)
      self.hb = pya.DPoint(self.w/2, -self.b)
      self.ha = pya.DPoint(self.h*math.tan(math.radians(self.a/2)), 0)
      # fix params
      self.b_ = self.b
      self.w_ = self.w
      self.a_ = self.a
      self.h_ = self.h
    else:
      # fix angle handle
      self.ha.y = 0
      self.hh.x = 0
      # calc params from handle
      self.b = self.b_ = abs(self.hb.y)
      self.w = self.w_ = 2 * abs(self.hb.x)
      self.h = self.h_ = abs(self.hh.y)
      self.a = self.a_ = math.degrees(2 * math.atan(abs(self.ha.x)/self.h))
  
  def can_create_from_shape_impl(self):
    return self.shape.is_box() or self.shape.is_polygon() or self.shape.is_path()
  
  def parameters_from_shape_impl(self):
    w = self.shape.bbox().width()*self.layout.dbu
    h = self.shape.bbox().height()*self.layout.dbu
    if w > h:
      w, h = h, w
    self.b = 3*h/5
    self.h = 2*h/5
    self.a = math.degrees(2*math.atan(5/4*w/h))
    self.w = w/5
    self.l = self.layout.get_info(self.layer)
  
  def transformation_from_shape_impl(self):
    w = self.shape.bbox().width()
    h = self.shape.bbox().height()
    if w > h:
      return pya.Trans(3, False, pya.Point(self.shape.bbox().center().x+0.1*w, self.shape.bbox().center().y))
    else:
      return pya.Trans(pya.Point(self.shape.bbox().center().x, self.shape.bbox().center().y+0.1*h))
  
  def produce_impl(self):
    dbu = self.layout.dbu
    arrow = []
    tg = math.tan(math.radians(self.a/2))
    hw = self.h * tg
    arrow.append(pya.Point.from_dpoint(pya.DPoint(self.w/(2*dbu), -self.b/dbu)))
    arrow.append(pya.Point.from_dpoint(pya.DPoint(self.w/(2*dbu), 0)))
    arrow.append(pya.Point.from_dpoint(pya.DPoint(hw/dbu, 0)))
    arrow.append(pya.Point.from_dpoint(pya.DPoint(0, self.h/dbu)))
    arrow.append(pya.Point.from_dpoint(pya.DPoint(-hw/dbu, 0)))
    arrow.append(pya.Point.from_dpoint(pya.DPoint(-self.w/(2*dbu), 0)))
    arrow.append(pya.Point.from_dpoint(pya.DPoint(-self.w/(2*dbu), -self.b/dbu)))
    self.cell.shapes(self.l_layer).insert(pya.Polygon(arrow))