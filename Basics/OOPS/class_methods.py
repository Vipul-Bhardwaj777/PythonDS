class ChaiOrder:

    def __init__(self, tea_type, sweetness, size):
        self.tea_type = tea_type
        self.sweetness = sweetness
        self.size = size

    @classmethod
    def from_dic(cls, dictionary):
        return cls(dictionary['tea_type'],dictionary['sweetness'],dictionary['size'])
    
    @classmethod
    def from_string(cls, str):
        tea_type, sweetness, size = str.split('-')
        
        return cls(tea_type, sweetness, size)
    
order1 = ChaiOrder.from_dic({})
order2 = ChaiOrder.from_string('')