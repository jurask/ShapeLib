import pya

class CrossPadsExt(pya.PCellDeclarationHelper):

  def __init__(self):
    # Important: initialize the super class
    super(CrossPadsExt, self).__init__()
    # declare the parameters
    self.param("l", self.TypeLayer, "Layer", default = pya.LayerInfo(1, 0))
    self.param("cp", self.TypeShape, "", default = pya.DPoint(10, 0.5))
    self.param("pp", self.TypeShape, "", default = pya.DPoint(20, 1))
    self.param("bp", self.TypeShape, "", default = pya.DPoint(20, 20))
    self.param("ep", self.TypeShape, "", default = pya.DPoint(30, 0.5))
    self.param("cl", self.TypeDouble, "Cross length", default = 10)
    self.param("pl", self.TypeDouble, "Pad length", default = 10)
    self.param("el", self.TypeDouble, "Extension length", default = 10)
    self.param("cw", self.TypeDouble, "Cross width", default = 1)
    self.param("pw", self.TypeDouble, "Pad width", default = 2)
    self.param("inv", self.TypeBoolean, "Inverted", default = False)
    self.param("b1", self.TypeDouble, "Boundary width", default = 20)
    self.param("b2", self.TypeDouble, "Boundary height", default = 20)
    self.param("cl_", self.TypeDouble, "Cross length", default = 10, hidden = True)
    self.param("pl_", self.TypeDouble, "Pad length", default = 10, hidden = True)
    self.param("el_", self.TypeDouble, "Extension length", default = 10, hidden = True)
    self.param("cw_", self.TypeDouble, "Cross width", default = 1, hidden = True)
    self.param("pw_", self.TypeDouble, "Pad width", default = 2, hidden = True)
    self.param("b1_", self.TypeDouble, "Boundary width", default = 20, hidden = True)
    self.param("b2_", self.TypeDouble, "Boundary height", default = 20, hidden = True)

  def display_text_impl(self):
    return "PaddedCrossExt(L={}, PL={}, EL={}, W={}, PW={})".format(self.cl, self.pl, self.el, self.cw, self.pw)
  
  def coerce_parameters_impl(self):
    if self.cl < 0:
      self.cl *= -1
    if self.pl < 0:
      self.pl *= -1
    if self.el < 0:
      self.el *= -1
    if self.cw < 0:
      self.cw *= -1
    if self.pw < 0:
      self.pw *= -1
    if self.b1 < self.cl*2+self.pl*2+self.el*2:
      self.b1 = self.cl*2+self.pl*2+self.el*2
    if self.b2 < self.cl*2+self.pl*2+self.el*2:
      self.b2 = self.cl*2+self.pl*2+self.el*2
    if self.cl_ != self.cl or self.pl_ != self.pl or self.el != self.el_ or self.cw_ != self.cw or self.pw_ != self.pw or self.b1_ != self.b1 or self.b2_ != self.b2:
      # update handle
      self.pp = pya.DPoint(self.pl+self.cl, self.pw/2)
      self.cp = pya.DPoint(self.cl, self.cw/2)
      self.ep = pya.DPoint(self.pl+self.cl+self.el, self.cw/2)
      self.bp = pya.DPoint(self.b1/2, self.b2/2)
      # fix params
      self.cl_ = self.cl
      self.pl_ = self.pl
      self.el_ = self.el
      self.cw_ = self.cw
      self.pw_ = self.pw
      self.b1_ = self.b1
      self.b2_ = self.b2
    else:
      # calc params from handle
      self.cl = self.cl_ = abs(self.cp.x)
      self.cw = self.cw_ = abs(self.cp.y*2)
      self.pl = self.pl_ = abs(self.pp.x) - self.cl
      self.pw = self.pw_ = abs(self.pp.y*2)
      self.el = self.el_ = abs(self.ep.x) - self.cl - self.pl
      self.b1 = self.b1_ = abs(self.bp.x*2)
      self.b2 = self.b2_ = abs(self.bp.y*2)
  
  def can_create_from_shape_impl(self):
    return self.shape.is_box() or self.shape.is_polygon() or self.shape.is_path()
  
  def parameters_from_shape_impl(self):
    self.pl = self.cl = self.shape.bbox().width() * self.layout.dbu / 4
    self.b1 = self.shape.bbox().width() * self.layout.dbu
    self.b2 = self.shape.bbox().height() * self.layout.dbu
    if self.shape.bbox().width() < self.shape.bbox().height():
      self.cw = self.shape.bbox().width() * self.layout.dbu / 10
      self.pw = self.shape.bbox().width() * self.layout.dbu / 5
    else:
      self.cw = self.shape.bbox().height() * self.layout.dbu / 10
      self.pw = self.shape.bbox().height() * self.layout.dbu / 5
    self.l = self.layout.get_info(self.layer)
  
  def transformation_from_shape_impl(self):
    return pya.Trans(self.shape.bbox().center())
  
  def produce_impl(self):
    dbu = self.layout.dbu
    cross = []
    # top
    cross.append(pya.Point.from_dpoint(pya.DPoint(self.cw/(2*dbu), self.cw/(2*dbu))))
    cross.append(pya.Point.from_dpoint(pya.DPoint(self.cw/(2*dbu), self.cl/dbu)))
    cross.append(pya.Point.from_dpoint(pya.DPoint(self.pw/(2*dbu), self.cl/dbu)))
    cross.append(pya.Point.from_dpoint(pya.DPoint(self.pw/(2*dbu), (self.cl+self.pl)/dbu)))
    cross.append(pya.Point.from_dpoint(pya.DPoint(self.cw/(2*dbu), (self.cl+self.pl)/dbu)))
    cross.append(pya.Point.from_dpoint(pya.DPoint(self.cw/(2*dbu), (self.cl+self.pl+self.el)/dbu)))
    cross.append(pya.Point.from_dpoint(pya.DPoint(-self.cw/(2*dbu), (self.cl+self.pl+self.el)/dbu)))
    cross.append(pya.Point.from_dpoint(pya.DPoint(-self.cw/(2*dbu), (self.cl+self.pl)/dbu)))
    cross.append(pya.Point.from_dpoint(pya.DPoint(-self.pw/(2*dbu), (self.cl+self.pl)/dbu)))
    cross.append(pya.Point.from_dpoint(pya.DPoint(-self.pw/(2*dbu), self.cl/dbu)))
    cross.append(pya.Point.from_dpoint(pya.DPoint(-self.cw/(2*dbu), self.cl/dbu)))
    # left
    cross.append(pya.Point.from_dpoint(pya.DPoint(-self.cw/(2*dbu), self.cw/(2*dbu))))
    cross.append(pya.Point.from_dpoint(pya.DPoint(-self.cl/dbu, self.cw/(2*dbu))))
    cross.append(pya.Point.from_dpoint(pya.DPoint(-self.cl/dbu, self.pw/(2*dbu))))
    cross.append(pya.Point.from_dpoint(pya.DPoint(-(self.cl+self.pl)/dbu, self.pw/(2*dbu))))
    cross.append(pya.Point.from_dpoint(pya.DPoint(-(self.cl+self.pl)/dbu, self.cw/(2*dbu))))
    cross.append(pya.Point.from_dpoint(pya.DPoint(-(self.cl+self.pl+self.el)/dbu, self.cw/(2*dbu))))
    cross.append(pya.Point.from_dpoint(pya.DPoint(-(self.cl+self.pl+self.el)/dbu, -self.cw/(2*dbu))))
    cross.append(pya.Point.from_dpoint(pya.DPoint(-(self.cl+self.pl)/dbu, -self.cw/(2*dbu))))
    cross.append(pya.Point.from_dpoint(pya.DPoint(-(self.cl+self.pl)/dbu, -self.pw/(2*dbu))))
    cross.append(pya.Point.from_dpoint(pya.DPoint(-self.cl/dbu, -self.pw/(2*dbu))))
    cross.append(pya.Point.from_dpoint(pya.DPoint(-self.cl/dbu, -self.cw/(2*dbu))))
    # bottom
    cross.append(pya.Point.from_dpoint(pya.DPoint(-self.cw/(2*dbu), -self.cw/(2*dbu))))
    cross.append(pya.Point.from_dpoint(pya.DPoint(-self.cw/(2*dbu), -self.cl/dbu)))
    cross.append(pya.Point.from_dpoint(pya.DPoint(-self.pw/(2*dbu), -self.cl/dbu)))
    cross.append(pya.Point.from_dpoint(pya.DPoint(-self.pw/(2*dbu), -(self.cl+self.pl)/dbu)))
    cross.append(pya.Point.from_dpoint(pya.DPoint(-self.cw/(2*dbu), -(self.cl+self.pl)/dbu)))
    cross.append(pya.Point.from_dpoint(pya.DPoint(-self.cw/(2*dbu), -(self.cl+self.pl+self.el)/dbu)))
    cross.append(pya.Point.from_dpoint(pya.DPoint(self.cw/(2*dbu), -(self.cl+self.pl+self.el)/dbu)))
    cross.append(pya.Point.from_dpoint(pya.DPoint(self.cw/(2*dbu), -(self.cl+self.pl)/dbu)))
    cross.append(pya.Point.from_dpoint(pya.DPoint(self.pw/(2*dbu), -(self.cl+self.pl)/dbu)))
    cross.append(pya.Point.from_dpoint(pya.DPoint(self.pw/(2*dbu), -self.cl/dbu)))
    cross.append(pya.Point.from_dpoint(pya.DPoint(self.cw/(2*dbu), -self.cl/dbu)))
    # right
    cross.append(pya.Point.from_dpoint(pya.DPoint(self.cw/(2*dbu), -self.cw/(2*dbu))))
    cross.append(pya.Point.from_dpoint(pya.DPoint(self.cl/dbu, -self.cw/(2*dbu))))
    cross.append(pya.Point.from_dpoint(pya.DPoint(self.cl/dbu, -self.pw/(2*dbu))))
    cross.append(pya.Point.from_dpoint(pya.DPoint((self.cl+self.pl)/dbu, -self.pw/(2*dbu))))
    cross.append(pya.Point.from_dpoint(pya.DPoint((self.cl+self.pl)/dbu, -self.cw/(2*dbu))))
    cross.append(pya.Point.from_dpoint(pya.DPoint((self.cl+self.pl+self.el)/dbu, -self.cw/(2*dbu))))
    cross.append(pya.Point.from_dpoint(pya.DPoint((self.cl+self.pl+self.el)/dbu, self.cw/(2*dbu))))
    cross.append(pya.Point.from_dpoint(pya.DPoint((self.cl+self.pl)/dbu, self.cw/(2*dbu))))
    cross.append(pya.Point.from_dpoint(pya.DPoint((self.cl+self.pl)/dbu, self.pw/(2*dbu))))
    cross.append(pya.Point.from_dpoint(pya.DPoint(self.cl/dbu, self.pw/(2*dbu))))
    cross.append(pya.Point.from_dpoint(pya.DPoint(self.cl/dbu, self.cw/(2*dbu))))
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