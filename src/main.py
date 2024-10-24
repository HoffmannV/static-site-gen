from textnode import TextType, TextNode

def main():
    node = TextNode("text", TextType.bold_text)
    node2 = TextNode("text", TextType.bold_text)
    boot_dev_node = TextNode("This is a text node", TextType.bold_text, "https://www.boot.dev")

    print(boot_dev_node)
    print(node)
    print(boot_dev_node == node)
    print(node == node2)

if __name__ == "__main__":    
    main()
