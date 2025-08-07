from textnode import *
from htmlnode import *
from functions import *
import os
import shutil
import sys


def main():
    basepath = ""
    if len(sys.argv) == 1:
        basepath = "./"
    else:
        basepath = sys.argv[1]
    print(basepath)
    copy(f"{basepath}static", f"{basepath}docs")
    #generate_page("./content/index.md", "template.html", "./public/index.html")
    generate_pages_recursively(f"{basepath}content", "template.html", f"{basepath}docs", basepath = basepath)

def copy(source, destination):
    if not os.path.exists(destination):
        os.mkdir(destination)
    if not os.path.exists(source):
        raise Exception(f"Invaild source path: {source}")

    clear_directory(destination)
    copy_files(source, destination)


def copy_files(source, destination):
    if os.path.isdir(source):
        cd = os.listdir(source)
        for item in cd:
            full_path = os.path.join(source, item)
            destination_path = os.path.join(destination, item)
            if os.path.isdir(full_path):
                print(f"Copying directory {full_path}")
                os.mkdir(destination_path)
                copy_files(full_path, destination_path)
                
            else:
                if os.path.isfile(full_path):
                    print(f"Copying file {full_path}")
                    shutil.copy(full_path, destination_path)


def clear_directory(directory):
    if os.path.isdir(directory):
        cd = os.listdir(directory)
        for item in cd:
            full_path = os.path.join(directory, item)
            if os.path.isdir(full_path):
                print(f"clearing directory {full_path}")
                clear_directory(full_path)
                print(f"removing directory {full_path}")
                shutil.rmtree(full_path)
            else:
                print(f"removing file {full_path}")
                os.remove(full_path)
    return 

def generate_page(from_path, template_path, dest_path , basepath = "./"):
    if dest_path.endswith(".md"):
        dest_path = dest_path[:len(dest_path) - 2]
        dest_path += "html"
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    markdown = read_file(from_path)
    template = read_file(template_path)
    html_nodes = markdown_to_html_node(markdown)
    html = html_nodes.to_html()
    title = extract_title(markdown) 
    template = template.replace("{{ Title }}", title)
    template = template.replace("{{ Content }}", html)
    template = template.replace('href="/', f'href="{basepath}')
    template = template.replace('src="/', f'src="{basepath}')
    write_file(dest_path, template)

def generate_pages_recursively(from_path, template_path, dest_path, basepath = "./"):
    if os.path.isdir(from_path):
        cd = os.listdir(from_path)
        for file in cd:
            full_path = os.path.join(from_path, file)
            destination_path = os.path.join(dest_path, file)
            if file.endswith(".md"):
                generate_page(full_path, template_path, destination_path, basepath)
            if os.path.isdir(full_path):
                os.mkdir(destination_path)
                generate_pages_recursively(full_path, template_path, destination_path, basepath)

def read_file(path):
    if not os.path.isfile(path):
        raise Exception(f"Invalid file name: {path}")
    file = open(path)
    output = file.read()
    file.close()
    return output

def write_file(path, text):
    try:
        with open(path, 'x') as file:
            file.write(text)
        print(f"File '{path}' created successfully.")
    except FileExistsError:
        print(f"File '{path}' already exists.")




if __name__ == '__main__':
    main()