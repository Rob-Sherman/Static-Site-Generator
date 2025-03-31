import os
import shutil
import re

from textnode import *
from htmlnode import *
from inline_markdown import *
from block_markdown import *


path_to_static = "static/"
path_to_public = "public/"

from_path = "content/"
template_path = "template.html"
dest_path = "public/"

def main():
	check_directories(path_to_static, path_to_public)
	copy_contents(path_to_static, path_to_public)
	find_pages(from_path, dest_path)


# check paths and delete contents from to_dir (public)
def check_directories(from_dir, to_dir):
	if os.path.exists(from_dir):
		print(f"{from_dir} directory exists")
	else:
		raise Exception(f"The directory, {from_dir}, does not exist.")

	if os.path.exists(to_dir):
		print(f"{to_dir} directory exists")
		shutil.rmtree(to_dir)
		print(f"Removed old {to_dir} directory")
		os.mkdir(to_dir)
		print(f"Created new {to_dir} directory")
	else:
		os.mkdir(to_dir)
		print(f"{to_dir} directory created")

# copy all files / directories
def copy_contents(from_dir, to_dir):
	static_contents = os.listdir(from_dir)
	print(static_contents)
	if len(static_contents) == 0:
		raise Exception(f"{from_dir} directory is empty.")
	else:
		for item in static_contents:
			path = os.path.join(from_dir, item)
			path2 = os.path.join(to_dir, item)
			print(path)
			if os.path.isfile(path) == True:
				shutil.copy(path, path2)
				print(f"Copying: {path} to {path2}")
			else:
				os.mkdir(path2)
				print(f"Creating {path2} directory")
				copy_contents(path, path2)


# convert to html
def convert_to_html(from_path):
	with open(from_path) as f:
		contents = f.read()
		node = markdown_to_html_node(contents)
		html = node.to_html()
		return html


# extract title from Markdown
def extract_title(markdown):
	title = re.search(r"<h1>(.*)</h1>", markdown)
	return title.group(1)


# generate html file
def generate_page(from_path, template_path, dest_path):
	html = convert_to_html(from_path)
	template = ""
	title = extract_title(html)
	dest_path = dest_path.replace(".md", ".html")
	with open(template_path) as f:
		template = f.read()
	template = template.replace("{{ Title }}", title)
	new_file = template.replace("{{ Content }}", html)
	
	try:
		with open(dest_path, "w") as file:
			file.write(new_file)
		print(f"{dest_path} created succesfully.")
	except Exception:
		print("Couldn't create file")


#find all markdown files then send to generate_page
def find_pages(from_path, dest_path):
	dir_contents = os.listdir(from_path)
	if len(dir_contents) == 0:
		raise Exception(f"{from_path} directory is empty.")
	else:
		for item in dir_contents:
			path = os.path.join(from_path, item)
			path2 = os.path.join(dest_path, item)
			if os.path.isfile(path) == True:
				if path.endswith(".md"):
					generate_page(path, template_path, path2)
					print(f"Generating page from {path}")
				else:
					print(f"Unsupported file type: {path}")
					continue
			else:
				os.mkdir(path2)
				print(f"Creating {path2} directory")
				find_pages(path, path2)
			


main()

