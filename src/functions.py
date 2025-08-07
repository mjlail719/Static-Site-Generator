from htmlnode import *
from textnode import *
import re

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for node in old_nodes:
        if node.text_type == TextType.TEXT:
            split_string = node.text.split(delimiter)
            if len(split_string) % 2 == 0:
                split_string.insert(0, "")
            i = 0
            if len(split_string) % 2 == 0:
                raise Exception("Invalid markdown syntax, must have closing delimiter")
            for string in split_string:
                if string == "":
                    i += 1
                    continue
                if i % 2 == 1:
                    new_nodes.append(TextNode(string, text_type))
                else:
                    new_nodes.append(TextNode(string, TextType.TEXT))
                i += 1
            
        else:
            new_nodes.append(node)
    return new_nodes

def split_nodes_image(old_nodes):
    return split_nodes_image_or_link(old_nodes, TextType.IMAGE)

def split_nodes_link(old_nodes):
    return split_nodes_image_or_link(old_nodes, TextType.LINK)


def split_nodes_image_or_link(old_nodes, text_type):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        match(text_type):
            case TextType.IMAGE:
                image = extract_markdown_images(node.text)

                if image != []:
                    new_nodes.append(TextNode(image[0][0], text_type, url = image[0][1]))
                else:
                    new_nodes.append(node)
            case TextType.LINK:
                link = extract_markdown_links(node.text)
                if link != []:
                    new_nodes.append(TextNode(link[0][0], text_type, url = link[0][1]))
                else:
                    new_nodes.append(node)
    return new_nodes
            
def text_to_textnodes(text):
    nodes = [TextNode(text, TextType.TEXT)]
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    return nodes
    

def extract_markdown_images(text):
    return re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)

def extract_markdown_links(text):
    return re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)

def markdown_to_blocks(markdown):
    split_markdown = markdown.split("\n\n")
    output = []
    for string in split_markdown:
        string = string.strip("\n\t ")
        if string != "":
            output.append(string)
    return output

def block_to_block_type(block):
    
    heading_start = block.split()
    if heading_start[0].startswith("#"):
        count = heading_start[0].count("#")
        if count in range(1,7):
            return BlockType.HEADING
    
    if block.startswith("```") and block.endswith("```"):
        return BlockType.CODE

    split_block = block.split("\n")
    correct_start = True
    for string in split_block:
        if not string.startswith(">"):
            correct_start = False
            break

    if correct_start:
        return BlockType.QUOTE

    correct_start = True
    for string in split_block:
        if not string.startswith("- "):
            correct_start = False
            break
        
    if correct_start:
        return BlockType.UNORDERED_LIST
        
    correct_start = True
    index = 1
    for string in split_block:
        if not string.startswith(f"{index}. "):
            correct_start = False
            break
        index += 1
    
    if correct_start:
        return BlockType.ORDERED_LIST

    
    return BlockType.PARAGRAPH

def markdown_to_html_node(markdown):
    split_markdown = markdown_to_blocks(markdown)
    blocks_typed = []
    html_nodes = []
    for block in split_markdown:
        blocks_typed.append((block, block_to_block_type(block)))


    for block, block_type in blocks_typed:
        html_nodes.append(block_to_html(block, block_type))

    parent_html_block = ParentNode("div", html_nodes)
    final_html = parent_html_block
    return final_html

def block_to_html(block, block_type):
    tag = ""
    match(block_type):
        case BlockType.PARAGRAPH:
            tag = "p"
        case BlockType.HEADING:
            heading_num = block.count("#")
            tag = f"h{heading_num}"
            replacer_string = "#" * heading_num + " "
            block = block.replace(replacer_string, "")
        case BlockType.CODE:
            tag = "code"
            block = block.strip("```")
            block = block.lstrip()
            code_text = TextNode(block, TextType.CODE)
            return ParentNode("pre", [text_node_to_html_node(code_text)], {})
        case BlockType.QUOTE:
            tag = "blockquote"
            block = block.replace("> ", "")
            block = block.replace(">", " ")
        case BlockType.UNORDERED_LIST:
            tag = "ul"
            block = block.replace("- ", "")
            temp_block = ""
            for string in block.split("\n"):
                temp_block += f"<li>\n{string}\n</li>"
            block = temp_block[:len(temp_block) - 1]
        case BlockType.ORDERED_LIST:
            tag = "ol"
            index = 1
            temp_block = ""
            for string in block.strip().split("\n"):
                temp_block += string.replace(f"{index}. ", "\n")
                index += 1
            block = temp_block
            block = block.lstrip()
            temp_block = ""
            for string in block.split("\n"):
                temp_block += f"<li>{string}</li>\n"
            block = temp_block[:len(temp_block) - 1]

    children = text_to_children(block)
    result = ParentNode(tag, children, {})
    return result


def text_to_children(text):
    if isinstance(text,list):
        text = convert_to_string(text)
    output = []
    for line in text.split("\n"):
        
        if line != None:
            text_nodes = text_to_textnodes(line)
            for node in text_nodes:
                output.append(text_node_to_html_node(node))
    return output
    
def convert_to_string(text):
    string = ""
    for entry in text:
        string += entry + " "
    return string[:len(string)]

def extract_title(markdown):
    split_md = markdown.split("\n")
    i = 0
    h1 = ""
    for block in split_md:
        split_block = block.split(" ")
        for word in split_block:
            if word == "#":
                if i < len(split_block):
                    h1 = split_block[i + 1:]
                else:
                    raise Exception("Invalid header")
            i += 1

    if h1 == "":
        raise Exception("Invalid header")

    return convert_to_string(h1).strip()
