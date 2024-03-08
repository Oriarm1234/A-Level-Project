from .DropdownList import (
    DropdownList,init as DLInit
)
from .Slider import (
    Slider, init as SInit
)
from .TextInputBox import (
    TextInputBox, init as TIBInit
)
from .Tickbox import (
    Tickbox, init as TInit
)

def ExtraElementsInit(images):
    DLInit(images)
    SInit(images)
    TIBInit(images)
    TInit(images)