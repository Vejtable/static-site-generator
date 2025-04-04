import os                                           # Module for interacting with the file system (e.g., paths, directories)
import shutil                                       # Module for high-level file operations like deleting entire directories
import sys                                          # Module for accessing command-line arguments (among other utilities)

from copystatic import copy_files_recursive         # Custom function to copy static files (e.g., images/styles) to the destination
from gencontent import generate_pages_recursive     # Custom function to generate HTML pages from content and a template

                                    ## Paths to various key directories and files.
dir_path_static = "./static"        # Directory containing static assets (e.g., CSS, images, JS files)
dir_path_public = "./docs"          # Target 'public' directory where the site will be built
dir_path_content = "./content"      # Directory containing site content files (e.g., Markdown, JSON)
template_path = "./template.html"   # HTML template used to wrap content into full HTML pages
default_basepath = "/"              # Default base path for links in the generated site

def main():                                     ## Main function used to build static site.

    basepath = default_basepath                 # Use default basepath unless overridden,
    if len(sys.argv) > 1:                       #   if a base path is provided,
        basepath = sys.argv[1]                  #   use it instead of the default

    print("Deleting public directory...")       # Notify user the directory is being deleted
    if os.path.exists(dir_path_public):         # Check if the target directory 'docs' exist
        shutil.rmtree(dir_path_public)          # Delete the 'docs' directory and all of its contents recursively

    print("Copying static files to public directory...")    # Notify user of files being copied over to public directory
    copy_files_recursive(dir_path_static, dir_path_public)  # Recursively copy all files from 'static'

    print("Generating content...")              # Notify user that HTML pages will be created using the content and the template - content generation process is beginning
    generate_pages_recursive(dir_path_content, template_path, dir_path_public, basepath)
    ### Traverse through the 'content' directory ('dir_path_content'), processing each content file
    ### Use the 'template_path' file to wrap the raw content in a standardized HTML structure
    ### Write the newly generated HJTML files into the 'docs' directory ('dir_path_public')
    ### The 'basepath' is used to adjust relative links in the HTML 

main()