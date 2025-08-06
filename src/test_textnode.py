import unittest

from textnode import *
from functions import *


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        node3 = TextNode("This is a text node", TextType.IMAGE)
        self.assertEqual(node, node2)
        self.assertNotEqual(node, node3)
        node = TextNode("This is a text node", TextType.BOLD, None)
        node3 = TextNode("This is a text node", TextType.BOLD, "https://www.boot.dev/lessons/0abc7ce4-3855-4624-9f2d-7e566690fee1")
        self.assertNotEqual(node, node3)
        self.assertEqual(node, node2)
    
    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

        node = TextNode("Bold", TextType.BOLD)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "Bold")

        node = TextNode("Italic", TextType.ITALIC)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "i")
        self.assertEqual(html_node.value, "Italic")

        node = TextNode('print("Hello world")', TextType.CODE)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "code")
        self.assertEqual(html_node.value, 'print("Hello world")')

        node = TextNode("Link", TextType.LINK, "www.testurl.org")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.value, "Link")
        self.assertEqual(html_node.props, {"href": "www.testurl.org"})

        node = TextNode("Image", TextType.IMAGE, "www.testurl.org")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.value, "Image")
        self.assertEqual(html_node.props, {"src":"www.testurl.org", "alt":"Image"})

    def test_split_nodes_delimiter(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        correct_nodes = [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" word", TextType.TEXT),
        ]
        self.assertEqual(new_nodes, correct_nodes)

        node = TextNode("This is text with a **bolded** word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        correct_nodes = [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("bolded", TextType.BOLD),
            TextNode(" word", TextType.TEXT),
        ]
        self.assertEqual(new_nodes, correct_nodes)

        node = TextNode("This is text with a _italicized_ word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "_", TextType.ITALIC)
        correct_nodes = [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("italicized", TextType.ITALIC),
            TextNode(" word", TextType.TEXT),
        ]
        self.assertEqual(new_nodes, correct_nodes)

        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        correct_nodes = [
            TextNode("This is text with a `code block` word", TextType.TEXT),
        ]
        self.assertEqual(new_nodes, correct_nodes)

        node = TextNode("This is text with a `code block word", TextType.IMAGE)
        with self.assertRaises(Exception):
            node.split_nodes_delimiter([node], "`", TextType.CODE)


if __name__ == "__main__":
    unittest.main()