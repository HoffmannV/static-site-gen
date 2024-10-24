

class HTMLNode():
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props
    
    def to_html(self):
        raise NotImplementedError()

    def props_to_html(self):
        return_value = ""

        if self.props:
            for prop in self.props:
                return_value += f"{prop}=\"{self.props[prop]}\" "

        return return_value.strip()
    
    def __repr__(self):
        return f"Tag: {self.tag}\nValue: {self.value}\nChildren: {self.children}\nProperties: {self.props}"
