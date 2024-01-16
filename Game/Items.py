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

key1 = keyPiece("key1")
key2 = keyPiece("key2")
key3 = keyPiece("key3")

print(key1.ID,key2.ID,key3.ID)