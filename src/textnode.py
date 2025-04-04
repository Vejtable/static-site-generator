from htmlnode import LeafNode
from enum import Enum


class TextType(Enum):       ## Enumeration of text types, each representing a distinct HTML element of text formatting style.
    TEXT = "text"           # Plain text
    BOLD = "bold"           # Bold text,                    <b>
    ITALIC = "italic"       # Italicized text,              <i>
    CODE = "code"           # Code block or inline code,    <code>
    LINK = "link"           # Hyperlink,                    <a href>        <="a hypertext reference"
    IMAGE = "image"         # Image element,                <img>


class TextNode:                                        ## Represents a unit of formatted text, including plain, blod, italic, code, links, and images.
    def __init__(self, text, text_type, url=None):     # Inittialize a TextNode with text content, type, and an optional URL (for links and images)
        self.text = text                               # The main content of the node (the displayed text)
        self.text_type = text_type                     # The type of text (TextType Enum)
        self.url = url                                 # Optional URL for 'link' or 'image' types

    def __eq__(self, other):                           # Redefines the `__eq__` method (used with `==`) to specify the conditions for two objects to be considered "equal."
        return (self.text_type == other.text_type
            and self.text == other.text
            and self.url == other.url)

    def __repr__(self):                                # Provides a developer-friendly string representation of the TextNode instance.
        return f"TextNode({self.text}, {self.text_type.value}, {self.url})"


def text_node_to_html_node(text_node):                                              ## Converts a TextNode object into a LeafNode HTML representation based on its text_type.
    if text_node.text_type == TextType.TEXT:                                        # 'plain text', (no tag)
        return LeafNode(None, text_node.text) 
    if text_node.text_type == TextType.BOLD:                                        # 'bold text', (<b>)
        return LeafNode("b", text_node.text)  
    if text_node.text_type == TextType.ITALIC:                                      # 'italic text', (<i>)
        return LeafNode("i", text_node.text) 
    if text_node.text_type == TextType.CODE:                                        # 'code text', (<code>)
        return LeafNode("code", text_node.text)   
    if text_node.text_type == TextType.LINK:                                        # 'link text', (<a> with href)
        return LeafNode("a", text_node.text, {"href": text_node.url})  
    if text_node.text_type == TextType.IMAGE:                                       # 'image text', (<img> with src and alt)
        return LeafNode("img", "", {"src": text_node.url, "alt": text_node.text})   
    raise ValueError(f"invalid text type: {text_node.text_type}")                   # Raise an error for unsupported or invalid text types