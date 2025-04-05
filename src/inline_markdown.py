import re

from textnode import TextNode, TextType


def text_to_textnodes(text):                                                # Converts raw text into a list of 'TextNode' objects, parsing inline markdown elements
    nodes = [TextNode(text, TextType.TEXT)]                                 # Starts by treating the entire text as plain text,
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)               #   parse **bold** text,
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)              #   parse __italic__ text,
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)                #   parse 'inline code' text,
    nodes = split_nodes_image(nodes)                                        #   parse image text in the format ![Alt](url)
    nodes = split_nodes_link(nodes)                                         #   parse link text in the format [Text](url)
    return nodes


def split_nodes_delimiter(old_nodes, delimiter, text_type):                 # The function called in 'text_to_textnodes' function to parse bold, italic, and code text
    
    new_nodes = []                                                          # Stores the resulting list of text nodes
    
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:                             # Skip nodes that aren't plain text
            new_nodes.append(old_node)                                      # Leave non-text nodes untouched
            continue
        split_nodes = []                                                    # Temporary llist for split results
        sections = old_node.text.split(delimiter)                           # Split text by delimiter
        if len(sections) % 2 == 0:                                          # Raise error if delimiter is not closed (if even, there is an unclosed delimiter)
            raise ValueError("invalid markdown, formatted section not closed")
        for i in range(len(sections)):                                      # Iterate through split sections,
            if sections[i] == "":                                           #   ignore empty selections
                continue
            if i % 2 == 0:                                                  # Even-index sections: plain text
                split_nodes.append(TextNode(sections[i], TextType.TEXT))
            else:                                                           # Odd-index sections: formatted text 
                split_nodes.append(TextNode(sections[i], text_type))
        new_nodes.extend(split_nodes)                                       # Add processed nodes to the result
    return new_nodes                                                        # Return updated list of nodes


def split_nodes_image(old_nodes):                                               # The function called in 'text_to_textnodes' function to parse image text
    new_nodes = []                                                              # Creates a new list of nodes
    for old_node in old_nodes:      
        if old_node.text_type != TextType.TEXT:                                 # If the node is not of type TEXT,
            new_nodes.append(old_node)                                          #   add it to the new list unchanged
            continue
        original_text = old_node.text                                           # Extract the original text of the current node
        images = extract_markdown_images(original_text)                         # Find all markdown images in the text
        if len(images) == 0:                                                    # If no images are found,
            new_nodes.append(old_node)                                          #   add the old_node unchanged
            continue
        for image in images:                                                    # For each detected image, split the text into sections and create new modifiers,
            sections = original_text.split(f"![{image[0]}]({image[1]})", 1)     #   split the original text around the current image Markdown syntax
            if len(sections) != 2:                                              # Validate that the split results in two sectiuons (before and after the image),
                raise ValueError("invalid markdown, image section not closed")  #   raise error if that is not the case
            if sections[0] != "":                                               # If there is text before the image,
                new_nodes.append(TextNode(sections[0], TextType.TEXT))          #   create a new text node for it
            new_nodes.append(                                                   # Create a new image node with the image description and URL
                TextNode(
                    image[0],                                                   #   the alt text for the image,
                    TextType.IMAGE,                                             #   define this node as an image type, 
                    image[1],                                                   #   URL of the image
                )
            )
            original_text = sections[1]                                         # Udate original_text to the remaining text after the current image
        if original_text != "":                                                 # If there is text remaining after processing all images,
            new_nodes.append(TextNode(original_text, TextType.TEXT))            #   create a new text node for it
    return new_nodes                                                            # Return the new list of nodes with images split


def split_nodes_link(old_nodes):                                                # The function called in 'text_to_textnodes' function to parse and split link text
    new_nodes = []                                                              # Initialize a list to store the processed nodes within
    for old_node in old_nodes:                                                  # Iterate over the original list of nodes
        if old_node.text_type != TextType.TEXT:                                 #   if a node is NOT a text type,
            new_nodes.append(old_node)                                          #   add it to the list unchanged
            continue
        original_text = old_node.text                                           # Extract the text of the current text node
        links = extract_markdown_links(original_text)                           # Use the helper function to find all Markdown links in the text
        if len(links) == 0:                                                     # If no links are found,
            new_nodes.append(old_node)                                          #   add the original node unchanged
            continue    
        for link in links:                                                      # For each link found, split the text into sections and create nodes
            sections = original_text.split(f"[{link[0]}]({link[1]})", 1)        # Split the text around the current link Markdown syntax
            if len(sections) != 2:                                              # Ensure the split results in exactly two sections,
                raise ValueError("invalid markdown, link section not closed")   #   raise an error in the case of != 2 sections
            if sections[0] != "":                                               # If there is text before the link,
                new_nodes.append(TextNode(sections[0], TextType.TEXT))          #   create a new text node for it
            new_nodes.append(TextNode(link[0], TextType.LINK, link[1]))         # Create a new node for the link, storing the label and the link itself
            original_text = sections[1]                                         # Update the original_text to the remaining text after the current link
        if original_text != "":                                                 # If there is still text remaining after processing all links,
            new_nodes.append(TextNode(original_text, TextType.TEXT))            #   create a text node for it
    return new_nodes                                                            # Return the new list of nodes with links split


def extract_markdown_images(text):                      ## Identifies and extracts all Markdown image elements using the syntax `![alt_text](url)` from the given text
    pattern = r"!\[([^\[\]]*)\]\(([^\(\)]*)\)"          # Regular expression to match Markdown image syntax
    matches = re.findall(pattern, text)                 # Find all matches of the pattern in the input text
    return matches                                      # Return a list of tuples, where each tuple contains `(alt_text, url)`


def extract_markdown_links(text):                       ## Identifies and extracts all Markdown link elements using the syntax `[link_text](url)`
    pattern = r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)"     # Regular expression to match Markdown link syntax
    matches = re.findall(pattern, text)                 # Find all matches of the pattern in the input text
    return matches                                      # Return a list of tuples, where each tuple contains `(link_text, url)`