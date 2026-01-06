from .textnode import TextNode, TextType
from typing import Tuple,List, Dict, Callable
from enum import Enum

import re


IMG_ADJUST = 2  # for '!' and '['
LINK_ADJUST = 1 # for '['
IDX_ADJUST = 3 # for ']' '('  and ')'

# Just so I don't have to retype it a bunch of times
PIPELINE = [TextType.BOLD, TextType.ITALIC, TextType.CODE, TextType.IMAGE, TextType.LINK]


# These are all for type hinting
Extractor = Callable[[str], List[Tuple[str,str]]]
SplitBuilder = Callable[[List[TextNode]], List[TextNode]]

class BlockType (Enum):
    PARAGRAPH = 'p'
    HEADER = 'h'
    QUOTE = 'blockquote'
    CODE = 'code'
    UNORDERED_LIST = 'ul'
    ORDERED_LIST = 'ol'


# RegEx Helpers
def extract_markdown_images(text:str) -> List[Tuple[str,str]]:
    return re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    
def extract_markdown_links(text:str) -> List[Tuple[str,str]]:
    return re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)

# Mapping for RegEx Functions
EXTRACTOR: Dict[TextType,Extractor] = {
    TextType.IMAGE: extract_markdown_images,
    TextType.LINK: extract_markdown_links,

}

def extract_title(markdown):
    lines = markdown.split('\n')
    for line in lines:
        new_line = line.strip()
        if new_line.startswith('# '):
            return new_line[2:]
    
    raise Exception("Title Missing")



# Splitter Heplers
def make_delimiter_splitter(delimter:str, text_type:TextType) -> Callable[[List[TextNode]], List[TextNode]]:
    def split_nodes_delimiter(old_nodes:list[TextNode]) -> list[TextNode]:
        new_nodes = []
        for node_to_split in old_nodes:
            if node_to_split.text_type is not TextType.TEXT:
                new_nodes.append(node_to_split)
                continue
            
            # It's a type I can deal with
            node_text = node_to_split.text
            new_blocks = node_text.split(delimter)

            # No inline found
            if len(new_blocks) == 1:
                new_nodes.append(node_to_split)
                continue
            
            # malformed inline (no matching end)
            if len(new_blocks) % 2 == 0:
                raise ValueError("Malformed")

            # The if block statement allows me to remove trailing empty strings
            for idx,block in enumerate(new_blocks):
                if block:
                    new_nodes.append(TextNode(block, TextType.TEXT if idx % 2 == 0 else text_type))
        return new_nodes
    return split_nodes_delimiter
    
def make_img_link_splitter(text_type:TextType, adjuster:int) -> Callable[[List[TextNode]], List[TextNode]]:
    if not (text_type is TextType.LINK or text_type is TextType.IMAGE):
        raise ValueError("Improper Usage")
    
    def split_nodes_img_link_helper(old_nodes:List[TextNode]) -> List[TextNode]:
        new_nodes = []
        for node_to_split in old_nodes:
            # Edge Case - Nodes are already good
            if node_to_split.text_type != TextType.TEXT:
                new_nodes.append(node_to_split)
                continue


            # helper is defined above, its slightly different based on whether its a link or image
            list_of_items = EXTRACTOR[text_type](node_to_split.text)
            node_text = node_to_split.text
            current_index = 0

            for item in list_of_items:
                
                # This shouldn't ever happen, I can't get a test case to make it happen, but just in case
                if current_index >= len(node_text):
                    raise ValueError("Malfromed Text")

                first_txt = item[0]
                second_txt = item[1]

                # To account for the markdown characters

                temp_current_index = current_index
                while (True):
                    start_index = node_text.find(first_txt, temp_current_index)
                    if start_index == -1:
                        raise ValueError("Malformed Text")

                    if start_index > 0 and node_text[start_index-1] == '[':
                        start_index = start_index - adjuster
                        break
                    temp_current_index += max(len(first_txt),1)

                # This is actually the default case - when things are at the start or back to back this does not trigger (no empty texts)
                if current_index != start_index:
                    prefix_text = node_text[current_index:start_index]
                    prefix_node = TextNode(prefix_text,TextType.TEXT)
                    new_nodes.append(prefix_node)

                new_node = TextNode(first_txt,text_type,second_txt)
                new_nodes.append(new_node)

                # Update our current position
                current_index = (start_index + len(first_txt) + len(second_txt) + (adjuster+IDX_ADJUST))

            # Handles trailing text with no more links / images
            if current_index < len(node_text):
                new_nodes.append(TextNode(node_text[current_index:],TextType.TEXT))

        return new_nodes
    return split_nodes_img_link_helper

# Mapping for splitter functions
SPLIT_BUILDER: Dict[TextType, SplitBuilder] = {
    TextType.BOLD: make_delimiter_splitter('**', TextType.BOLD),
    TextType.ITALIC: make_delimiter_splitter('_', TextType.ITALIC),
    TextType.CODE: make_delimiter_splitter('`', TextType.CODE),
    TextType.IMAGE: make_img_link_splitter(TextType.IMAGE, IMG_ADJUST),
    TextType.LINK: make_img_link_splitter(TextType.LINK, LINK_ADJUST)

}

def markdown_to_blocks(markdown:str) -> List[str]:
    markdown = markdown.replace('\r',"")
    blocks = markdown.split('\n\n')
    new_blocks = [stripped_block for block in blocks if (stripped_block := block.strip()) != '']
    return new_blocks

def markdown_header_validator(markdown):
    if len(markdown) < 2:
        raise ValueError("Malformed Header Block") 
    current_char = 0
    
    while markdown[current_char] == '#':
        current_char += 1
    if current_char > 6 or markdown[current_char] != ' ':
        raise ValueError("Malformed Header Block")
    return BlockType.HEADER

def markdown_code_validator(markdown):
    if not markdown.endswith('```'):
        raise ValueError("Malformed Code Block") 
    return BlockType.CODE

def markdown_quote_validator(markdown):
    lines = markdown.split('\n')
    for line in lines:
        if not line.startswith('>'):
            raise ValueError("Malformed Quote Block")
    return BlockType.QUOTE

def markdown_unordered_list_validator(markdown):
    lines = markdown.split('\n')
    for line in lines:
        if not line.startswith('- '):
            raise ValueError("Malformed Unordered List Block")
    return BlockType.UNORDERED_LIST

def markdown_ordered_list_validator(markdown):
    previous_digit = 0
    lines = markdown.split('\n')
    for line in lines:
        if len(line) <= 2 or not line[0].isdigit() or not line[1] == '.' or not line[2] == ' ':
            raise ValueError("Malformed Ordered List Block")
        current_digit = int(line[0])
        if previous_digit + 1 != current_digit:
            raise ValueError("Malformed Ordered List Block")
        previous_digit = current_digit
    return BlockType.ORDERED_LIST


Validator = Callable[[str], BlockType]
VALIDATOR:Dict[BlockType,Validator] = {
    BlockType.HEADER: markdown_header_validator,
    BlockType.QUOTE: markdown_quote_validator,
    BlockType.CODE: markdown_code_validator,
    BlockType.UNORDERED_LIST: markdown_unordered_list_validator,
    BlockType.ORDERED_LIST: markdown_ordered_list_validator,
    BlockType.PARAGRAPH: lambda _: BlockType.PARAGRAPH,

}

def block_to_block_type(markdown:str) -> BlockType:
    if not markdown: raise ValueError("Empty Block")
    first_markdown_char = markdown[0]
    match first_markdown_char:
        case '#':
            validator = VALIDATOR[BlockType.HEADER]
        case '>':
            validator = VALIDATOR[BlockType.QUOTE]
        case '-': 
            validator = VALIDATOR[BlockType.UNORDERED_LIST]
        case _:
            if first_markdown_char.isdigit():
                validator = VALIDATOR[BlockType.ORDERED_LIST]
            elif markdown.startswith('```'):
                validator = VALIDATOR[BlockType.CODE]
            else:
                validator = VALIDATOR[BlockType.PARAGRAPH]
        
    return validator(markdown)



def trim_md_chars(block: str, block_type):
    updated_string = block
    if block_type == BlockType.QUOTE:   
        updated_string = updated_string.replace('\n> ', ' ')
        updated_string = updated_string.replace('> ', '')
    
    if block_type == BlockType.UNORDERED_LIST:
        lines = updated_string.split('\n')
        parts = [f'<li>{line[2:]}</li>' for line in lines]
        updated_string = "".join(parts)

    if block_type == BlockType.ORDERED_LIST:
        # print (repr(updated_string))
        lines = updated_string.split('\n')
        parts = [f'<li>{line[3:]}</li>' for line in lines]
        updated_string = "".join(parts)

    if block_type == BlockType.HEADER:
        space_char = updated_string.index(' ')
        updated_string = updated_string[space_char+1:]

    if block_type == BlockType.CODE:
        updated_string = updated_string.replace('```\n','')
        updated_string = updated_string.replace('\n```','\n')


    return updated_string