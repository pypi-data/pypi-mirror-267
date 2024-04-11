from new_rep.new_rep.tty.tty_object import TTYObject

class TTY(TTYObject):
    def __init__(self, name_s: str, label_s: str, input_s: str, output_s: str):
        self.name = name_s
        self.label = label_s
        self.input = input_s
        self.output = output_s
        
        super().__init__()