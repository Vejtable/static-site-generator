from enum import Enum

from htmlnode import ParentNode
from inline_markdown import text_to_textnodes
from textnode import text_node_to_html_node, TextNode, TextType


class BlockType(Enum):          ##  Enumeration of Markdown block types
    PARAGRAPH = "paragraph"     # Standard block of text
    HEADING = "heading"         # Heading block with one or more `#`
    CODE = "code"               # Multiline code block (encased in ```...```)
    QUOTE = "quote"             # Blockquote starting with `>`
    OLIST = "ordered_list"      # Ordered list (lines starting with 1., 2., etc.)
    ULIST = "unordered_list"    # Unordered list (lines starting with `'`)


def markdown_to_blocks(markdown):           ## Splits Markdown into isolated blocks by double line breaks
    blocks = markdown.split("\n\n")         # Break on double new lines
    filtered_blocks = []                    # Holds non-empty blocks
    for block in blocks:                    # Iterates each block,
        if block == "":                     #   skip empty block
            continue                        
        block = block.strip()               # Remove unnecessary white space
        filtered_blocks.append(block)       # Add cleaned block to the list
    return filtered_blocks                  # Returns all cleaned Markdown blocks


def block_to_block_type(block):                                                             ## Determines the type of a Markdown block
    lines = block.split("\n")                                                               # Splits the block into individual lines

    if block.startswith(("# ", "## ", "### ", "#### ", "##### ", "###### ")):               # If block starts with 1-6 `#`,
        return BlockType.HEADING                                                            #   block is a markdown heading

    if len(lines) > 1 and lines[0].startswith("```") and lines[-1].startswith("```"):       # If block is more than 1 line, and starts + ends with ```,
        return BlockType.CODE                                                               #   block is fenced code block

    if block.startswith(">"):                                                               # If block starts with `>`,
        for line in lines:                                                                  #   check each line in the block,
            if not line.startswith(">"):                                                    #     if any line does NOT start with `>`,
                return BlockType.PARAGRAPH                                                  #       treat block as a paragraph, not a quote
        return BlockType.QUOTE                                                              #   otherwise, (if every line DOES start with `>`) block is quote block

    if block.startswith("- "):                                                              # If block starts with `- `,
        for line in lines:                                                                  #   check each line in the block,
            if not line.startswith("- "):                                                   #     if any line does NOT start with `- `,
                return BlockType.PARAGRAPH                                                  #       treat block as a paragraph, not an unordered list
        return BlockType.ULIST                                                              #   otherwise (if every line DOES start with `- `) block is an unordered list

    if block.startswith("1. "):                                                             # If block starts with `1. `,
        i = 1                                                                               #   initialize counter for ordered list numbering
        for line in lines:                                                                  #   check each line in the block,
            if not line.startswith(f"{i}. "):                                               #     if any line does NOT match the expected number + `. `,
                return BlockType.PARAGRAPH                                                  #       treat block as a paragraph, not an ordered list
            i += 1                                                                          #   increment counter to checklthe next number
        return BlockType.OLIST                                                              #   otherwise (if every line DOES start with appropriate number + `. `) block is an ordered list
    return BlockType.PARAGRAPH


def markdown_to_html_node(markdown):                ## Converts Markdown text into an HTML node tree
    blocks = markdown_to_blocks(markdown)           # Break Markdown into blocks of content
    children = []                                   # Prepare to collect child HTML nodes
    for block in blocks:                            # Process each block,
        html_node = block_to_html_node(block)       #   convert block into corresponding HTML node
        children.append(html_node)                  #   add HTML node to children list
    return ParentNode("div", children, None)        # Return a `div` containing all child nodes


def block_to_html_node(block):                      ## Converts a block of Markdown to its corresponding HTML node
    block_type = block_to_block_type(block)         # Determine the tupe of the Markdown block
    if block_type == BlockType.PARAGRAPH:           # If the block is a paragraph,
        return paragraph_to_html_node(block)        #   convert it to a paragraph HTML node
    if block_type == BlockType.HEADING:             # If the block is a heading,
        return heading_to_html_node(block)          #   convert it to a heading HTML node
    if block_type == BlockType.CODE:                # If the block is a code block,
        return code_to_html_node(block)             #   convert it to a code HTML node
    if block_type == BlockType.OLIST:               # If the block is an ordered list,
        return olist_to_html_node(block)            #   convert it to an ordered list HTML node
    if block_type == BlockType.ULIST:               # If the block is an unordered list,
        return ulist_to_html_node(block)            #   convert it to an unordered list HTML node
    if block_type == BlockType.QUOTE:               # If the block is a quote block,
        return quote_to_html_node(block)            #   convert it to a blockquote HTML node
    raise ValueError("invalid block type")          # Raise an error if the block type is not recognized


def text_to_children(text):                                 ## Converts raw text into a list of HTML child nodes
    text_nodes = text_to_textnodes(text)                    # Break up the text into text nodes
    children = []                                           # Prepare a list for the resulting HTML nodes
    for text_node in text_nodes:                            # Iterates though each text node,
        html_node = text_node_to_html_node(text_node)       #   convert the text node to an HTML node
        children.append(html_node)                          #   append the HTML node to the list of children
    return children                                         # Return the list of HTML child nodes


def paragraph_to_html_node(block):              ## Converts a Markdown paragraph block to an HTML node
    lines = block.split("\n")                   # Split the block into lines, as parahraphs may span multiple lines
    paragraph = " ".join(lines)                 # Join all lines into one, separating with spaces to maintain cohesion
    children = text_to_children(paragraph)      # Convert the paragraph text into child HTML nodes
    return ParentNode("p", children)            # Wrap the children in a 'p' (paragraph) HTML node and return it


def heading_to_html_node(block):                                ## Converts a Markdown heading block to an HTML node
    level = 0                                                   # Initialize the heading level ('h1', 'h2', etc.)
    for char in block:                                          # Loop through each character in the block,
        if char == "#":                                         #   increment the level for each '#' encountered
            level += 1
        else:                                                   
            break                                               # Stop counting once non-# characters are encountered
    if level + 1 >= len(block):                                 # Check for invalid headings with too few characters after '#'
        raise ValueError(f"invalid heading level: {level}")     #   raise an error if invalid
    text = block[level + 1 :]                                   # Extract the heading's text (skip `level + 1` characters for '#', spaces, etc.)
    children = text_to_children(text)                           # Convert the heading text into child HTML nodes
    return ParentNode(f"h{level}", children)                    # Return an HTML node with the appropriate heading level


def code_to_html_node(block):                                           ## Converts a Markdown code block to an HTML node
    if not block.startswith("```") or not block.endswith("```"):        # Ensure the block starts AND ends with ```
        raise ValueError("invalid code block")                          #   raise an error if that is not the case
    text = block[4:-3]                                                  # Extract the content inside the triple backticks
    raw_text_node = TextNode(text, TextType.TEXT)                       # Create a TextNode from the code content
    child = text_node_to_html_node(raw_text_node)                       # Convert the TextNode into an HTML node
    code = ParentNode("code", [child])                                  # Wrap the code content in a <code> HTML element node
    return ParentNode("pre", [code])                                    # Wrap the <code> element in a <pre> HTML element node, and return


def olist_to_html_node(block):                              ## Converts a Markdown ordered list block to an HTML node
    items = block.split("\n")                               # Split the block into individual list items
    html_items = []                                         # Initialize a list to store the HTML representations of each item
    for item in items:                                      # Loop through each list item in the block,
        text = item[3:]                                     #   skip the "1. " prefix
        children = text_to_children(text)                   #   convert the text of the list item into child HTML nodes
        html_items.append(ParentNode("li", children))       #   create an <li> node for the item and append it to the list
    return ParentNode("ol", html_items)                     # Wrap all <li> nodes in an <ol> HTML element node and return


def ulist_to_html_node(block):                              ## Converts a Markdown unordered list block to an HTML node
    items = block.split("\n")                               # Split the block into individual list items
    html_items = []                                         # Initialize a list to store the HTML representations of each item
    for item in items:                                      # Loop through each list item in the block, 
        text = item[2:]                                     #   skip the "- " prefix,
        children = text_to_children(text)                   #   convert the text of the list item into child HTML nodes
        html_items.append(ParentNode("li", children))       #   create an <li> node for the item and append it to the list 
    return ParentNode("ul", html_items)                     # Wrap all <li> noddes in a <ul> HTML element node and return


def quote_to_html_node(block):                              ## Converts a Markdown blockquote block to an HTML node
    lines = block.split("\n")                               # Split the block into individual lines using newlines
    new_lines = []                                          # Initialize a list to store processed lines from the blockquote
    for line in lines:                                      # Loop through each line in the block
        if not line.startswith(">"):                        # Check if the line starts with a ">", as is reqauired for a blockquote
            raise ValueError("invalid quote block")         #   raise an error if a line does not start with the correct character
        new_lines.append(line.lstrip(">").strip())          #   remove the leading ">", struop any extra whitespace, and store the result
    content = " ".join(new_lines)                           # Combine all processed lines into a single string, forming the quote content
    children = text_to_children(content)                    # Convert the combined content into HTML nodes
    return ParentNode("blockquote", children)               # Wrap the child nodes in a <blockquote> node and return the result