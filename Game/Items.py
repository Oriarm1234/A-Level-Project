class Item:
    amountGenerated = 0
    
    def __init__(self, name):
        self.name = name
        self.ID = Item.amountGenerated
        Item.amountGenerated+=1

class Key(Item):
    pass

class KeyPiece(Key):
    pass

key1 = KeyPiece("key1")
key2 = KeyPiece("key2")
key3 = KeyPiece("key3")

print(key1.ID,key2.ID,key3.ID)