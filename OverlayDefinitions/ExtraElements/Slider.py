from InteractiveOverlays import *
from pygame.image import load as loadImage

def Slider(Pos, name, parent, minVal = 0.0, MaxVal = 1.0, roundNDigits = 2):
    r = Rectangle("background", (530,300), (420,21), None, (100,100,100))
    l = Line("line", (330, 299), (730, 299), None, (0,0,0), 4)
    c = Circle("circle", (330,300), None, (80,80,80),4, 8)
    t = Text(str(minVal), "Calibri", 16, (0,0,0), (950, 300), "sliderText", None)
    r.align_to_center()
    c.align_to_center()
    t.align_to_middle_right()
    t.x = r.x + r.hitbox.w
    slider = Group("Slider", (0,0), None, (r,l,c,t))
    slider.percent = 0
    slider.roundNDigits = roundNDigits

    def slider_pressed(self, *args, **kwargs):
        mousePos = args[0]
        element = self._elements.get("circle", None)
        line = self._elements.get("line", None)
        text = self._elements.get("sliderText", None)
        if element is not None and line is not None:
            element.x = max(min(mousePos[0], line.endX), line.x)
            
            self.percent =(element._x-line._x) / (line._endX-line._x)

            if text is not None:
                
                text.text = str(self.get_value(self))
                slider.value = self.get_value(self)
                
    def get_value(self, *args, **kwargs):
        return round(minVal + self.percent * (MaxVal-minVal),self.roundNDigits)
    
    def set_value(self, value, *args, **kwargs):
        percent = round((value-minVal) / (MaxVal-minVal),self.roundNDigits)
        self.set_percent(self, percent)
        
    def get_percent(self, *args, **kwargs):
        return self.percent

    def set_percent(self, percent, *args, **kwargs):
        
        element = self._elements.get("circle", None)
        line = self._elements.get("line", None)
        text = self._elements.get("sliderText", None)
        if element is not None and line is not None:
            element.x = line._x + max(min(percent, 1), 0) * (line._endX-line._x)
            
            slider.percent =(element._x-line._x) / (line._endX-line._x)

            if text is not None:
                
                text.text = str(self.get_value(self))
                slider.value = self.get_value(self)
            

        
    slider.pressed = slider_pressed
    slider.held_down = slider_pressed
    slider._interactive = True
    slider.get_percent = get_percent
    slider.set_percent = set_percent
    slider.get_value = get_value
    slider.set_value = set_value
    slider.x, slider.y = Pos
    slider.name = name
    slider.parent = parent
    slider.value = slider.get_value(slider)
    
    return slider
    
    #for elementName in slider._elements:

arrowImage = loadImage("Images\\dropdownarrow.png")