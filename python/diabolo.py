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

import math
import pya

class Diabolo(pya.PCellDeclarationHelper):


  def __init__(self):

    # Important: initialize the super class
    super(Diabolo, self).__init__()

    # declare the parameters
    self.param("l", self.TypeLayer, "Layer", default = pya.LayerInfo(1, 0))
    self.param("lb", self.TypeDouble, "Bridge length", default = 0.1)
    self.param("wb", self.TypeDouble, "Bridge width", default = 0.1)
    self.param("lw", self.TypeDouble, "Wing length", default = 0.1)
    self.param("a", self.TypeDouble, "Wing angle", default = 45)
    self.param("hb", self.TypeShape, "", default = pya.DPoint(0.05, 0.05))
    self.param("hw", self.TypeShape, "", default = pya.DPoint(0.15, 0.09142135623730951))
    self.param("lb_", self.TypeDouble, "Bridge length", default = 0.1, hidden = True)
    self.param("wb_", self.TypeDouble, "Bridge width", default = 0.1, hidden = True)
    self.param("lw_", self.TypeDouble, "Wing length", default = 0.1, hidden = True)
    self.param("a_", self.TypeDouble, "Wing angle", default = 45, hidden = True)

  def display_text_impl(self):
    # Provide a descriptive text for the cell
    return "Diabolo(lb=" + str('%.3f' % self.lb) + ",wb=" + ('%.3f' % self.wb) +  ",lw=" + ('%.3f' % self.lw) + ",angle=" + ('%.3f' % self.a) +")"
  
  def coerce_parameters_impl(self):
    if self.lb < 0:
      self.lb *= -1
    if self.wb < 0:
      self.wb *= -1
    if self.lw < 0:
      self.lw *= -1
    if self.lb != self.lb_ or self.wb != self.wb_ or self.lw != self.lw_ or self.a != self.a_:
      # update handle
      hbx = self.lb/2
      hby = self.wb/2
      hwx = hbx + self.lw
      hwy = hby + self.lw * math.tan(math.radians(self.a/2))
      self.hb = pya.DPoint(hbx, hby)
      self.hw = pya.DPoint(hwx, hwy)
      # fix params
      self.lb_ = self.lb
      self.wb_ = self.wb
      self.lw_ = self.lw
      self.a_ = self.a
    else:
      # calc params from handle
      hbx = abs(self.hb.x)
      hby = abs(self.hb.y)
      hwx = abs(self.hw.x)
      hwy = abs(self.hw.y)
      self.lb = self.lb_ = hbx * 2
      self.wb = self.wb_ = hby * 2
      self.lw = self.lw_ = hwx - hbx
      self.a = self.a_ = 2 * math.degrees(math.atan((hwy - hby)/self.lw))
  
  def can_create_from_shape_impl(self):
    return False
  
  def parameters_from_shape_impl(self):
    return None
  
  def transformation_from_shape_impl(self):
    return pya.Trans(self.shape.bbox().center())
  
  def produce_impl(self):
  
    # This is the main part of the implementation: create the layout

    # fetch the parameters
    dbu = self.layout.dbu
    tg = math.tan(math.radians(self.a/2))
    
    # compute the diabolo
    pts = []
    pts.append(pya.Point(pya.DPoint((-self.lb/2)/dbu, (self.wb/2)/dbu)))
    pts.append(pya.Point(pya.DPoint((-self.lb/2-self.lw)/dbu, (self.wb/2+self.lw*tg)/dbu)))
    pts.append(pya.Point(pya.DPoint((-self.lb/2-self.lw)/dbu, (-self.wb/2-self.lw*tg)/dbu)))
    pts.append(pya.Point(pya.DPoint((-self.lb/2)/dbu, -(self.wb/2)/dbu)))
    pts.append(pya.Point(pya.DPoint((self.lb/2)/dbu, -(self.wb/2)/dbu)))
    pts.append(pya.Point(pya.DPoint((self.lb/2+self.lw)/dbu, (-self.wb/2-self.lw*tg)/dbu)))
    pts.append(pya.Point(pya.DPoint((self.lb/2+self.lw)/dbu, (self.wb/2+self.lw*tg)/dbu)))
    pts.append(pya.Point(pya.DPoint((self.lb/2)/dbu, (self.wb/2)/dbu)))
    
    # create the shape
    self.cell.shapes(self.l_layer).insert(pya.Polygon(pts))