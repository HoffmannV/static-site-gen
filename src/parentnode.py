from htmlnode import HTMLNode

class ParentNode(HTMLNode):
    def __init__(self, children, tag=None, props=None):
        super().__init__(children=children, tag=tag, props=props)

    def to_html(self):
        if not self.tag:
            raise ValueError("The node has to have a tag")
        if not self.children:
            raise ValueError("The node cannot have no children")
        
        html_element = ""
        #if self.children == None:
        #    return self.enclose_element_in_tag(html_element)
        #else:

        for child in self.children:
#            print(child)
            html_element += child.to_html()

        return self.enclose_element_in_tag(html_element)

