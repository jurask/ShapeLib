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

class Star(pya.PCellDeclarationHelper):

  def __init__(self):
    # Important: initialize the super class
    super(Star, self).__init__()
    # declare the parameters
    self.param("l", self.TypeLayer, "Layer", default = pya.LayerInfo(1, 0))
    self.param("hi", self.TypeShape, "", default = pya.DPoint(5, 0))
    self.param("ho", self.TypeShape, "", default = pya.DPoint(10, 0))
    self.param("ri", self.TypeDouble, "Inner radius", default = 5)
    self.param("ro", self.TypeDouble, "Outer radius", default = 10)
    self.param("n", self.TypeInt, "Number of corners", default = 8)
    self.param("ri_", self.TypeDouble, "Inner radius", default = 5, hidden = True)
    self.param("ro_", self.TypeDouble, "Outer radius", default = 10, hidden = True)

  def display_text_impl(self):
    return "Star(Ri=" + str('%.1f' % self.ri) + ", Ro=" + ('%.1f' % self.ro) + ", N=" + ('%.1f' % self.n) + ")"
  
  def coerce_parameters_impl(self):
    if self.n < 3:
      self.n = 3
    if self.ri < 0:
      self.ri *= -1
    if self.ro < 0:
      self.ro *= -1
    if self.ri_ != self.ri or self.ro_ != self.ro:
      # update handle
      self.hi = pya.DPoint(self.ri, 0)
      self.ho = pya.DPoint(self.ro, 0)
      # fix params
      self.ri_ = self.ri
      self.ro_ = self.ro
    else:
      # calc params from handle
      self.ri = self.ri_ = math.sqrt(abs(self.hi.x)**2+abs(self.hi.y)**2)
      self.ro = self.ro_ = math.sqrt(abs(self.ho.x)**2+abs(self.ho.y)**2)
  
  def can_create_from_shape_impl(self):
    return self.shape.is_box() or self.shape.is_polygon() or self.shape.is_path()
  
  def parameters_from_shape_impl(self):
    self.ro = self.shape.bbox().width() * self.layout.dbu / 2
    self.ri = self.ro/2
    self.n = 8
    self.l = self.layout.get_info(self.layer)
  
  def transformation_from_shape_impl(self):
    return pya.Trans(self.shape.bbox().center())
  
  def produce_impl(self):
    dbu = self.layout.dbu
    star = []
    anglestep = math.radians(360/self.n)
    for i in range(self.n):
      angle = i*anglestep
      x = self.ri*math.cos(angle)
      y = self.ri*math.sin(angle)
      star.append(pya.Point.from_dpoint(pya.DPoint(x/dbu, y/dbu)))
      x = self.ro*math.cos(angle+anglestep/2)
      y = self.ro*math.sin(angle+anglestep/2)
      star.append(pya.Point.from_dpoint(pya.DPoint(x/dbu, y/dbu)))
    self.cell.shapes(self.l_layer).insert(pya.Polygon(star))