import unittest

from src.textnode import TextNode, TextType
from src.markdown_converter import text_to_text_blocks  


class TestTextToTextBlocks(unittest.TestCase):
    def test_plain_text(self):
        text = "Just plain text."
        expected = [TextNode("Just plain text.", TextType.TEXT)]
        self.assertEqual(text_to_text_blocks(text), expected)

    def test_bold_only(self):
        text = "This is **bold** text."
        expected = [
            TextNode("This is ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" text.", TextType.TEXT),
        ]
        self.assertEqual(text_to_text_blocks(text), expected)

    def test_italic_only(self):
        text = "This is _italic_ text."
        expected = [
            TextNode("This is ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" text.", TextType.TEXT),
        ]
        self.assertEqual(text_to_text_blocks(text), expected)

    def test_code_only(self):
        text = "This is `code` text."
        expected = [
            TextNode("This is ", TextType.TEXT),
            TextNode("code", TextType.CODE),
            TextNode(" text.", TextType.TEXT),
        ]
        self.assertEqual(text_to_text_blocks(text), expected)

    def test_link_only(self):
        text = "A [link](https://example.com)."
        expected = [
            TextNode("A ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://example.com"),
            TextNode(".", TextType.TEXT),
        ]
        self.assertEqual(text_to_text_blocks(text), expected)

    def test_image_only(self):
        text = "![alt](https://example.com/a.png)"
        expected = [
            TextNode("alt", TextType.IMAGE, "https://example.com/a.png"),
        ]
        self.assertEqual(text_to_text_blocks(text), expected)

    def test_mixed_all_features(self):
        text = "Hi **B** _I_ `C` [L](https://l.com) ![A](https://i.com/a.png) end"
        expected = [
            TextNode("Hi ", TextType.TEXT),
            TextNode("B", TextType.BOLD),
            TextNode(" ", TextType.TEXT),
            TextNode("I", TextType.ITALIC),
            TextNode(" ", TextType.TEXT),
            TextNode("C", TextType.CODE),
            TextNode(" ", TextType.TEXT),
            TextNode("L", TextType.LINK, "https://l.com"),
            TextNode(" ", TextType.TEXT),
            TextNode("A", TextType.IMAGE, "https://i.com/a.png"),
            TextNode(" end", TextType.TEXT),
        ]
        self.assertEqual(text_to_text_blocks(text), expected)

    def test_multiple_links(self):
        text = "Go [one](https://a.com) and [two](https://b.com) now"
        expected = [
            TextNode("Go ", TextType.TEXT),
            TextNode("one", TextType.LINK, "https://a.com"),
            TextNode(" and ", TextType.TEXT),
            TextNode("two", TextType.LINK, "https://b.com"),
            TextNode(" now", TextType.TEXT),
        ]
        self.assertEqual(text_to_text_blocks(text), expected)

    def test_multiple_images(self):
        text = "Pics: ![one](https://x.com/1.png) and ![two](https://x.com/2.png)"
        expected = [
            TextNode("Pics: ", TextType.TEXT),
            TextNode("one", TextType.IMAGE, "https://x.com/1.png"),
            TextNode(" and ", TextType.TEXT),
            TextNode("two", TextType.IMAGE, "https://x.com/2.png"),
        ]
        self.assertEqual(text_to_text_blocks(text), expected)

    def test_back_to_back_images(self):
        text = "![one](https://x.com/1.png)![two](https://x.com/2.png)"
        expected = [
            TextNode("one", TextType.IMAGE, "https://x.com/1.png"),
            TextNode("two", TextType.IMAGE, "https://x.com/2.png"),
        ]
        self.assertEqual(text_to_text_blocks(text), expected)

    def test_image_then_text(self):
        text = "![alt](https://x.com/a.png) then text"
        expected = [
            TextNode("alt", TextType.IMAGE, "https://x.com/a.png"),
            TextNode(" then text", TextType.TEXT),
        ]
        self.assertEqual(text_to_text_blocks(text), expected)

    def test_text_then_image(self):
        text = "text then ![alt](https://x.com/a.png)"
        expected = [
            TextNode("text then ", TextType.TEXT),
            TextNode("alt", TextType.IMAGE, "https://x.com/a.png"),
        ]
        self.assertEqual(text_to_text_blocks(text), expected)

    def test_link_at_start_and_end(self):
        text = "[start](https://a.com) middle [end](https://b.com)"
        expected = [
            TextNode("start", TextType.LINK, "https://a.com"),
            TextNode(" middle ", TextType.TEXT),
            TextNode("end", TextType.LINK, "https://b.com"),
        ]
        self.assertEqual(text_to_text_blocks(text), expected)

    def test_malformed_bold_raises(self):
        text = "This is **broken"
        with self.assertRaises(ValueError):
            text_to_text_blocks(text)

    def test_malformed_italic_raises(self):
        text = "This is _broken"
        with self.assertRaises(ValueError):
            text_to_text_blocks(text)

    def test_malformed_code_raises(self):
        text = "This is `broken"
        with self.assertRaises(ValueError):
            text_to_text_blocks(text)


if __name__ == "__main__":
    unittest.main()
