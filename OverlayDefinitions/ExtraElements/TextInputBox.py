from InteractiveOverlays import *
import time
import pygame


shiftKeys = {
    "1":"!",
    "2":"\"",
    "3":"£",
    "4":"$",
    "5":"%",
    "6":"^",
    "7":"&",
    "8":"*",
    "9":"(",
    "0":")",
    "[":"{",
    "]":"}",
    ";":":",
    "'":"@",
    ",":"<",
    ".":">",
    "/":"?",
    "#":"~",
    "-":"_",
    "=":"+",
    "`":"¬",
    "\\":"|",
}



def TextInputBoxPressed(self, *args, **kwargs):
    if self.canSelect:
        self.selected = not self.selected
        self.lastPressed = time.time()

def TextInputBoxPreUpdate(self, *args, **kwargs):
    events:list[pygame.event.Event]
    events = kwargs["events"]
    
    if self.selected:
        
        
        
        if self.pointerIndex >= len(self.Value):
            self.pointerIndex = len(self.Value)
        
        
        
        
        self.capslock = pygame.key.get_mods() & pygame.KMOD_CAPS
        for event in events:
            if "key" in dir(event):
                if event.type == pygame.KEYDOWN:
                    self.keys[event.key] = [1, time.time()]
                    
                        
                        
                elif event.type == pygame.KEYUP:
                    self.keys[event.key] = [0,0]
                    if event.key == 1073742049 or event.key == 1073742053:
                        self.holdingShift = False
        
        for key in self.keys:
            
            if ( self.keys[key][0] == 3 and\
                (time.time()-self.keys[key][1] > self.keyAllowedTime)) or\
                self.keys[key][0] == 1 or\
                self.keys[key][0] == 2 and time.time()-self.keys[key][1] > self.keyHeldDelay:
                    
                    if self.keys[key][0] != 0 and self.keys[key][0] != 3:
                        self.keys[key][0] +=1
                        
                        

                    
                    self.keys[key][1] = time.time()

                        
                
                    if key in range(32,127): ##PRINTABLE CHARACTERS
                        o=0
                        
                        if self.holdingShift or self.capslock:
                            if key in range(97, 123):
                                o = -32
                            elif chr(key) in shiftKeys and not self.capslock:
                                o = ord(shiftKeys[chr(key)]) - key
                                
                                    
                                        
                                        
                                        
                                        
                        if len(self.Value) < self.maxCharacterLimit:       
                        
                        
                            self.Value = self.Value[:self.pointerIndex] + chr(key + o) + self.Value[self.pointerIndex:]

                            if self.pointerMoves:
                                self.pointerIndex +=1
                    
                    elif key == 8: #BACKSPACE
                        if self.pointerIndex != 0:
                            self.Value = self.Value[:self.pointerIndex-1] + self.Value[self.pointerIndex:]
                        
                            if self.pointerMoves:
                                self.pointerIndex -=1
                    
                    elif key == 1073742049 or key == 1073742053:
                        self.holdingShift = True
                    
                    elif key == 27: #ESCAPE
                        self.pressed(self, *args, **kwargs)
                    
                    elif key == 1073741904:
                        self.setPointerIndex(self, max(self.pointerIndex-1, 0)) #LEFT ARROW 
                    
                    elif key == 1073741903:
                        self.setPointerIndex(self, min(self.pointerIndex+1,len(self.Value))) #RIGHT ARROW 
            
        
        
        
        
        if time.time() - self.timeSinceLastSwitch >= self.pointerTime:
            self.timeSinceLastSwitch = time.time()
            self.pointerVisible = not self.pointerVisible

                
    elif self.pointerVisible:
        self.pointerVisible = False
        
        
    
    
    
    if self.pointerIndex < self.visibleCharacterIndexBeginning:
        self.visibleCharacterIndexBeginning = self.pointerIndex
    if self.pointerIndex > self.visibleCharacterIndexBeginning + self.maxVisibleCharacterLimit:
        self.visibleCharacterIndexBeginning += self.pointerIndex - (self.visibleCharacterIndexBeginning + self.maxVisibleCharacterLimit)
    
    if len(self.Value)<(self.visibleCharacterIndexBeginning + self.maxVisibleCharacterLimit) and self.visibleCharacterIndexBeginning != 0:
        
        self.visibleCharacterIndexBeginning = max(0, len(self.Value)-self.maxVisibleCharacterLimit)
    
    
    self.TextBox.Text =  self.Value[self.visibleCharacterIndexBeginning:(self.visibleCharacterIndexBeginning + self.maxVisibleCharacterLimit)]
    

    if self.pointerVisible and not self.pointerForcedInvisible:
        pass
    
    self.TextBox.Text = " " *max(0,3- self.visibleCharacterIndexBeginning)+"." *min(3, self.visibleCharacterIndexBeginning) + self.TextBox.Text
    self.TextBox.Text += "."*min(3,max(0, len(self.Value)-(self.visibleCharacterIndexBeginning + self.maxVisibleCharacterLimit)))
    
    
    
    if self.Value == "":
        self.HoloTextBox.x = self.TextBox.x
        self.HoloTextBox.Text = "   " +  " |"[self.pointerVisible] +  self.HoloText
        self.HoloTextBox.align_to_bottom_right()
        
        
    elif self.Value != "":
        textWidth = self.TextBox.renderer(self.TextBox.Text[:self.pointerIndex+3]).get_rect().w
        self.HoloTextBox.x = self.TextBox.x + textWidth
        self.HoloTextBox.Text = "|" * (self.pointerVisible and not self.pointerForcedInvisible)
        self.HoloTextBox.align_to_bottom_middle()
    

def setPointerIndex(self, newIndex):
    if self.canMovePointer and self.pointerMoves:
        
        self.pointerIndex = newIndex
    
         
def otherElementPressed(self, *args, **kwargs):
    if self.selected:
        self.pressed(self)
        

def TextInputBox(Pos, BackgroundSize, BorderSize, TextSize, Font, Name, Parent, Padding, BackgroundColour, BorderColour, TextColour, HoloTextColour, DefaultText = "", HoloText = "Enter Text Here", maxCharacterLimit = 40, maxVisibleCharacterLimit=40, canMovePointer = True, pointerMoves=True):
    
    
    Border = Rectangle(Name+"-Border", Pos, (BackgroundSize[0]+BorderSize*2, BackgroundSize[1]+BorderSize*2), Parent, BorderColour, BorderSize)
    Background = Rectangle(Name+"-Background", (Pos[0]+BorderSize, Pos[1]+BorderSize), BackgroundSize, Parent, BackgroundColour)
    TextBox = Text(DefaultText, Font, TextSize, TextColour, (Pos[0] + Padding+BorderSize, Pos[1]+Padding+BorderSize), Name+"-Text", Parent)
    HoloTextBox = Text(HoloText, Font, TextSize, HoloTextColour, (Pos[0] + Padding+BorderSize, Pos[1]+Padding+BorderSize), Name+"-HoloText", Parent)
    
    self = Group(Name, Pos, Parent, [Border,Background,TextBox])
    self.selected = False
    self.Interactive = True
    self.lastPressed = time.time()
    self.pointerVisible = False
    self.pointerIndex = len(DefaultText) * pointerMoves
    self.pointerTime = 0.5
    self.timeSinceLastSwitch = time.time()
    self.holdingShift = False
    self.capslock = False
    self.canMovePointer = canMovePointer
    self.pointerMoves = pointerMoves
    self.maxVisibleCharacterLimit = maxVisibleCharacterLimit
    self.maxCharacterLimit = maxCharacterLimit
    self.visibleCharacterIndexBeginning = 0
    self.pointerForcedInvisible = False
    self.keys = {}
    self.keyAllowedTimer = time.time()
    self.keyAllowedTime = 0.05
    self.keyHeldDelay = 0.25
    self.canSelect = True
    
    self.Value = DefaultText
    self.HoloText = HoloText
    
    
    
    self.TextBox = TextBox
    self.HoloTextBox = HoloTextBox
    
    
    self.pressed = TextInputBoxPressed
    self.pre_update = TextInputBoxPreUpdate
    self.setPointerIndex = setPointerIndex
    self.other_element_pressed = otherElementPressed
    
    return self

