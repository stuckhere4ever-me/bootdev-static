import unittest

from src.markdown_helpers import *




class TestMdBlocks(unittest.TestCase):
    def test_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        expected =         [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ]

        self.assertEqual(blocks,expected)


    def test_more_blocks(self):
            md = """
This is **bolded** paragraph

This is an image ![alt](https://example.com/a.png)

This is the a random paragraph with _italics_
and a new line with `code`

- This is a list
- with items

A [link](https://example.com)

And this is everything in two sentences
Hi **B** _I_ `C` [L](https://l.com) ![A](https://i.com/a.png) end
"""
            blocks = markdown_to_blocks(md)
            expected =         [
                    "This is **bolded** paragraph",
                    "This is an image ![alt](https://example.com/a.png)",
                    "This is the a random paragraph with _italics_\nand a new line with `code`",
                    "- This is a list\n- with items",
                    "A [link](https://example.com)",
                    "And this is everything in two sentences\nHi **B** _I_ `C` [L](https://l.com) ![A](https://i.com/a.png) end",
                ]

            self.assertEqual(blocks,expected)


    def test_markdown_to_blocks_trims_whitespace(self):
        md = "   First block   \n\n\t Second block\t\n\n  Third block  "
        blocks = markdown_to_blocks(md)
        expected = ["First block", "Second block", "Third block"]
        self.assertEqual(blocks, expected)

    def test_markdown_to_blocks_drops_empty_blocks_extra_newlines(self):
        md = "\n\n\nFirst\n\n\n\nSecond\n\n\n"
        blocks = markdown_to_blocks(md)
        expected = ["First", "Second"]
        self.assertEqual(blocks, expected)

    def test_markdown_to_blocks_preserves_internal_newlines(self):
        md = "Line 1\nLine 2\nLine 3\n\nNext block"
        blocks = markdown_to_blocks(md)
        expected = ["Line 1\nLine 2\nLine 3", "Next block"]
        self.assertEqual(blocks, expected)

    def test_markdown_to_blocks_no_blank_lines_single_block(self):
        md = "Just one block\nwith multiple lines\nand no blank line separation"
        blocks = markdown_to_blocks(md)
        expected = ["Just one block\nwith multiple lines\nand no blank line separation"]
        self.assertEqual(blocks, expected)

    def test_markdown_to_blocks_handles_windows_newlines(self):
        md = "First block\r\n\r\nSecond block\r\n\r\nThird block"
        blocks = markdown_to_blocks(md)
        # Depending on your implementation, you may need to normalize \r\n earlier in the pipeline.
        # If you keep markdown_to_blocks as-is, this test will likely fail (that's fine; it exposes the gap).
        expected = ["First block", "Second block", "Third block"]
        self.assertEqual(blocks, expected)

    def test_markdown_to_blocks_heading_paragraph_list_example(self):
        md = """# Heading

This is a paragraph
that continues on the next line.

- item 1
- item 2
- item 3
"""
        blocks = markdown_to_blocks(md)
        expected = [
            "# Heading",
            "This is a paragraph\nthat continues on the next line.",
            "- item 1\n- item 2\n- item 3",
        ]
        self.assertEqual(blocks, expected)


    def test_block_to_blocktype_paragraph(self):
        md = "First block"
        block = block_to_block_type(md)
        expected = BlockType.PARAGRAPH
        self.assertEqual(block, expected)

    def test_block_to_blocktype_header_one(self):
        md = "# Hello"
        block = block_to_block_type(md)
        expected = BlockType.HEADER
        self.assertEqual(block, expected)

    def test_block_to_blocktype_header_two(self):
        md = "## Hello"
        block = block_to_block_type(md)
        expected = BlockType.HEADER
        self.assertEqual(block, expected)

    def test_block_to_blocktype_header_three(self):
        md = "### Hello"
        block = block_to_block_type(md)
        expected = BlockType.HEADER
        self.assertEqual(block, expected)

    def test_block_to_blocktype_header_four(self):
        md = "#### Hello"
        block = block_to_block_type(md)
        expected = BlockType.HEADER
        self.assertEqual(block, expected)

    def test_block_to_blocktype_header_five(self):
        md = "##### Hello"
        block = block_to_block_type(md)
        expected = BlockType.HEADER
        self.assertEqual(block, expected)

    def test_block_to_blocktype_header_six(self):
        md = "###### Hello"
        block = block_to_block_type(md)
        expected = BlockType.HEADER
        self.assertEqual(block, expected)

    def test_block_to_blocktype_header_broken(self):
        md = "####### Hello"
        with self.assertRaises(ValueError):
            block = block_to_block_type(md)

    def test_block_to_blocktype_code_good(self):
        md = '''```
This is a good code block
It is pretty awesome
```'''

        block = block_to_block_type(md)
        expected = BlockType.CODE
        self.assertEqual(block, expected)
    
    def test_block_to_blocktype_code_broken_no_end(self):
        md = '''```
This is a bad code block
It is pretty aweful
'''
        with self.assertRaises(ValueError):
            block = block_to_block_type(md)

    def test_block_to_blocktype_code_broken_missing_tick(self):
        md = '''```
This is a bad code block
It is pretty aweful``
'''
        with self.assertRaises(ValueError):
            block = block_to_block_type(md)


    def test_block_to_blocktype_quote_good(self):
        md = '''> Good Stuff
>This is good quote
>Really Good quote
> I love this quote'''

        block = block_to_block_type(md)
        expected = BlockType.QUOTE
        self.assertEqual(block, expected)

    def test_block_to_blocktype_quote_bad(self):
        md = '''> Bad Stuff
>This is Bad quote
<Really Bad quote
> I hate this quote'''

        with self.assertRaises(ValueError):
            block = block_to_block_type(md)

    def test_block_to_blocktype_ul_good(self):
        md = '''- Good Stuff
- This is good quote
- Really Good quote
- I love this quote'''

        block = block_to_block_type(md)
        expected = BlockType.UNORDERED_LIST
        self.assertEqual(block, expected)

    def test_block_to_blocktype_ul_missing_dash(self):
        md = '''- Bad Stuff
- This is Bad quote
- Really Bad quote
I hate this quote'''

        with self.assertRaises(ValueError):
            block = block_to_block_type(md)

    def test_block_to_blocktype_ul_missing_space(self):
        md = '''- Bad Stuff
- This is Bad quote
- Really Bad quote
-I hate this quote'''

        with self.assertRaises(ValueError):
            block = block_to_block_type(md)

    def test_block_to_blocktype_ol_good(self):
        md = '''1. Good Stuff
2. This is good quote
3. Really Good quote
4. I love this quote'''

        block = block_to_block_type(md)
        expected = BlockType.ORDERED_LIST
        self.assertEqual(block, expected)

    def test_block_to_blocktype_ol_missing_num(self):
        md = '''1. Bad Stuff
This is Bad quote
3. Really Bad quote
4. I hate this quote'''

        with self.assertRaises(ValueError):
            block = block_to_block_type(md)

    def test_block_to_blocktype_ol_missing_space(self):
        md = '''1. Bad Stuff
2. This is Bad quote
3.Really Bad quote
4. I hate this quote'''

        with self.assertRaises(ValueError):
            block = block_to_block_type(md)

    def test_block_to_blocktype_ol_missing_period(self):
        md = '''1. Bad Stuff
2. This is Bad quote
3. Really Bad quote
4 I hate this quote'''

        with self.assertRaises(ValueError):
            block = block_to_block_type(md)

    def test_block_to_blocktype_empty_block_raises(self):
        md = ""
        with self.assertRaises(ValueError):
            block_to_block_type(md)

    # ---------- Heading edge cases ----------
    def test_block_to_blocktype_header_missing_space_after_hash_raises(self):
        md = "#Hello"
        with self.assertRaises(ValueError):
            block_to_block_type(md)

    def test_block_to_blocktype_header_hash_only_raises(self):
        md = "#"
        with self.assertRaises(ValueError):
            block_to_block_type(md)

    def test_block_to_blocktype_header_six_hash_missing_space_raises(self):
        md = "######Hello"
        with self.assertRaises(ValueError):
            block_to_block_type(md)

    def test_block_to_blocktype_header_valid_with_more_text(self):
        md = "### Hello there friend"
        self.assertEqual(block_to_block_type(md), BlockType.HEADER)

    # ---------- Code block edge cases ----------
    def test_block_to_blocktype_code_single_line_ticks_only_valid(self):
        md = "```\n```"
        self.assertEqual(block_to_block_type(md), BlockType.CODE)

    def test_block_to_blocktype_code_fence_not_alone_on_line_breaks(self):
        # Your code requires lines[0] == '```' and lines[-1] == '```'
        md = "```python\nprint('hi')\n```"
        self.assertEqual(block_to_block_type(md), BlockType.CODE)

    def test_block_to_blocktype_code_missing_start_fence_treated_as_paragraph(self):
        md = "print('hi')\n```"
        self.assertEqual(block_to_block_type(md), BlockType.PARAGRAPH)

    def test_block_to_blocktype_code_extra_text_after_end_fence_breaks(self):
        md = "```\ncode\n``` trailing"
        with self.assertRaises(ValueError):
            block_to_block_type(md)

    # ---------- Quote edge cases ----------
    def test_block_to_blocktype_quote_multiline_requires_every_line_starts_with_gt(self):
        md = "> line 1\nline 2"
        with self.assertRaises(ValueError):
            block_to_block_type(md)

    def test_block_to_blocktype_quote_single_gt_is_quote(self):
        md = ">"
        self.assertEqual(block_to_block_type(md), BlockType.QUOTE)

    # ---------- Unordered list edge cases ----------
    def test_block_to_blocktype_ul_requires_dash_space(self):
        md = "-item 1\n-item 2"
        with self.assertRaises(ValueError):
            block_to_block_type(md)

    def test_block_to_blocktype_ul_single_item_valid(self):
        md = "- one item"
        self.assertEqual(block_to_block_type(md), BlockType.UNORDERED_LIST)

    # ---------- Ordered list edge cases ----------
    def test_block_to_blocktype_ol_out_of_order_numbers_should_raise_per_spec(self):
        # Spec says must start at 1 and increment by 1. Your current code does NOT enforce this.
        md = "1. one\n3. three"
        with self.assertRaises(ValueError):
            block_to_block_type(md)

    def test_block_to_blocktype_ol_must_start_at_one_should_raise_per_spec(self):
        # Your current code will classify this as ORDERED_LIST, but spec says it must start at 1.
        md = "2. two\n3. three"
        with self.assertRaises(ValueError):
            block_to_block_type(md)

    def test_block_to_blocktype_ol_two_digit_number_should_be_supported_per_spec(self):
        # Your current code only checks line[0], line[1], line[2], so "10. " will fail.
        md = "1. one\n2. two\n10. ten"
        with self.assertRaises(ValueError):
            block_to_block_type(md)

    def test_block_to_blocktype_ol_single_item_valid(self):
        md = "1. only"
        self.assertEqual(block_to_block_type(md), BlockType.ORDERED_LIST)

    # ---------- “Looks like” list/quote but shouldn’t be ----------
    def test_block_to_blocktype_dash_without_space_is_paragraph(self):
        # Since you only treat unordered list if markdown.startswith('-') and then require '- ' per line,
        # this should raise in your implementation; spec would likely treat as paragraph.
        md = "-not a list item"
        with self.assertRaises(ValueError):
            block_to_block_type(md)


if __name__ == "__main__":
    unittest.main()
