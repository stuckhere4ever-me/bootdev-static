import unittest

from src.htmlnode import HTMLNode


class TestHTMLNode(unittest.TestCase):
    def test_eq(self):
        node_one = HTMLNode('a', "Hello", [HTMLNode(), HTMLNode()], {'href':'www.awesomesause.com', 'template': '_blank'})
        node_two = HTMLNode('a', "Hello", [HTMLNode(), HTMLNode()], {'href':'www.awesomesause.com', 'template': '_blank'})
        self.assertEqual(node_one, node_two)
    
    def test_not_eq(self):
        node_one = HTMLNode('a', "Hello", [HTMLNode(), HTMLNode()], {'href':'www.awesomesause.com', 'template': '_blank'})
        node_two = HTMLNode('b', "Hello", [HTMLNode(), HTMLNode()], {'href':'www.awesomesause.com', 'template': '_blank'})
        self.assertNotEqual(node_one, node_two)
    
    def test_not_empty(self):
        node_one = HTMLNode()
        node_two = HTMLNode(None, None, None, None)
        self.assertEqual(node_one, node_two)

    def test_params_one(self):
        node_one = HTMLNode('a', "Hello", None, {'href':'www.awesomesause.com', 'target': '_blank'})
        params = node_one.props_to_html()
        test_string = ' href=\"www.awesomesause.com\" target=\"_blank\"'
        self.assertEqual(params, test_string)

    def test_params_two(self):
        node_one = HTMLNode('a', "Hello", [HTMLNode(None,None,None,{'target':"_blank"})], {'href':'www.awesomesause.com'})
        params = node_one.props_to_html()
        test_string = ' href=\"www.awesomesause.com\"'
        self.assertEqual(params, test_string)

    def test_params_three(self):
        node_one = HTMLNode()
        params = node_one.props_to_html()
        test_string = ''
        self.assertEqual(params, test_string)


if __name__ == "__main__":
    unittest.main()