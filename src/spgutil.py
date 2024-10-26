from textnode import TextType, TextNode
from leafnode import LeafNode

def text_node_to_html_node(text_node):
    match(text_node.text_type):
        case(TextType.NORMAL):
            return LeafNode(text_node.text)
        case(TextType.BOLD):
            return LeafNode(text_node.text, "b")
        case(TextType.ITALIC):
            return LeafNode(text_node.text, "i")
        case(TextType.IMAGE):
            return LeafNode(value="", tag="img", props={"src": text_node.url, "alt": text_node.text})
        case(TextType.LINK):
            return LeafNode(value=text_node.text, tag="a", props={"href": text_node.url})
        case _:
            raise Exception("Whoops something went wrong!")

def split_nodes_delimiter(text_node, delimiter, text_type):
    text_node_list = list()

    for node in text_node:
        if len(node.text.split(delimiter)) % 2 == 0:
            raise ValueError("Invalid markdown, formatted section not closed")
        
        text = node.text
        if delimiter not in text:
            text_node_list.append(node)

        while delimiter in text:
            tmp = text.split(delimiter, 1)
            text_pre_delimiter = tmp[0]
            delimited_text = tmp[1].split(delimiter, 1)[0]
            text = tmp[1].split(delimiter, 1)[1]

            if text_pre_delimiter != "":
                text_node_list.append(TextNode(text_pre_delimiter, node.text_type))
            text_node_list.append(TextNode(delimited_text, text_type))
            if delimiter not in text:
                text_node_list.append(TextNode(text, node.text_type))

    return text_node_list

def split_nodes(nodes):
    delimited_nodes = nodes.copy()
    delimiters = [('`', TextType.CODE), ('**', TextType.BOLD), ('*', TextType.ITALIC)]
    for x, y in delimiters:
        delimited_nodes = split_nodes_delimiter(delimited_nodes, x, y)
    return delimited_nodes
