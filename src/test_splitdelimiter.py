import unittest

from split_delimeter import split_nodes_delimiter
from textnode import TextNode, TextType, text_node_to_html_node
from htmlnode import HTMLNode, LeafNode, ParentNode


class TestNodeSplit(unittest.TestCase):
    def test_one_bold_delimiter(self):
        node = [TextNode("This is **bold** text", TextType.TEXT)]
        expected = [
            TextNode("This is ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" text", TextType.TEXT),
        ]
        result = split_nodes_delimiter(node, "**", TextType.BOLD)
        self.assertEqual(result, expected)

    def test_multiple_bold_delimiters_in_one_string(self):
        node = [TextNode("Some **bold** and **more bold** words", TextType.TEXT)]
        expected = [
            TextNode("Some ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" and ", TextType.TEXT),
            TextNode("more bold", TextType.BOLD),
            TextNode(" words", TextType.TEXT)
        ]
        result = split_nodes_delimiter(node, "**", TextType.BOLD)
        self.assertEqual(result, expected)

    def test_one_italic_delimiter(self):
        node = [TextNode("This is *italic* text", TextType.TEXT)]
        expected = [
            TextNode("This is ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" text", TextType.TEXT)
        ]
        result = split_nodes_delimiter(node, "*", TextType.ITALIC)
        self.assertEqual(result, expected)

    def test_multiple_italic_delimiters_in_one_string(self):
        node = [TextNode("Some *italic* and *more italic* words", TextType.TEXT)]
        expected = [
            TextNode("Some ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" and ", TextType.TEXT),
            TextNode("more italic", TextType.ITALIC),
            TextNode(" words", TextType.TEXT)
        ]
        result = split_nodes_delimiter(node, "*", TextType.ITALIC)
        self.assertEqual(result, expected)

    def test_one_code_delimiter(self):
        node = [TextNode("This is a `code` block", TextType.TEXT)]
        expected = [
            TextNode("This is a ", TextType.TEXT),
            TextNode("code", TextType.CODE),
            TextNode(" block", TextType.TEXT),
        ]
        result = split_nodes_delimiter(node, "`", TextType.CODE)
        self.assertEqual(result, expected)

    def test_multiple_code_delimiters_in_one_string(self):
        node = [TextNode("Some `code` blocks, and more `code` blocks", TextType.TEXT)]
        expected = [
            TextNode("Some ", TextType.TEXT),
            TextNode("code", TextType.CODE),
            TextNode(" blocks, and more ", TextType.TEXT),
            TextNode("code", TextType.CODE),
            TextNode(" blocks", TextType.TEXT)
        ]
        result = split_nodes_delimiter(node, "`", TextType.CODE)
        self.assertEqual(result, expected)

    def test_one_link_delimiter(self):
        node = [TextNode("")]

    def test_no_delimiter(self):
        node = [TextNode("Just plain text", TextType.TEXT)]
        expected = [TextNode("Just plain text", TextType.TEXT)]
        result = split_nodes_delimiter(node, "**", TextType.BOLD)
        self.assertEqual(result, expected)

    def test_missing_closing_delimiter(self):
        with self.assertRaises(Exception):
            node = [TextNode("Unmatched **bold text", TextType.TEXT)]
            split_nodes_delimiter(node, "**", TextType.BOLD)
