from textnode import TextNode, TextType

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    if text_type not in TextType:
        raise Exception("invalid text type")
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue

        text = node.text

        while delimiter in text:
            first_break = text.find(delimiter)
            second_break = text.find(delimiter, first_break + 1)

            if first_break == -1 or second_break == -1:
                raise Exception("Invalid syntax: Missing matching delimiters in text.")

            first_part = (text[:first_break])
            second_part = (text[first_break + len(delimiter):second_break])
            third_part = (text[second_break + len(delimiter):])

            new_nodes.append(TextNode(first_part, TextType.TEXT))
            new_nodes.append(TextNode(second_part, text_type))
            text = third_part
        
        if text:
            new_nodes.append(TextNode(text, TextType.TEXT))

        