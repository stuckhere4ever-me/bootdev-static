import unittest

from src.textnode import TextNode, TextType
from src.markdown_helpers import SPLIT_BUILDER


split_nodes_image = SPLIT_BUILDER[TextType.IMAGE] 
split_nodes_link = SPLIT_BUILDER[TextType.LINK] 


class TestSplitImagesAndLinks(unittest.TestCase):
    # ----------- Images -----------
    def test_image_breakout(self):
        node = TextNode(
                "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
                TextType.TEXT,
            )
        new_nodes = split_nodes_image([node])
        
        expected =  [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ]

        self.assertEqual(new_nodes, expected)

        node_one = TextNode(
                "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
                TextType.TEXT,
            )
        node_two = TextNode(
            "This is also text with a ![cool_image](https://i.imgur.com/zjjcJKZ.png) and another ![second cool_image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )

        
        new_nodes = split_nodes_image([node_one,node_two])
        
        expected =  [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
                TextNode("This is also text with a ", TextType.TEXT),
                TextNode("cool_image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second cool_image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ]
        self.assertEqual(new_nodes, expected)

    def test_split_images_no_images(self):
        node = TextNode("Just plain text here.", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        expected = [TextNode("Just plain text here.", TextType.TEXT)]
        self.assertEqual(new_nodes, expected)

    def test_split_images_image_at_start(self):
        node = TextNode("![alt](https://x.com/a.png) then text", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        expected = [
            TextNode("alt", TextType.IMAGE, "https://x.com/a.png"),
            TextNode(" then text", TextType.TEXT),
        ]
        self.assertEqual(new_nodes, expected)

    def test_split_images_image_at_end(self):
        node = TextNode("text then ![alt](https://x.com/a.png)", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        expected = [
            TextNode("text then ", TextType.TEXT),
            TextNode("alt", TextType.IMAGE, "https://x.com/a.png"),
        ]
        self.assertEqual(new_nodes, expected)

    def test_split_images_back_to_back(self):
        node = TextNode("![one](https://x.com/1.png)![two](https://x.com/2.png)", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        expected = [
            TextNode("one", TextType.IMAGE, "https://x.com/1.png"),
            TextNode("two", TextType.IMAGE, "https://x.com/2.png"),
        ]
        self.assertEqual(new_nodes, expected)

    def test_split_images_non_text_passthrough(self):
        node1 = TextNode("prefix ![alt](https://x.com/a.png) suffix", TextType.TEXT)
        node2 = TextNode("already image node", TextType.IMAGE, "https://x.com/existing.png")
        new_nodes = split_nodes_image([node1, node2])

        expected = [
            TextNode("prefix ", TextType.TEXT),
            TextNode("alt", TextType.IMAGE, "https://x.com/a.png"),
            TextNode(" suffix", TextType.TEXT),
            node2,
        ]
        self.assertEqual(new_nodes, expected)

    def test_split_images_alt_text_with_spaces(self):
        node = TextNode("look ![my cool image!](https://x.com/a.png) ok", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        expected = [
            TextNode("look ", TextType.TEXT),
            TextNode("my cool image!", TextType.IMAGE, "https://x.com/a.png"),
            TextNode(" ok", TextType.TEXT),
        ]
        self.assertEqual(new_nodes, expected)

    # ----------- Links (for when split_nodes_link is implemented) -----------

    def test_split_links_multiple(self):
        node = TextNode(
            "a [boot](https://www.boot.dev) and [yt](https://www.youtube.com)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        expected = [
            TextNode("a ", TextType.TEXT),
            TextNode("boot", TextType.LINK, "https://www.boot.dev"),
            TextNode(" and ", TextType.TEXT),
            TextNode("yt", TextType.LINK, "https://www.youtube.com"),
        ]
        self.assertEqual(new_nodes, expected)

    def test_split_links_edges(self):
        node = TextNode("[start](https://a.com) middle [end](https://b.com)", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        expected = [
            TextNode("start", TextType.LINK, "https://a.com"),
            TextNode(" middle ", TextType.TEXT),
            TextNode("end", TextType.LINK, "https://b.com"),
        ]
        self.assertEqual(new_nodes, expected)

    def test_split_links_breaks_when_link_text_appears_in_plain_text_first(self):
        node = TextNode(
            "boot then a link [boot](https://example.com) end",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])

        expected = [
            TextNode("boot then a link ", TextType.TEXT),
            TextNode("boot", TextType.LINK, "https://example.com"),
            TextNode(" end", TextType.TEXT),
        ]

        self.assertEqual(new_nodes, expected)

    def test_split_images_breaks_when_alt_text_appears_in_plain_text_first(self):
        node = TextNode(
            "alt then image ![alt](https://example.com/a.png) end",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])

        expected = [
            TextNode("alt then image ", TextType.TEXT),
            TextNode("alt", TextType.IMAGE, "https://example.com/a.png"),
            TextNode(" end", TextType.TEXT),
        ]

        self.assertEqual(new_nodes, expected)


    # def test_split_links_malformed_raises(self):
    #     node = TextNode("bad [link](https://a.com", TextType.TEXT)
    #     with self.assertRaises(ValueError):
    #         split_nodes_link([node])


if __name__ == "__main__":
    unittest.main()




