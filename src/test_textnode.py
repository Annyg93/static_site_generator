import unittest

from textnode import TextNode, TextType, text_node_to_html_node
from htmlnode import HTMLNode, LeafNode, ParentNode


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_not_eq(self):
        node = TextNode("This is a text node", TextType.ITALIC)
        node2 = TextNode("This is a text node", TextType.TEXT)
        self.assertNotEqual(node, node2)

    def test_url(self):
        node = TextNode("This is a text node", TextType.BOLD, url=None)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_converting_simple_textnode(self):
        node = TextNode("very simple", TextType.TEXT)
        expected = LeafNode(None, "very simple")
        result = text_node_to_html_node(node)
        self.assertEqual(result, expected)

    def test_converting_bold_textnode(self):
        node = TextNode("bold text", TextType.BOLD)
        expected = LeafNode("b", "bold text")
        result = text_node_to_html_node(node)
        self.assertEqual(result, expected)

    def test_converting_link_with_url_textnode(self):
        node = TextNode("link here", TextType.LINK, "https://google.com")
        expected = LeafNode("a", "link here", {"href": "https://google.com"})
        result = text_node_to_html_node(node)
        self.assertEqual(result, expected)

    def test_converting_imaage_with_src_and_text_textnode(self):
        node = TextNode("alt text", TextType.IMAGE, "https://example.com/image.png")
        expected = LeafNode(
            "img", "", {"src": "https://example.com/image.png", "alt": "alt text"}
        )
        result = text_node_to_html_node(node)
        self.assertEqual(result, expected)

    def test_error_case_converting_textnode(self):
        with self.assertRaises(Exception):
            node = TextNode("this fails", None)
            text_node_to_html_node(node)


if __name__ == "__main__":
    unittest.main()
