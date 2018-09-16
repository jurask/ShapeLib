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

class Cross(pya.PCellDeclarationHelper):

  def __init__(self):
    # Important: initialize the super class
    super(Cross, self).__init__()
    # declare the parameters
    self.param("l", self.TypeLayer, "Layer", default = pya.LayerInfo(1, 0))
    self.param("hh", self.TypeShape, "", default = pya.DPoint(10, 0.5))
    self.param("hv", self.TypeShape, "", default = pya.DPoint(0, 10))
    self.param("hb", self.TypeShape, "", default = pya.DPoint(20, 20))
    self.param("l1", self.TypeDouble, "Width", default = 10)
    self.param("l2", self.TypeDouble, "Height", default = 10)
    self.param("w", self.TypeDouble, "Line width", default = 1)
    self.param("inv", self.TypeBoolean, "Inverted", default = False)
    self.param("b1", self.TypeDouble, "Boundary width", default = 20)
    self.param("b2", self.TypeDouble, "Boundary height", default = 20)
    self.param("l1_", self.TypeDouble, "Width", default = 10, hidden = True)
    self.param("l2_", self.TypeDouble, "Height", default = 10, hidden = True)
    self.param("w_", self.TypeDouble, "Line width", default = 1, hidden = True)
    self.param("b1_", self.TypeDouble, "Boundary width", default = 20, hidden = True)
    self.param("b2_", self.TypeDouble, "Boundary height", default = 20, hidden = True)

  def display_text_impl(self):
    return "Cross(L1=" + str('%.1f' % self.l1) + ", L2=" + ('%.1f' % self.l2) + ", W=" + ('%.1f' % self.w) + ")"
  
  def coerce_parameters_impl(self):
    if self.l1 < 0:
      self.l1 *= -1
    if self.l2 < 0:
      self.l2 *= -1
    if self.b1 < 0:
      self.b1 *= -1
    if self.b2 < 0:
      self.b2 *= -1
    if self.w < 0:
      self.w *= -1
    if self.b1 < self.l1*2:
      self.b1 = self.l1*2
    if self.b2 < self.l2*2:
      self.b2 = self.l2*2
    if self.l1_ != self.l1 or self.l2_ != self.l2 or self.w_ != self.w or self.b1_ != self.b1 or self.b2_ != self.b2:
      # update handle
      self.hh = pya.DPoint(self.l1, self.w/2)
      self.hv = pya.DPoint(0, self.l2)
      self.hb = pya.DPoint(self.b1/2, self.b2/2)
      # fix params
      self.l1_ = self.l1
      self.l2_ = self.l2
      self.w_ = self.w
      self.b1_ = self.b1
      self.b2_ = self.b2
    else:
      # calc params from handle
      self.l1 = self.l1_ = abs(self.hh.x)
      self.l2 = self.l2_ = abs(self.hv.y)
      self.w = self.w_ = abs(self.hh.y*2)
      self.b1 = self.b1_ = abs(self.hb.x*2)
      self.b2 = self.b2_ = abs(self.hb.y*2)
  
  def can_create_from_shape_impl(self):
    return self.shape.is_box() or self.shape.is_polygon() or self.shape.is_path()
  
  def parameters_from_shape_impl(self):
    self.l1 = self.shape.bbox().width() * self.layout.dbu / 2
    self.l2 = self.shape.bbox().height() * self.layout.dbu / 2
    self.b1 = self.shape.bbox().width() * self.layout.dbu
    self.b2 = self.shape.bbox().height() * self.layout.dbu
    self.w = 1
    self.l = self.layout.get_info(self.layer)
  
  def transformation_from_shape_impl(self):
    return pya.Trans(self.shape.bbox().center())
  
  def produce_impl(self):
    dbu = self.layout.dbu
    cross = []
    cross.append(pya.Point.from_dpoint(pya.DPoint(self.w/(2*dbu), self.w/(2*dbu))))
    cross.append(pya.Point.from_dpoint(pya.DPoint(self.l1/dbu, self.w/(2*dbu))))
    cross.append(pya.Point.from_dpoint(pya.DPoint(self.l1/dbu, -self.w/(2*dbu))))
    cross.append(pya.Point.from_dpoint(pya.DPoint(self.w/(2*dbu), -self.w/(2*dbu))))
    cross.append(pya.Point.from_dpoint(pya.DPoint(self.w/(2*dbu), -self.l2/dbu)))
    cross.append(pya.Point.from_dpoint(pya.DPoint(-self.w/(2*dbu), -self.l2/dbu)))
    cross.append(pya.Point.from_dpoint(pya.DPoint(-self.w/(2*dbu), -self.w/(2*dbu))))
    cross.append(pya.Point.from_dpoint(pya.DPoint(-self.l1/dbu, -self.w/(2*dbu))))
    cross.append(pya.Point.from_dpoint(pya.DPoint(-self.l1/dbu, self.w/(2*dbu))))
    cross.append(pya.Point.from_dpoint(pya.DPoint(-self.w/(2*dbu), self.w/(2*dbu))))
    cross.append(pya.Point.from_dpoint(pya.DPoint(-self.w/(2*dbu), self.l2/dbu)))
    cross.append(pya.Point.from_dpoint(pya.DPoint(self.w/(2*dbu), self.l2/dbu)))
    if not self.inv:
      self.cell.shapes(self.l_layer).insert(pya.Polygon(cross))
    else:
      boundary = []
      boundary.append(pya.Point.from_dpoint(pya.DPoint(-self.b1/(2*dbu), -self.b2/(2*dbu))))
      boundary.append(pya.Point.from_dpoint(pya.DPoint(self.b1/(2*dbu), -self.b2/(2*dbu))))
      boundary.append(pya.Point.from_dpoint(pya.DPoint(self.b1/(2*dbu), self.b2/(2*dbu))))
      boundary.append(pya.Point.from_dpoint(pya.DPoint(-self.b1/(2*dbu), self.b2/(2*dbu))))
      poly = pya.Polygon(boundary)
      poly.insert_hole(cross)
      self.cell.shapes(self.l_layer).insert(poly)