



class TTYObject(object):
    
    def __init__(self) -> None:
        pass

    def __str_dict_items(self) -> str:
        return ', '.join([f'{a}={v}' for a, v in self.__dict__.items()])

    def __str__(self) -> str:
        return f'{self.__class__.__name__}({self.__str_dict_items()})'
    
    def __repr__(self) -> str:
        return self.__str__()
    

class TTY(TTYObject):
    def __init__(self, name_s: str, label_s: str, input_s: str, output_s: str):
        self.name = name_s
        self.label = label_s
        self.input = input_s
        self.output = output_s
        
        super().__init__()