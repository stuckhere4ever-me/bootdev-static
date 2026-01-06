import unittest
from src.markdown_converter import markdown_to_html_node
from src.markdown_helpers import extract_title


class TestMarkdownToHtmlNodeQuick(unittest.TestCase):
    def test_paragraph(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here
"""
        expected = "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>"
        node = markdown_to_html_node(md)
        self.assertEqual(node.to_html(), expected)

    def test_quote(self):
        md = """
> This is a quote
> with **bold** and _italic_
> and `code`
"""
        expected = "<div><blockquote>This is a quote with <b>bold</b> and <i>italic</i> and <code>code</code></blockquote></div>"
        node = markdown_to_html_node(md)
        self.assertEqual(node.to_html(), expected)

    def test_unordered_list(self):
        md = """
- First item
- Second has **bold**
- Third has _italic_ and `code`
"""
        expected = "<div><ul><li>First item</li><li>Second has <b>bold</b></li><li>Third has <i>italic</i> and <code>code</code></li></ul></div>"
        node = markdown_to_html_node(md)
        self.assertEqual(node.to_html(), expected)

    def test_ordered_list(self):
        md = """
1. First item
2. Second has **bold**
3. Third has _italic_ and `code`
"""
        expected = "<div><ol><li>First item</li><li>Second has <b>bold</b></li><li>Third has <i>italic</i> and <code>code</code></li></ol></div>"
        node = markdown_to_html_node(md)
        self.assertEqual(node.to_html(), expected)

    def test_code_block(self):
        md = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
"""
        expected = "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>"
        node = markdown_to_html_node(md)
        self.assertEqual(node.to_html(), expected)

    def test_headers_h1_through_h6(self):
        cases = [
            ("# Header 1\n", "<div><h1>Header 1</h1></div>"),
            ("## Header 2\n", "<div><h2>Header 2</h2></div>"),
            ("### Header 3\n", "<div><h3>Header 3</h3></div>"),
            ("#### Header 4\n", "<div><h4>Header 4</h4></div>"),
            ("##### Header 5\n", "<div><h5>Header 5</h5></div>"),
            ("###### Header 6\n", "<div><h6>Header 6</h6></div>"),
        ]

        for md, expected in cases:
            node = markdown_to_html_node(md)
            self.assertEqual(node.to_html(), expected)

    # ---------- HEADERS ----------
    def test_single_header_h1(self):
        md = "# Hello\n"
        node = markdown_to_html_node(md)
        self.assertEqual(node.to_html(), "<div><h1>Hello</h1></div>")

    def test_single_header_h6(self):
        md = "###### Deep\n"
        node = markdown_to_html_node(md)
        self.assertEqual(node.to_html(), "<div><h6>Deep</h6></div>")

    def test_headers_mixed_levels(self):
        md = """
# H1

## H2

### H3
"""
        node = markdown_to_html_node(md)
        self.assertEqual(
            node.to_html(),
            "<div><h1>H1</h1><h2>H2</h2><h3>H3</h3></div>",
        )

    # ---------- PARAGRAPHS ----------
    def test_single_paragraph_no_inline(self):
        md = "Just a plain paragraph.\n"
        node = markdown_to_html_node(md)
        self.assertEqual(node.to_html(), "<div><p>Just a plain paragraph.</p></div>")

    def test_paragraph_multiple_lines_normalize(self):
        md = """
Line one
Line two
Line three
"""
        node = markdown_to_html_node(md)
        self.assertEqual(node.to_html(), "<div><p>Line one Line two Line three</p></div>")

    def test_paragraph_inline_combo(self):
        md = """
Hello **B** _I_ `C` end
"""
        node = markdown_to_html_node(md)
        self.assertEqual(
            node.to_html(),
            "<div><p>Hello <b>B</b> <i>I</i> <code>C</code> end</p></div>",
        )

    # ---------- QUOTES ----------
    def test_quote_single_line(self):
        md = """
> quoted text
"""
        node = markdown_to_html_node(md)
        self.assertEqual(node.to_html(), "<div><blockquote>quoted text</blockquote></div>")

    def test_quote_multiple_lines_with_inline(self):
        md = """
> first
> has **bold**
> and _italic_ and `code`
"""
        node = markdown_to_html_node(md)
        self.assertEqual(
            node.to_html(),
            "<div><blockquote>first has <b>bold</b> and <i>italic</i> and <code>code</code></blockquote></div>",
        )

    # ---------- UNORDERED LIST ----------
    def test_unordered_list_basic(self):
        md = """
- one
- two
- three
"""
        node = markdown_to_html_node(md)
        self.assertEqual(
            node.to_html(),
            "<div><ul><li>one</li><li>two</li><li>three</li></ul></div>",
        )

    def test_unordered_list_with_inline(self):
        md = """
- first has **bold**
- second has _italic_
- third has `code`
"""
        node = markdown_to_html_node(md)
        self.assertEqual(
            node.to_html(),
            "<div><ul><li>first has <b>bold</b></li><li>second has <i>italic</i></li><li>third has <code>code</code></li></ul></div>",
        )

    # ---------- ORDERED LIST ----------
    def test_ordered_list_basic(self):
        md = """
1. one
2. two
3. three
"""
        node = markdown_to_html_node(md)
        self.assertEqual(
            node.to_html(),
            "<div><ol><li>one</li><li>two</li><li>three</li></ol></div>",
        )

    def test_ordered_list_with_inline(self):
        md = """
1. first has **bold**
2. second has _italic_
3. third has `code`
"""
        node = markdown_to_html_node(md)
        self.assertEqual(
            node.to_html(),
            "<div><ol><li>first has <b>bold</b></li><li>second has <i>italic</i></li><li>third has <code>code</code></li></ol></div>",
        )

    # ---------- CODE BLOCKS ----------
    def test_codeblock_preserves_inline_markers(self):
        md = """
```
This has **bold** and _italic_ and `code`
and should NOT render those as HTML
```
"""
        node = markdown_to_html_node(md)
        self.assertEqual(
            node.to_html(),
            "<div><pre><code>This has **bold** and _italic_ and `code`\nand should NOT render those as HTML\n</code></pre></div>",
        )

    def test_codeblock_single_line(self):
        md = """
```
print("hi")
```
"""
        node = markdown_to_html_node(md)
        self.assertEqual(
            node.to_html(),
            '<div><pre><code>print("hi")\n</code></pre></div>',
        )

    # ---------- LINKS / IMAGES IN PARAGRAPHS ----------
    def test_paragraph_with_link(self):
        md = """
This is a [link](https://example.com) ok
"""
        node = markdown_to_html_node(md)
        self.assertEqual(
            node.to_html(),
            '<div><p>This is a <a href="https://example.com">link</a> ok</p></div>',
        )

    def test_paragraph_with_image(self):
        md = """
Start ![alt](https://img.com/a.png) end
"""
        node = markdown_to_html_node(md)
        self.assertEqual(
            node.to_html(),
            '<div><p>Start <img src="https://img.com/a.png" alt="alt" /> end</p></div>',
        )

    def test_paragraph_with_link_and_image(self):
        md = """
Go [here](https://a.com) and see ![pic](https://b.com/p.png)
"""
        node = markdown_to_html_node(md)
        self.assertEqual(
            node.to_html(),
            '<div><p>Go <a href="https://a.com">here</a> and see <img src="https://b.com/p.png" alt="pic" /></p></div>',
        )

    # ---------- MIXED DOCS ----------
    def test_mixed_blocks_all_types(self):
        md = """
# Title

A paragraph with **bold** and a [link](https://x.com)

> Quote with _italic_

- item 1
- item 2

1. first
2. second

```
code **not bold**
```
"""
        node = markdown_to_html_node(md)
        self.assertEqual(
            node.to_html(),
            '<div>'
            '<h1>Title</h1>'
            '<p>A paragraph with <b>bold</b> and a <a href="https://x.com">link</a></p>'
            '<blockquote>Quote with <i>italic</i></blockquote>'
            '<ul><li>item 1</li><li>item 2</li></ul>'
            '<ol><li>first</li><li>second</li></ol>'
            '<pre><code>code **not bold**\n</code></pre>'
            '</div>',
        )

    # ---------- “MAY BREAK” STYLE TESTS ----------
    def test_ordered_list_requires_incrementing(self):
        md = """
1. one
3. three
"""
        with self.assertRaises(ValueError):
            markdown_to_html_node(md)

    def test_unordered_list_requires_dash_space(self):
        md = """
-item
- ok
"""
        with self.assertRaises(ValueError):
            markdown_to_html_node(md)

    def test_quote_requires_all_lines_start_with_gt(self):
        md = """
> ok
nope
"""
        with self.assertRaises(ValueError):
            markdown_to_html_node(md)

    def test_malformed_header_missing_space(self):
        md = "##Bad\n"
        with self.assertRaises(ValueError):
            markdown_to_html_node(md)

    def test_malformed_codeblock_missing_end(self):
        md = """
```
no end fence
"""
        with self.assertRaises(ValueError):
            markdown_to_html_node(md)


    def test_extract_headers(self):
        md = "# Hello"
        result = extract_title(md)
        expected = "Hello"
        self.assertEqual(result, expected)

    def test_extract_headers_fail(self):
        md = "Hello"
        with self.assertRaises(Exception):
            extract_title(md)
 
    def test_extract_headers_space_lead(self):
        md = " # Hello"
        result = extract_title(md)
        expected = "Hello"
        self.assertEqual(result, expected)

    def test_extract_headers_space_trail(self):
        md = "# Hello "
        result = extract_title(md)
        expected = "Hello"
        self.assertEqual(result, expected)

    def test_extract_headers_space_malformed(self):
        md = "#Hello  "
        with self.assertRaises(Exception):
            extract_title(md)



if __name__ == "__main__":
    unittest.main()
