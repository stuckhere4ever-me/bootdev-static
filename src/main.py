from .markdown_converter import markdown_to_html_node, extract_title

import os
import shutil

STATIC_ROOT = './static'
HTML_ROOT = './public'
TEMPLATE_ROOT = './template'
CONTENT_ROOT = './content'


def clean_public():
    prep_dest(HTML_ROOT)
    copy_tree(STATIC_ROOT, HTML_ROOT)

def prep_dest(dest):
    if os.path.exists(dest):
        shutil.rmtree(dest)
    os.mkdir(dest)


def copy_tree(src, dest):
    list_of_items = os.listdir(src)
    
    for item in list_of_items:
        src_filename = os.path.join(src, item)    
        dst_filename = os.path.join(dest, item)
        if os.path.isfile(src_filename):
            shutil.copy(src_filename, dst_filename)

        else:
            if not os.path.exists(dst_filename):
                os.mkdir(dst_filename)
            copy_tree(src_filename, dst_filename)


def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    with open (from_path, 'r') as src:
        src_markdown = src.read()

    with open (template_path, 'r') as template:
        template_html = template.read()


    converted_html = (markdown_to_html_node(src_markdown)).to_html()
    page_title = extract_title(src_markdown)

    final_html = template_html.replace('{{ Title }}', page_title)
    final_html = final_html.replace('{{ Content }}', converted_html)

    if not os.path.exists(dest_path):
        os.makedirs(dest_path)

    dest_file = os.path.join(dest_path, 'index.html')
    with open (dest_file, 'w', encoding='utf-8') as dest:
        dest.write(final_html)

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    
    list_of_items = os.listdir(dir_path_content)
    # print (list_of_items)

    for content in list_of_items:
        updated_src_path = os.path.join(dir_path_content, content)
        if os.path.isfile(updated_src_path):
            #print (updated_src_path)
            generate_page(updated_src_path, template_path, dest_dir_path)
        else:
            updated_dst_path = os.path.join(dest_dir_path, content)
            generate_pages_recursive(updated_src_path, template_path, updated_dst_path)


def main():

    clean_public()

    if not os.path.exists((content_path := os.path.join(CONTENT_ROOT, 'index.md'))):
        raise FileNotFoundError(f"Missing File {content_path}")
    
    if not os.path.exists((template_path := os.path.join(TEMPLATE_ROOT, 'template.html'))):
        raise FileNotFoundError(f"Missing File {template_path}")


    generate_pages_recursive(CONTENT_ROOT, template_path, HTML_ROOT)




main()
