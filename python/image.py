import pya
import math

class Image(pya.PCellDeclarationHelper):

  def __init__(self):
    # Important: initialize the super class
    super(Image, self).__init__()
    # declare the parameters
    self.param("l", self.TypeLayer, "Layer", default = pya.LayerInfo(1, 0))
    self.param("path", self.TypeString, "Path", default = "")
    self.param("px", self.TypeDouble, "Pixel size", default = 1)
    self.param("t", self.TypeInt, "Tile size", default = 10)
    self.param("th", self.TypeInt, "Threshold", default = 127)
    self.param("inv", self.TypeBoolean, "Inverted", default = False)
    self.error = None

  def display_text_impl(self):
    if not self.error:
      return "Image(" + self.path + ")"
    else:
      return "Image(" + self.error + ")"
  
  def coerce_parameters_impl(self):
    pass  
    
  def can_create_from_shape_impl(self):
    return False
  
  def parameters_from_shape_impl(self):
    pass
    
  def transformation_from_shape_impl(self):
    pass
  
  def produce_impl(self):
    dbu = self.layout.dbu
    # resolve path
    info = pya.QFileInfo(self.path)
    if info.isRelative():
      view = pya.Application.instance().main_window().current_view()
      designfile = view.active_cellview().filename()
      if designfile == "":
        self.error = "Error: In order to use relative file path, design must be saved first"
        return
      designdir = pya.QFileInfo(designfile).dir()
      path = designdir.absoluteFilePath(self.path)
    else:
      path = self.path
    # open image
    image = pya.QImage(path)
    if image.isNull():
      self.error = "Error opening image"
      return
    image = image.convertToFormat(pya.QImage.Format_Grayscale8)
    width = image.width()
    height = image.height()
    tilesx = math.ceil(width/self.t)
    tilesy = math.ceil(height/self.t)
    for tiley in range(tilesy):
      for tilex in range(tilesx):
        tile = image.copy(tilex*self.t, tiley*self.t, self.t, self.t)
        polygons = []
        # generate pixels
        for y in range(self.t):
          for x in range(self.t):
            color = pya.QColor(tile.pixel(x, y))
            color = (color.red+color.green+color.blue)/3
            if (color > self.th and not self.inv) or (color <= self.th and self.inv):
              x1 = (tilex*self.t+x)*self.px/dbu
              y1 = -(tiley*self.t+y)*self.px/dbu
              x2 = (tilex*self.t+x+1)*self.px/dbu
              y2 = -(tiley*self.t+y+1)*self.px/dbu
              polygons.append(pya.Polygon(pya.Box(pya.Point.from_dpoint(pya.DPoint(x1, y1)), pya.Point.from_dpoint(pya.DPoint(x2, y2)))))
        # merge
        processor = pya.EdgeProcessor()
        merged = processor.simple_merge_p2p(polygons, False, False)
        for polygon in merged:
          self.cell.shapes(self.l_layer).insert(polygon)
    self.error = None