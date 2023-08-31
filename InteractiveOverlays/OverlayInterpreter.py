import pygame

class Element:

    def __init__(self, name, image):
        self.Image:pygame.image
        self.Image = image
        self.Name  = name

        _mask = pygame.mask.from_surface(self.Image)
        self.Hitbox = _mask.get_bounding_rects()



class Overlay:

    def __init__(self):
        
        self._elements = {}
        self._elementHitboxes = {}
        """
        Dictionary
        Elements hitboxes as the keys,
        Elements as the values,

        an elements hitbox is a list containing pygame rectangles
        
        which defines the shape of an image
        """

    @property
    def Elements(self):
        return list(self._elements.keys())

    def appendElement(self, value):
        try:
            self._elementHitboxes[value.Hitbox] = value
            self._elements[value] = value.Hitbox
            return True
        except:
            return False
        
    def removeElement(self, value):
        try:
            del self._elementHitboxes[value.Hitbox]
            del self._elements[value]
            return True
        except:
            return False
        
    @property
    def ElementHitboxes(self):
        return list(self._elementHitboxes.keys())
        
    def IsElementAtPos(self, x, y):
        
        MouseRect = pygame.Rect(x, y, 1, 1)
        print(self.ElementHitboxes)
        collidedIndexes = MouseRect.collidelistall(self.ElementHitboxes)

        ElementsCollidedWith = []

        for index in collidedIndexes:
            ElementsCollidedWith.append(
                self._elementHitboxes[
                    self.ElementHitboxes[index]
                    ]
                )
        
        print(ElementsCollidedWith)




    
                

newOverlay = Overlay()
newElement = Element("test", pygame.image.load("test.png"))
print(newElement.Hitbox)
newOverlay.appendElement(newElement)

newOverlay.IsElementAtPos(1,1)

class OverlayFromFile:

    def __init__(self):
        pass