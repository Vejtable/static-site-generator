class HTMLNode:                                                              ## Base class represents a generic HTML node, forming a templat for all specific node types to inheret from.
    def __init__(self, tag=None, value=None, children=None, props=None):     # Initializes with attributes common to all HTML nodes.
        self.tag = tag                                                       # 'tag' is the HTML tag name (e.g, "div", "p", "span") - or None for non-element nodes.
        self.value = value                                                   # 'value' is the text content inside the node (if any) - typically used by text and leaf nodes.
        self.children = children                                             # 'children' is a list of child HTMLNode objects (nested nodes) - for non-leaf nodes.
        self.props = props                                                   # 'props' is a dictionary of HTML attributes for the node.

    def to_html(self):    ## Effectively signs a "contract" in which all inheretors of this class are required to implement a 'to_html' function
        raise NotImplementedError("to_html method not implemented")

    def props_to_html(self):      ## Converts dictionary of attributes (self.props) into string of HTML attributes: {"class": "header", "id": "main"} -> ' class="header" id="main"'
        if self.props is None:                                # If no props are provided,
            return ""                                         #   return an empty string
        props_html = ""                                       # Initialize a string to accumulalte key-value pairs in the dictionary
        for prop in self.props:                               # Iterate over all key-value pairs in the dictionary,
            props_html += f' {prop}="{self.props[prop]}"'     #   format and append each key-value pair
        return props_html
    
    def __repr__(self):                                       # Provides a developer-friendly string representation of the HTMLNode instance.
        return f"HTMLNode({self.tag}, {self.value}, children: {self.children}, {self.props})"


class LeafNode(HTMLNode):                             ## LeafNode represents a terminal node in the HTML tree.  Has a 'tag' and a 'value', but no children.
    def __init__(self, tag, value, props=None):       # Initializes a LeafNode - requiring 'tag' and 'value'
        super().__init__(tag, value, None, props)     #   may optionally have 'props' - a dictionary of tag properties/attributes

    def to_html(self):                                                            # Converts the LeafNode to its HTML string representation
        if self.value is None:                                                    # LeafNode must have content to render,
            raise ValueError("invalid HTML: no value")                            #   raises an error if that is not the case
        if self.tag is None:                                                      # If there is no tag ("plain text" instead of "<p>plain text</p>",
            return self.value                                                     #   return the value directly
        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"     # Wrap the value with the HTML opening and closing tags, including optional attributes.

    def __repr__(self):                                                           # Provides a developer-friendly string representation of the LeafNode instance.
        return f"LeafNode({self.tag}, {self.value}, {self.props})"


class ParentNode(HTMLNode):                           ## ParentNode represents an HTML node with child nodes, allowing nested HTML structures.
    def __init__(self, tag, children, props=None):    # Initialize the ParentNode with an HTML tag, a list of child nodes, and optional attributes,
        super().__init__(tag, None, children, props)  #   'tag': the HTML element's type - 'children': a list of child HTMLNode instances - 'props': dictionary of optional HTML attributes

    def to_html(self):                                                                # Converts the ParentNode and all its children into a complete HTML string
        if self.tag is None:                                                          # Ensure the node has a valid HTML tag,
            raise ValueError("invalid HTML: no tag")                                  #   raise an error if that is not the case
        if self.children is None:                                                     # Ensure the node has children,
            raise ValueError("invalid HTML: no children")                             #   raise an error if that is not the case
        children_html = ""                                                            # Initiate a list of children,
        for child in self.children:                                                   #   look for children,
            children_html += child.to_html()                                          #   call `to_html` on the children
        return f"<{self.tag}{self.props_to_html()}>{children_html}</{self.tag}>"      # Create the complete HTML element by combining the tag, attributes, and the rendered children

    def __repr__(self):                                                               # Provides a developer-friendly string representation of the ParentNode instance.
        return f"ParentNode({self.tag}, children: {self.children}, {self.props})"