from .textnode import TextNode, TextType
from .htmlnode import LeafNode, HTMLNode, ParentNode, LEAF_BUILDER
from typing import List
# from .markdown_helpers import LEAF_BUILDER, SPLIT_BUILDER, PIPELINE
from .markdown_helpers import *


# LEAF_BUILDER is what does all the work here
def text_node_to_html_node(node:TextNode) -> LeafNode:
    leaf_func = LEAF_BUILDER.get(node.text_type)
    if leaf_func is None:
        raise TypeError ("Invalid Text Type")
    return leaf_func(node)

    
# SPLIT_BUILDER is what does all the work here
def text_to_text_blocks(text:str) -> List[TextNode]:
    node_list = [TextNode(text, TextType.TEXT)]
    for text_type in PIPELINE:
        delimiter_function = SPLIT_BUILDER[text_type]
        node_list = delimiter_function(node_list)

    return node_list

# Consideration - We can build out a HTML_Builder Mapping similar to what we did with LeafBuilder, but I think it'll be two layers
# I don't really want to flex my inner SML so lets leave it be for now
def markdown_to_html_node(md:str) -> HTMLNode:
    list_of_html_nodes = []
    md_blocks = markdown_to_blocks(md)


    for md_block in md_blocks:
        md_block_type = block_to_block_type(md_block)
        updated_block = trim_md_chars(md_block, md_block_type)

        
        # Kinda ugly - might be a better way to do this
        if md_block_type != BlockType.CODE and md_block_type != BlockType.HEADER:
            my_children = build_children(updated_block)
            list_of_html_nodes.append(ParentNode(md_block_type.value, my_children, None))

        elif md_block_type == BlockType.HEADER:
            num_hashes = md_block.index(' ')
            my_children = build_children(updated_block)
            list_of_html_nodes.append(ParentNode(f'{md_block_type.value}{num_hashes}', my_children, None))
         

        else:  # Code
            txt_node = TextNode(updated_block, TextType.CODE)
            code_leaf = text_node_to_html_node(txt_node)
            code_parent = ParentNode('pre', [code_leaf], None)
            list_of_html_nodes.append(code_parent)

    final_node = ParentNode('div', list_of_html_nodes, None)
    return final_node    

def build_children(md_block):
    html_children = []
    list_of_txt_blocks = text_to_text_blocks(md_block)

    for block in list_of_txt_blocks:
        html_children.append(text_node_to_html_node(block))

    return html_children



    