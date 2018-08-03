import math
import pya

class Bowtie(pya.PCellDeclarationHelper):


  def __init__(self):

    # Important: initialize the super class
    super(Bowtie, self).__init__()

    # declare the parameters
    self.param("l", self.TypeLayer, "Layer", default = pya.LayerInfo(1, 0))
    self.param("lb", self.TypeDouble, "Bridge length", default = 0.1)
    self.param("wb", self.TypeDouble, "Bridge width", default = 0.1)
    self.param("lw", self.TypeDouble, "Wing length", default = 0.1)
    self.param("a", self.TypeDouble, "Wing angle", default = 45)

  def display_text_impl(self):
    # Provide a descriptive text for the cell
    return "Bowtie(lb=" + str('%.3f' % self.lb) + ",wb=" + ('%.3f' % self.wb) +  ",lw=" + ('%.3f' % self.lw) + ",angle=" + ('%.3f' % self.a) +")"
  
  def coerce_parameters_impl(self):
  
    # We employ coerce_parameters_impl to decide whether the handle or the 
    # numeric parameter has changed (by comparing against the effective 
    # radius ru) and set ru to the effective radius. We also update the 
    # numerical value or the shape, depending on which on has not changed.
    pass
  
  def can_create_from_shape_impl(self):
    # Implement the "Create PCell from shape" protocol: we can use any shape which 
    # has a finite bounding box
    return False
  
  def parameters_from_shape_impl(self):
    # Implement the "Create PCell from shape" protocol: we set r and l from the shape's 
    # bounding box width and layer
    return None
  
  def transformation_from_shape_impl(self):
    # Implement the "Create PCell from shape" protocol: we use the center of the shape's
    # bounding box to determine the transformation
    return pya.Trans(self.shape.bbox().center())
  
  def produce_impl(self):
  
    # This is the main part of the implementation: create the layout

    # fetch the parameters
    dbu = self.layout.dbu
    tg = math.tan(math.radians(self.a/2))
    
    # compute the circle
    pts = []
    pts.append(pya.Point(pya.DPoint((-self.lb/2)/dbu, (self.wb/2)/dbu)))
    pts.append(pya.Point(pya.DPoint((-self.lb/2-self.lw)/dbu, (self.wb/2+self.lw*tg)/dbu)))
    pts.append(pya.Point(pya.DPoint((-self.lb/2-self.lw)/dbu, (-self.wb/2-self.lw*tg)/dbu)))
    pts.append(pya.Point(pya.DPoint((-self.lb/2)/dbu, -(self.wb/2)/dbu)))
    self.cell.shapes(self.l_layer).insert(pya.Polygon(pts))
    pts = []
    pts.append(pya.Point(pya.DPoint((self.lb/2)/dbu, -(self.wb/2)/dbu)))
    pts.append(pya.Point(pya.DPoint((self.lb/2+self.lw)/dbu, (-self.wb/2-self.lw*tg)/dbu)))
    pts.append(pya.Point(pya.DPoint((self.lb/2+self.lw)/dbu, (self.wb/2+self.lw*tg)/dbu)))
    pts.append(pya.Point(pya.DPoint((self.lb/2)/dbu, (self.wb/2)/dbu)))
    self.cell.shapes(self.l_layer).insert(pya.Polygon(pts))