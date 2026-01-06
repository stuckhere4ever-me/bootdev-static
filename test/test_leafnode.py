import unittest

from src.htmlnode import LeafNode


class TestHTMLNode(unittest.TestCase):
    def test_eq(self):
        node_one = LeafNode('p', "This is a Leaf Node")
        node_two = LeafNode('p', "This is a Leaf Node")
        self.assertEqual(node_one, node_two)

    def test_leaf_rejects_children(self):
        with self.assertRaises(TypeError):
            LeafNode(tag="p", value="hi", children=[LeafNode(tag="b", value="x")]) # type: ignore

    def test_leaf_rejects_no_val(self):
        with self.assertRaises(ValueError):
            node_one = LeafNode(tag="p", value=None) # type: ignore
            node_one.to_html()

    def test_leaf_to_html_wrapping_tags(self):
        cases = [
            ("p", "<p>Hello, world!</p>"),
            ("b", "<b>Hello, world!</b>"),
            ("i", "<i>Hello, world!</i>"),
            ("code", "<code>Hello, world!</code>"),
            ("blockquote", "<blockquote>Hello, world!</blockquote>"),
            ("h1", "<h1>Hello, world!</h1>"),
            ("h2", "<h2>Hello, world!</h2>"),
            ("h3", "<h3>Hello, world!</h3>"),
            ("h4", "<h4>Hello, world!</h4>"),
            ("h5", "<h5>Hello, world!</h5>"),
            ("h6", "<h6>Hello, world!</h6>"),
            ("li", "<li>Hello, world!</li>"),
        ]

        for tag, expected in cases:
            with self.subTest(tag=tag):
                node = LeafNode(tag, "Hello, world!")
                self.assertEqual(node.to_html(), expected)

    def test_leaf_rejects_wrong_type(self):
        with self.assertRaises(TypeError):
            node_one = LeafNode(tag="ul", value="Hello World")
            node_one.to_html()
    
    def test_leaf_to_html_a(self):
        node = LeafNode("a", "Click me", {"href": "https://www.google.com"})
        self.assertEqual(node.to_html(), '<a href="https://www.google.com">Click me</a>')

    def test_leaf_to_html_img(self):
        node = LeafNode("img", "", {"src": "https://example.com/image.jpg", "alt": "An image"})
        self.assertEqual(
            node.to_html(),
            '<img src="https://example.com/image.jpg" alt="An image" />'
        )

    def test_leaf_to_html_none_tag_returns_raw_value(self):
        node = LeafNode(None, "Just text")
        self.assertEqual(node.to_html(), "Just text")




if __name__ == "__main__":
    unittest.main()