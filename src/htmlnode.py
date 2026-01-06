from __future__ import annotations
from typing import Sequence, Dict, Callable
from .textnode import TextNode, TextType
LEAF_TAGS = ["p", "b", "i", "a", "img", "code", "blockquote", "h1", "h2", "h3", "h4", "h5", "h6", "li", "span"]

LeafBuilder = Callable[[TextNode], "LeafNode"]

# Leaf Node Helpers
def text_leaf(n:TextNode) -> LeafNode:
    return LeafNode(None, n.text.replace('\n'," ")) # Strip newlines in paragraphs

def simple_leaf(n:TextNode) -> LeafNode:
    return LeafNode(n.text_type.value, n.text)

def image_leaf(n:TextNode) -> LeafNode:
    if n.url is None:
        raise ValueError("Image must contain a URL")
    return LeafNode(TextType.IMAGE.value, "",  {'src':n.url, 'alt':n.text})

def link_leaf(n:TextNode) -> LeafNode:
    if n.url is None:
        raise ValueError("Link Must contain a URL")
    return LeafNode(TextType.LINK.value, n.text, {'href':n.url})

# Mapping for Leaf Node Functions 
LEAF_BUILDER: Dict[TextType, LeafBuilder] = {
    TextType.LINK: link_leaf,
    TextType.IMAGE: image_leaf,
    TextType.TEXT: text_leaf,
    TextType.BOLD: simple_leaf,
    TextType.ITALIC: simple_leaf,
    TextType.CODE: simple_leaf,
}


class HTMLNode():
    def __init__(
            self, tag:str | None = None, 
            value:str | None = None, 
            children: Sequence[HTMLNode] | None = None, 
            props:dict[str,str] | None= None):
        
        self.tag = tag
        self.value = value
        self.children = None if children is None else list(children)
        self.props = props

    # Child Classes will override
    def to_html(self) -> str:
        raise NotImplemented
    
    def props_to_html(self) -> str:
        
        if not self.props or len(self.props) == 0:
            return ''
        
        sorted_props = sorted(self.props)
        if self.tag == 'img' and 'src' in sorted_props:
            src_idx = sorted_props.index('src')
            src_info = sorted_props[src_idx]
            del sorted_props[src_idx]
            sorted_props.insert(0,src_info)

            if 'alt' in sorted_props:
                alt_idx = sorted_props.index('alt')
                alt_info = sorted_props[alt_idx]
                del sorted_props[alt_idx]
                sorted_props.insert(1,alt_info)

        if self.tag == 'a' and 'href' in sorted_props:
            href_idx = sorted_props.index('href')
            href_info = sorted_props[href_idx]
            del sorted_props[href_idx]
            sorted_props.insert(0,href_info)


        parts = [f'{prop}="{self.props[prop]}"' for prop in sorted_props]


        return ' ' + ' '.join(parts)

    def __eq__(self, other:object) -> bool:
        if not isinstance(other,HTMLNode):
            return NotImplemented


        
        return ( self.tag == other.tag and 
                 self.value == other.value and 
                 self.children == other.children and
                 self.props == other.props
        )

    def __repr__(self) -> str:
        html_repr = "HTMLNode"
        tag_repr = ("None" if self.tag is None else f", {self.tag}")
        val_repr = ("None" if self.value is None else f", {self.value}")
        children_repr = ("None" if self.children is None else f", {self.children}")
        props_repr = ("None" if self.props is None else f", {self.props}")
        
        return f"{html_repr}(Tag: {tag_repr}, Val: {val_repr}, Children: {children_repr}, Properties: {props_repr})"




class LeafNode(HTMLNode):
    def __init__(
            self, tag:str | None, 
            value:str , 
            props:dict[str,str] | None= None
        ):
        super().__init__(tag=tag, value=value, children=None, props=props)

    def to_html(self) -> str:
        if self.value is None:
            raise ValueError("Leaf Node MUST contain a value")
        
        if self.tag is None:
            return self.value
        
        if self.tag not in LEAF_TAGS:
            raise TypeError("Invalid Leaf Tag")

        props_string = self.props_to_html()

        if self.tag == 'img':
            rendered_html = f'<{self.tag}{props_string} />'
        else:    
            rendered_html = f'<{self.tag}{props_string}>{self.value}</{self.tag}>'
        
        return rendered_html


class ParentNode(HTMLNode):
    def __init__(
            self, tag:str, 
            children:Sequence[HTMLNode], 
            props:dict[str,str] | None= None):
        
        if not children:
            raise ValueError("Parent Node MUST contain Children")
        
        if tag is None:
            raise ValueError("Parent Node MUST contain a Tag")
        
        if children is None:
            raise ValueError("Parent Node MUST contain Children")
        
        super().__init__(tag=tag, value=None, children=children, props=props)


    def to_html(self) -> str:

        assert self.tag is not None
        assert self.children is not None
        
        props_string = self.props_to_html()

        html_open = f'<{self.tag}{props_string}>'
        html_close = f'</{self.tag}>'
        parts = [child.to_html() for child in self.children]

        return html_open + "".join(parts) + html_close
