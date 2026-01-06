import unittest

from src.textnode import TextNode, TextType
from src.markdown_converter import text_node_to_html_node
from src.markdown_helpers import SPLIT_BUILDER

code_delimiter = SPLIT_BUILDER[TextType.CODE]
bold_delimiter = SPLIT_BUILDER[TextType.BOLD]
italics_delimeter = SPLIT_BUILDER[TextType.ITALIC]


class TestTextNode(unittest.TestCase):

 
    
    def test_eq_bold(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)
    
    def test_eq_italic(self):
        node = TextNode("This is a text node", TextType.ITALIC)
        node2 = TextNode("This is a text node", TextType.ITALIC)
        self.assertEqual(node, node2)

    def test_eq_Link(self):
        node = TextNode("This is a link node", TextType.LINK, 'www.google.com')
        node2 = TextNode("This is a link node", TextType.LINK, 'www.google.com')
        self.assertEqual(node, node2)

    def test_not_eq_bold(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is also a text node", TextType.BOLD)
        self.assertNotEqual(node, node2)
    
    def test_not_eq_italic(self):
        node = TextNode("This is a text node", TextType.ITALIC)
        node2 = TextNode("This is also a text node", TextType.ITALIC)
        self.assertNotEqual(node, node2)

    def test_not_eq_Link(self):
        node = TextNode("This is a link node", TextType.LINK, 'www.google.com')
        node2 = TextNode("This is a link node", TextType.LINK, 'www.google.con')
        self.assertNotEqual(node, node2)
    
    def test_not_eq_diff_types(self):
        node = TextNode("This is a link node", TextType.LINK, 'www.google.com')
        node2 = TextNode("This is a text node", TextType.TEXT)
        self.assertNotEqual(node, node2)

    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        bold_node = TextNode("This is a bold node", TextType.BOLD)
        italic_node = TextNode("This is an italic node", TextType.ITALIC)
        code_node = TextNode("This is a code node", TextType.CODE)
        link_node = TextNode("This is a link node", TextType.LINK, "http://awesomesauce.com")
        img_node = TextNode("This is an image node", TextType.IMAGE, "http://myimagesarecool.com")        
        
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

        bold_html = text_node_to_html_node(bold_node)
        self.assertEqual(bold_html.tag, 'b')
        self.assertEqual(bold_html.value, "This is a bold node")
        
        italic_html = text_node_to_html_node(italic_node)
        self.assertEqual(italic_html.tag, 'i')
        self.assertEqual(italic_html.value, "This is an italic node")

        code_html = text_node_to_html_node(code_node)
        self.assertEqual(code_html.tag, 'code')
        self.assertEqual(code_html.value, "This is a code node")

        link_html = text_node_to_html_node(link_node)
        self.assertEqual(link_html.tag, 'a')
        self.assertEqual(link_html.value, "This is a link node")
        html_properties = link_html.props_to_html()
        self.assertEqual(html_properties, ' href="http://awesomesauce.com"')

        img_html = text_node_to_html_node(img_node)
        self.assertEqual(img_html.tag, 'img')
        self.assertEqual(img_html.value, "")
        html_properties = img_html.props_to_html()
        self.assertEqual(html_properties, ' src="http://myimagesarecool.com" alt="This is an image node"')

    def split_node(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        new_nodes = code_delimiter([node])

        expected = [
            TextNode("This is text with a ", TextType.TEXT, None),
            TextNode("code block", TextType.CODE, None),
            TextNode(" word", TextType.TEXT, None),
        ]

        self.assertEqual(new_nodes, expected)

        node = TextNode("This is text with a `code block` word and another `code block` word", TextType.TEXT)
        new_nodes = code_delimiter([node])

        expected = [
            TextNode("This is text with a ", TextType.TEXT, None),
            TextNode("code block", TextType.CODE, None),
            TextNode(" word and another ", TextType.TEXT, None),
            TextNode("code block", TextType.CODE, None),
            TextNode(" word", TextType.TEXT, None),
        ]
        self.assertEqual(new_nodes, expected)


        node = TextNode("This is **bold** text", TextType.TEXT)
        new_nodes = bold_delimiter([node])

        expected = [
            TextNode("This is ", TextType.TEXT, None),
            TextNode("bold", TextType.BOLD, None),
            TextNode(" text", TextType.TEXT, None),
        ]

        self.assertEqual(new_nodes, expected)


        node1 = TextNode("Keep ", TextType.TEXT, None)
        node2 = TextNode("already bold", TextType.BOLD, None)

        new_nodes = code_delimiter([node1, node2])

        expected = [
            TextNode("Keep ", TextType.TEXT, None),
            TextNode("already bold", TextType.BOLD, None),
        ]

        self.assertEqual(new_nodes, expected)

        with self.assertRaises(ValueError):
            node = TextNode("This is `broken", TextType.TEXT, None)
            code_delimiter([node])

    def test_split_delimiter_no_trailing_empty_text_node(self):
        node = TextNode("Ends with code `x`", TextType.TEXT, None)
        new_nodes = code_delimiter([node])

        expected = [
            TextNode("Ends with code ", TextType.TEXT, None),
            TextNode("x", TextType.CODE, None),
        ]
        self.assertEqual(new_nodes, expected)

    def test_split_delimiter_no_leading_empty_text_node(self):
        node = TextNode("`x` starts with code", TextType.TEXT, None)
        new_nodes = code_delimiter([node])

        expected = [
            TextNode("x", TextType.CODE, None),
            TextNode(" starts with code", TextType.TEXT, None),
        ]
        self.assertEqual(new_nodes, expected)

    def test_split_delimiter_no_empty_text_nodes_between_back_to_back(self):
        node = TextNode("`one``two`", TextType.TEXT, None)
        new_nodes = code_delimiter([node])

        expected = [
            TextNode("one", TextType.CODE, None),
            TextNode("two", TextType.CODE, None),
        ]
        self.assertEqual(new_nodes, expected)



if __name__ == "__main__":
    unittest.main()