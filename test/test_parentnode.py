import unittest

from src.htmlnode import LeafNode, ParentNode


class TestHTMLNode(unittest.TestCase):
    def test_leaf_rejects_children(self):
        with self.assertRaises(TypeError):
            LeafNode(tag="p", value="hi", children=[LeafNode(tag="b", value="x")]) # type: ignore

    def test_leaf_rejects_no_val(self):
        with self.assertRaises(ValueError):
            node_one = LeafNode(tag="p", value=None) # type: ignore
            node_one.to_html()

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

    def test_parent_to_html_multiple_children_mixed(self):
        node = ParentNode(
            "p",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
        )
        self.assertEqual(
            node.to_html(),
            "<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>",
        )

    def test_parent_to_html_raises_if_tag_none(self):
        with self.assertRaises(ValueError):
            ParentNode(None, [LeafNode("span", "child")]).to_html()  # type: ignore[arg-type]

    def test_parent_to_html_raises_if_children_none(self):
        with self.assertRaises(ValueError):
            ParentNode("div", None).to_html()  # type: ignore[arg-type]

    def test_parent_to_html_raises_if_children_empty_list(self):
        with self.assertRaises(ValueError):
            ParentNode("div", []).to_html()


    def test_parent_to_html_nested_siblings(self):
        node = ParentNode(
            "div",
            [
                ParentNode("span", [LeafNode(None, "a")]),
                ParentNode("span", [LeafNode(None, "b")]),
            ],
        )
        self.assertEqual(node.to_html(), "<div><span>a</span><span>b</span></div>")

    def test_parent_to_html_deep_nesting(self):
        node = ParentNode(
            "div",
            [
                ParentNode(
                    "section",
                    [
                        ParentNode(
                            "p",
                            [
                                LeafNode("b", "x"),
                                LeafNode(None, "y"),
                            ],
                        )
                    ],
                )
            ],
        )
        self.assertEqual(node.to_html(), "<div><section><p><b>x</b>y</p></section></div>")

    def test_parent_to_html_with_props(self):
        node = ParentNode(
            "div",
            [LeafNode("span", "child")],
            {"id": "main"},
        )
        self.assertEqual(node.to_html(), '<div id="main"><span>child</span></div>')



if __name__ == "__main__":
    unittest.main()