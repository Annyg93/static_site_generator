import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode


class TestHTMLNode(unittest.TestCase):
    def test_eq(self):
        node = HTMLNode(props={"href": "https://www.boot.dev"})
        self.assertEqual(node.props_to_html(), ' href="https://www.boot.dev"')

    def test_no_prop(self):
        node = HTMLNode()
        self.assertEqual(node.props_to_html(), "")

    def test_multiple_prop(self):
        node = HTMLNode(props={"href": "https://boot.dev", "target": "_blank"})
        expected1 = ' href="https://boot.dev" target="_blank"'
        expected2 = ' target="_blank" href="https://boot.dev"'
        result = node.props_to_html()
        self.assertTrue(result == expected1 or result == expected2)

    def test_ln_no_value(self):
        with self.assertRaises(ValueError):
            node = LeafNode(tag="a", value=None)
            node.to_html()

    def test_ln_no_tag(self):
        node = LeafNode(tag=None, value="Hello")
        expected = "Hello"
        result = node.to_html()
        self.assertEqual(result, expected)

    def test_ln_tag_value_and_prop(self):
        node = LeafNode(
            tag="a", value="Click me!", props={"href": "https://www.google.com"}
        )
        expected = '<a href="https://www.google.com">Click me!</a>'
        result = node.to_html()
        self.assertEqual(result, expected)

    def test_pn_multiple_children_in_a_row(self):
        node = ParentNode(
            "p",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
        )
        expected = "<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>"
        result = node.to_html()
        self.assertEqual(result, expected)

    def test_pn_nested_parentnodes(self):
        node = ParentNode("div", [ParentNode("p", [LeafNode(None, "some text")])])
        expected = "<div><p>some text</p></div>"
        result = node.to_html()
        self.assertEqual(result, expected)

    def test_pn_props_on_parent(self):
        node = ParentNode(
            "a", [LeafNode(None, "link")], props={"href": "https://www.google.com"}
        )

        expected = '<a href="https://www.google.com">link</a>'
        result = node.to_html()
        self.assertEqual(result, expected)

    def test_pn_empty_children_list(self):
        with self.assertRaises(ValueError):
            node = ParentNode("a", children=[])
            node.to_html()

    def test_pn_mixed_nesting(self):
        node = ParentNode(
            "div",
            [
                LeafNode("b", "bold text"),
                ParentNode("p", [LeafNode("i", "italic text")]),
            ],
        )
        expected = "<div><b>bold text</b><p><i>italic text</i></p></div>"
        result = node.to_html()
        self.assertEqual(result, expected)

    def test_pn_tag_is_none(self):
        with self.assertRaises(ValueError):
            node = ParentNode(None, [LeafNode("b", "bold text")])
            node.to_html()

    def test_pn_deep_nesting(self):
        node = ParentNode(
            "div",
            [
                ParentNode(
                    "div",
                    [
                        ParentNode(
                            "p",
                            [
                                LeafNode("i", "italic text"),
                                ParentNode("span", [LeafNode(None, "some text")]),
                            ],
                        )
                    ],
                )
            ],
        )
        expected = (
            "<div><div><p><i>italic text</i><span>some text</span></p></div></div>"
        )
        result = node.to_html()
        self.assertEqual(result, expected)

    def test_pn_multiple_props(self):
        node = ParentNode(
            "p",
            [LeafNode(None, "link")],
            props={
                "href": "https://www.google.com",
                "id": "link_to_google",
                "class": "link",
            },
        )
        expected = (
            '<p href="https://www.google.com" id="link_to_google" class="link">link</p>'
        )
        result = node.to_html()
        self.assertEqual(result, expected)
