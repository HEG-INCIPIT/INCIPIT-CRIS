array_ark = ["ark:/68061/g24w2n", "ark:/68061/g24w2a", "ark:/68061/g24w2b", "ark:/68061/g24w2c"]

class Ark:
    def __init__(self):
        self.ark = array_ark[0]
        if(len(array_ark)>0):
            array_ark.pop(0)

    def ark_creation(self):
        return self.ark
