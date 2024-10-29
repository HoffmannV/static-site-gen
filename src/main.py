from textnode import TextType, TextNode
from htmlnode import HTMLNode
from leafnode import LeafNode
from parentnode import ParentNode
from enum import Enum
import spgutil

def main():
    file = open('public/text', 'r')
    content = file.read()
    file.close()

    html_content = spgutil.markdown_to_html_node(content)

    print(html_content.to_html())

if __name__ == "__main__":    
    main()
