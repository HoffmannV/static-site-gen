from textnode import TextType, TextNode
from leafnode import LeafNode
from parentnode import ParentNode
import re

def text_node_to_html_node(text_node):
    match(text_node.text_type):
        case(TextType.NORMAL | TextType.HTML):
            return LeafNode(text_node.text)
        case(TextType.BOLD):
            return LeafNode(text_node.text, "b")
        case(TextType.ITALIC):
            return LeafNode(text_node.text, "i")
        case(TextType.CODE):
            return LeafNode(text_node.text, "code")
        case(TextType.IMAGE):
            return LeafNode(value="", tag="img", props={"src": text_node.url, "alt": text_node.text})
        case(TextType.LINK):
            return LeafNode(value=text_node.text, tag="a", props={"href": text_node.url})
        case _:
            raise Exception(f"Whoops something went wrong!\n{text_node}")

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

def split_nodes_text(nodes):
    delimited_nodes = nodes.copy()
    delimiters = [('`', TextType.CODE), ('**', TextType.BOLD), ('*', TextType.ITALIC)]
    for x, y in delimiters:
        delimited_nodes = split_nodes_delimiter(delimited_nodes, x, y)
        for i in range(len(delimited_nodes)):
            delimited_nodes[i] = TextNode(text_node_to_html_node(delimited_nodes[i]).to_html(), TextType.HTML)
            #print(delimited_nodes)
    return delimited_nodes

def split_nodes_image(old_nodes):
    new_nodes = [] 
    for node in old_nodes:
        extracted_img = extract_markdown_images(node.text)
        text = node.text
        for img_alt, img_url in extracted_img:
            delimiter = f"![{img_alt}]({img_url})"
            tmp = text.split(delimiter, 1)
            text_pre_delimiter = tmp[0]
            text = tmp[1] 
            if text_pre_delimiter != "":
                new_nodes.append(TextNode(text_pre_delimiter, TextType.NORMAL))
            new_nodes.append(TextNode(img_alt, TextType.IMAGE, img_url))
        if text != "":
            new_nodes.append(TextNode(text, TextType.NORMAL))
    return new_nodes

def split_nodes_link(old_nodes):
    new_nodes = [] 
    for node in old_nodes:
        if node.text_type != TextType.IMAGE:
            extracted_img = extract_markdown_links(node.text)
            text = node.text
            for img_alt, img_url in extracted_img: 
                delimiter = f"[{img_alt}]({img_url})"
                tmp = text.split(delimiter, 1)
                text_pre_delimiter = tmp[0]
                text = tmp[1] 
                if text_pre_delimiter != "":
                    new_nodes.append(TextNode(text_pre_delimiter, TextType.NORMAL))
                new_nodes.append(TextNode(img_alt, TextType.LINK, img_url))
            if text != "":
                new_nodes.append(TextNode(text, TextType.NORMAL))
        else:
            new_nodes.append(node)
    return new_nodes

def extract_markdown_images(text):
    matches = re.findall(r"\!\[(.*?)\]\((.*?)\)", text)
    return matches

def extract_markdown_links(text):
    matches = re.findall(r"\[(.*?)\]\((.*?)\)", text)
    return matches

def text_to_text_nodes(text):
    new_nodes = split_nodes_text([text])
    new_nodes = split_nodes_image(new_nodes)
    new_nodes = split_nodes_link(new_nodes)
    return new_nodes

def markdown_to_blocks(markdown):
    content_lst = markdown.strip().split("\n")
    tmp = []
    content_blocks = []
    for i in range(len(content_lst)):
        if content_lst[i] == '':
            content_blocks.append('\n'.join(tmp))
            tmp = []
        elif  i == len(content_lst) - 1:
            tmp.append(content_lst[i])
            content_blocks.append('\n'.join(tmp))
        else:
            tmp.append(content_lst[i])
    return content_blocks

def block_to_block_type(block):
    max_heading = 6
    heading_type = 0

    #Check for heading
    if block[0] == '#':
        for char in block:
            if char == '#':
                heading_type += 1
            elif char == ' ' and heading_type < 7:
                return ParentNode(children=list(), tag=f"h{heading_type}")
            else:
                raise ValueError("Incorrect heading markdown")

    #check for code block
    elif ''.join(block[:3]) == "```":
        if ''.join(block[-3:]) == "```":
            return ParentNode(list(), "input", {"readonly": "readonly", "style": "width: 100%; padding: 10px; font-family: monospace; font-size: 14px; background-color: #f5f5f5; border: 1px solid #ccc; color: #333; overflow: auto; white-space: pre; border-radius: 4px; pointer-events: none; user-select: text;"}) 
        else:
            raise ValueError("Code block not closed")

    #check for qoute
    elif block[0] == '>':
        lines = block.split('\n')
        for line in lines:
            if line[0] != '>':
                raise ValueError("Every line in a qoute block must begin with the \'>\' character")
        return ParentNode(list(), "blockquote")
    
    #check for unordered list
    elif block[0] == '*' or block[0] == '-':
        lines = block.split('\n')
        for line in lines:
            if line[0] != '*' and block[0] != '-':
                raise ValueError("Every line in a unordered list block must begin with the \'*\' or \'-\' character")
            if line[1] != ' ':
                raise ValueError("There has to be a whitespace after the \'*\' or \'-\' character")
        return ParentNode(list(), "ul")
    
    #chekc for ordered list
    elif block[1] == '.':
        lines = block.split('\n')
        for i in range(len(lines)):
            if lines[i][0] != str(i+1) or lines[i][1] != '.' or lines[i][2] != ' ':
                raise ValueError(f"Every line in a ordered list block must begin with the appropriate number followed by the \'.\' character and a white space\n{lines}")
        return ParentNode(list(), "ol")

    else:
        return ParentNode(list(), "p")
 

