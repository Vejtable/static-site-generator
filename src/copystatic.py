import os
import shutil


def copy_files_recursive(source_dir_path, dest_dir_path):
    if not os.path.exists(dest_dir_path):                   # If the destination directory doesn't exist,
        os.mkdir(dest_dir_path)                             #   create it

    for filename in os.listdir(source_dir_path):            # Iterate over every file and subdirectory in the source directory
        from_path = os.path.join(source_dir_path, filename) #   full source file path
        dest_path = os.path.join(dest_dir_path, filename)   #   full destination file path
        print(f" * {from_path} -> {dest_path}")             #   inform the user of the file being copied
 
        if os.path.isfile(from_path):                       # If the current item is a file,
            shutil.copy(from_path, dest_path)               #   copy it to the destination

        else:                                               # If the current item is a directory,
            copy_files_recursive(from_path, dest_path)      #   call the function recursively