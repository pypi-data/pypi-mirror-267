class TTYObject(object):
    
    def __init__(self) -> None:
        pass

    def __str_dict_items(self) -> str:
        return ', '.join([f'{a}={v}' for a, v in self.__dict__.items()])

    def __str__(self) -> str:
        return f'{self.__class__.__name__}({self.__str_dict_items()})'
    
    def __repr__(self) -> str:
        return self.__str__()