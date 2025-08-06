import unittest

from htmlnode import *

class TestHTMLNode(unittest.TestCase):
    def test_eq(self):
        prop = {
            "href": "https://www.google.com",
            "target": "_blank",
        }
        node = HTMLNode(tag="h1", value="header", props=prop)
        node2 = HTMLNode(tag="h1", value="header", props=prop)
        node3 = HTMLNode(tag="h2", value="header", props=prop)
        
        self.assertEqual(node, node2)
        self.assertNotEqual(node, node3)

    def test_props_to_html(self):
        prop = {
            "href": "https://www.google.com",
            "target": "_blank",
        }
        prop2 = {
            "href": "https://www.google.com",
            "target": "_blank",
            "test": "test",
        }
        node = HTMLNode(tag="h1", value="header", props=prop)
        node2 = HTMLNode(tag="h1", value="header", props=prop2)
        node3 = HTMLNode()
        html = node.props_to_html()
        html2 = node2.props_to_html()
        html3 = node3.props_to_html()
        self.assertEqual(html, ' href="https://www.google.com" target="_blank"')
        self.assertEqual(html2, ' href="https://www.google.com" target="_blank" test="test"')
        self.assertNotEqual(html, html2)
        self.assertEqual(html3, "")

class TestLeafNode(unittest.TestCase):
    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")
        node = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        self.assertEqual(node.to_html(), '<a href="https://www.google.com">Click me!</a>')
        node = LeafNode("a", None)
        with self.assertRaises(ValueError):
            node.to_html()

class TestParentNode(unittest.TestCase):
    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )


if __name__ == "__main__":
    unittest.main()