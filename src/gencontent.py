import os
from pathlib import Path
from markdown_blocks import markdown_to_html_node


def generate_pages_recursive(dir_path_content, template_path, dest_dir_path, basepath):
    for filename in os.listdir(dir_path_content):                                          # Iterate over all files and subdirectories in the source content directory
        from_path = os.path.join(dir_path_content, filename)                               #   full path of the source file/directory
        dest_path = os.path.join(dest_dir_path, filename)                                  #   full path of the destination source file/directory

        if os.path.isfile(from_path):                                                      # If the item is a file, 
            dest_path = Path(dest_path).with_suffix(".html")                               #   modify the destination path to have an .html extension, 
            generate_page(from_path, template_path, dest_path, basepath)                   #   generate an HTML page from the markdown file

        else:                                                                              # If the item is a directory,
            generate_pages_recursive(from_path, template_path, dest_path, basepath)        #   recursively process its contents


def generate_page(from_path, template_path, dest_path, basepath):
    print(f" * {from_path} {template_path} -> {dest_path}")         # Inform the user of the generated file paths
    from_file = open(from_path, "r")                                # Open the markdown file for reading,
    markdown_content = from_file.read()                             #   read its contents,
    from_file.close()                                               #   close the file

    template_file = open(template_path, "r")                        # Open the template file,
    template = template_file.read()                                 #   read its contents,
    template_file.close()                                           #   close the file

    node = markdown_to_html_node(markdown_content)                  # Parse the markdown content into an HTML node,
    html = node.to_html()                                           #   convert that HTML node to an HTML string

    title = extract_title(markdown_content)                         # Extract the title (first top-level heading) from the markdown content
    template = template.replace("{{ Title }}", title)               # Replace the "{{ Title }}" placeholder in the template with the extracted title
    template = template.replace("{{ Content }}", html)              # Replace the "{{ Content }}" placeholdee with the generated HTML content
    template = template.replace('href="/', 'href="' + basepath)     # Adjust href links to include the base path
    template = template.replace('src="/', 'src="' + basepath)       # Adjust src links to include the base path

    dest_dir_path = os.path.dirname(dest_path)                      # Get the directory path for the destination file
    if dest_dir_path != "":                                         # If the destination directory path is not empty,
        os.makedirs(dest_dir_path, exist_ok=True)                   #   ensure the destination directory exists (create it if necessary)
    to_file = open(dest_path, "w")                                  # Open the destination file for writing,
    to_file.write(template)                                         #   write the final HTML ftemplate to the destination file


def extract_title(md):
    lines = md.split("\n")                 # Split the markdown content into individual lines,
    for line in lines:                     #   iterate through each line,
        if line.startswith("# "):          #   if a line starts with "# " (a top-level heading)
            return line[2:]                #   return the text following the "# " as the title
    raise ValueError("no title found")     # Raise an error if no top-level heading is found to be the title