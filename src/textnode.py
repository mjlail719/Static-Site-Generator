from enum import Enum
from htmlnode import *

class TextType(Enum):
    TEXT = "TEXT"
    BOLD = "**BOLD**"
    ITALIC = "_ITALIC_"
    CODE = "`CODE`"
    LINK = "[LINK](URL)"
    IMAGE = "![IMAGE](URL)"

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"

class TextNode:
    def __init__(self, text, text_type, url=None):
        self.text = text
        self.text_type = text_type
        self.url = url
    
    def __eq__(self, other):
        return (
                self.text == other.text and self.text_type == other.text_type and self.url == other.url
            )

    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type.value}, {self.url})"

def text_node_to_html_node(text_node):
    if text_node.text != None:
        match text_node.text_type:
            case TextType.TEXT:
                return LeafNode(None, text_node.text)
            case TextType.BOLD:
                return LeafNode("b", text_node.text)
            case TextType.ITALIC:
                return LeafNode("i", text_node.text)
            case TextType.CODE:
                return LeafNode("code", text_node.text)
            case TextType.LINK:
                return LeafNode("a", text_node.text, {"href": text_node.url})
            case TextType.IMAGE:
                return LeafNode("img", text_node.text, {"src": text_node.url, "alt": text_node.text})
            case _:
                raise Exception("Text type must be one of the valid selections")