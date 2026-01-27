# Source Code

This directory contains all the requisite source code that builds the website.

## Files

Within the directory the following files are contained:
- [htmlnode.py](htmlnode.py)
- [main.py](main.py)
- [markdown_converter.py](markdown_converter.py)
- [markdown_helpers.py](markdown_helpers.py)
- [textnode.py](textnode.py)
- __init__.py - Notes that this file is included to ensure the directory is packaged

Because of the packaged nature of the project, imports will look like this:
- `from src.{filename} import {thing_to_import}` from outside the src directory
- `from .{filename} import {thing_to_import}` from within the src directory

## CONSTANTS

Contstants that are used within the overall program
- HTML_ROOT - The destination of the final website
- STATIC_ROOT - Where the static files are stored
- TEMPLATE_ROOT - Where the root files are stored
- CONTENT_ROOT - Where the content markdown files to be converted are stored



## File Details - htmlnode.py
There are some specific things in the file that are a bit confusing, so I want to make sure to explain them in detail.
First off, everything is using Type Hinting.  This took a **long** ass time.  Python really hates static typing.  Like a lot.  

`from typing import Sequence, Dict, Callable` -> This allows us to use type hints for Dictionaries, Functions (Callables), and 'Sequences' which as far as I can tell are anything iterable (is that actually a word?)

`LeafBuilder = Callable[[TextNode], "LeafNode"]` -> This is me building a type for a function I will create.  

The specific syntax looks like this: `{type_name} = Callable[[{list_of_argument_types OR ...}], {return type}]`

There are also 4 'helper' functions for LeafNodes in the file.  
Specifically, these will take a TextNode and turn them into leaf nodes.  These functions are all of type `LeafBuilder`

The final thing in this file is a mapping of Lead Node functions.  
This is a dictionary of type: `Dict[TextType, LeafBuilder]`

It lets me create a an HTML node from a text node in clean code rather than having to worry about side effects, since each Function is completly isolated from the others.  In the final versions side effects and immutiability was preserved so it wasn't strictly neccissary but it did clean up the code some, and let me handle images and links easily.  It also significantly reduced the number of edge cases I had to deal with.

These functions are called as part of the text_node_to_html_node function in markdown converter.

### HTML Node

**Location**: [htmlnode.py](htmlnode.py)

**Child Classes**
- LeafNode - An HTML Node with no children 
- ParentNode - An HTML Node with a list of children

**Properties** 
- Tag - What kind of HTML Node is this? 
- Value - Whats the value of the node (usually this is text to display or alt-text for an image)
- Children - A list of HTMLNodes that are all of our children  
- Properties - a dictionary that contains the key:value paris of 'property':value.  This is essentially extra stuff that's needed for html tags (example, src or href)

I dislike the fact that properties is reused in this case, but technically both are accurate so here we are.  Note that variable names are not exactly the same (example properties is actually props in code)

Children is a list of abstracted HTML nodes because they can be either Leaf or Parent nodes.  This is _technically_ polymorphism, since we will run to_html on each of the inhreitted items. 

**Functions**
```to_html ```

Will be overwritten by Child Classes

```props_to_html``` 

Rewrite the properties dictionary as html.
For deterministic behavior I sorted the properties, but this mucked up a couple of my unit tests.  Specifically, I wanted to make sure src and href were in the first position, so I had to write edge cases for them.  

After that I used list comprehension to actually build out parts of an html string then used join to throw them together.  Note that we needed to make sure there is a leading space so it doesn't plunk them all together. 

`parts = [f'{prop}="{self.props[prop]}"' for prop in sorted_props]` -> Gives me a list of strings
`' ' + ' '.join(parts)` -> creates one string from the array parts with a space as the seperating character and adds a leading space

```__eq__```

This is just for unit tests.

```__repr__```

This is the represented by method (not str).  They are acting the same here.

### LeafNode

**Location**: [htmlnode.py](htmlnode.py)

**Parent Class**
HTMLNode

**Child Classes**
None

**Properties** 
All Properties are hte same, but note that LeafNodes have no children


**Functions**
```to_html ```

Builds out the html representation.  Validate it is a legitimate leaf tag, turn my properties into html, then render my html.
Because img is a void tag, I had to handle it specially (adding / before the close tag).  Which breaks my value check, but it never happens so i left it be.

The trick will be I am going to build out the leaf node with a Text Node so I can make sure its not a thing.

### ParentNode

**Location**: [htmlnode.py](htmlnode.py)

**Parent Class**
HTMLNode

**Child Classes**
None

**Properties** 
All Properties are hte same, but note that Parent Nodes MUST have children and tags and not have a value


**Functions**
```to_html ```

Builds out the html representation.  I had to do a bunch of assertions to ensure my type hinting worked okay. 
This function was generally pretty easy, we just wrap our children's html tags in ours (remember to throw open then children then close)

This is where the polymorphism kicks in heavy: `parts = [child.to_html() for child in self.children]`

child can either be another parent node or a leaf node, either way since we abstracted out the to_html() function it'll work.  And we do some fancy pants recurision here as part of the list comprehension. 

if child is leaf node (base case) then we just return the rendered string
if child is a parent node (recursive case) then we return a rendered string based on the children's string and our tag.


## File Details - textnode.py
A pretty simple file.  We have an enum type that allows us to enumerate different HTML types that may show up. 
Currently we support Text, Bold, Italic, Code, Link, and Images. Note that the 'values' are the html tags (with the exception of Text which doesn't automatically add a <p> tag)


### TextNode

**Location**: [textnode.py](textnode.py)

**Properties** 
- Text -> The text contained within the node
- text_type -> A TextType that defines what type of md we are dealing with
- url -> Certain things need urls (links and images), otherwise it can be


```__eq__```

This is just for unit tests.

```__repr__```

This is the represented by method (not str).  They are acting the same here.

## File Details - markdown_converter.py
This file contains all of the base functionality around converting markdown to html.
The goal will be to take markdown and convert it to text blocks, then convert those text blocks to html.

```markdown_to_html_node(md)```
Takes one argument (string) that represents the markdown we want to conver to html.
Returns a single HTML node that will represent the entire webpage that is going to be created.

First thing we are going to do is take the markdown file and create a list of text blocks.
Then we will iterate through the blocks, get the type for each block and trim out the requisite characters (based on the type).

This was hell in practice, it ended up not actually being that hard, but finding the right place to remove the markdown characacters and where to combine them suuuucked.  Once I killed all the erroneous characters, then we handle everything that isn't a header or code.  

Those get inline children(build children), creates a list of htmnl nodes (we can assume all the second tier are LeafNodes), then create a single parent node with all of those children and append it to my list of html_nodes.

If it is a Header I do the same thing but account for the `<h{num}>` but determining the number of hash marks.
If it is code then I just build my own text node and turn it into an html node.  I can assumethat there are no children in a code string.  

Also I needed to apprend a 'pre' parent node because it is preformatted

I could not come up with a better way to build out each node without building out a mapping and that was kind of a pain, so I didn't bother. 


After we run one of those cases for all the blocks, we need to embed the entire thing into one div node.  

```text_node_to_html_node(md)```
Uses Leaf Builder to assign a function based on the type of node we have, then runs the assigned function on the text node.

```text_to_text_blocks(md)```
This will go one at a time through all of the types of text nodes that could exist (stored in PIPELINE), and will run that particular deliminter types function.  These ended up being created as closures so that we could send the deliminter value into the function completely independent of the actual value in PIPELINE.

```build_children(md)```
The tricky part here was to note that we are actually getting an md block, so we had to break out the text blocks then build and html node from each of them.  I know I could have used a list comprehension to do this, but this felt like it made it more readable.  

## File Details - markdown_helpers.py
This file is the most complex in terms of logic in the entire program.  It includes all of the helper functions for various points within the project.  Its not perfectly laid out, but the ideas are generally well founded.

`IMG_ADJUST`, `LINK_ADJUST`, and `IDX_ADJUST` are constants that allow me to remove link and image markdown characters.

`PIPELINE = [TextType.BOLD, TextType.ITALIC, TextType.CODE, TextType.IMAGE, TextType.LINK]` is what we iterate over for all the different text types in order.

`Extractor = Callable[[str], List[Tuple[str,str]]]` and
`SplitBuilder = Callable[[List[TextNode]], List[TextNode]]`

will be used specifically for type hinting.
```python
class BlockType (Enum):
    PARAGRAPH = 'p'
    HEADER = 'h'
    QUOTE = 'blockquote'
    CODE = 'code'
    UNORDERED_LIST = 'ul'
    ORDERED_LIST = 'ol'
```

Are the various types that can be included for a BlockType

```python 
# RegEx Helpers
def extract_markdown_images(text:str) -> List[Tuple[str,str]]:
    return re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    
def extract_markdown_links(text:str) -> List[Tuple[str,str]]:
    return re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)

# Mapping for RegEx Functions
EXTRACTOR: Dict[TextType,Extractor] = {
    TextType.IMAGE: extract_markdown_images,
    TextType.LINK: extract_markdown_links,

}
```

This section builds out regex expressions for extracting images and links.  
I took the particular regex from bootdev's hints, I spent about 30 minutes trying to figure it out then yelled at my screen and gave up.  I hate regex so much.  It's just as bad as when it was in perl.  Seriously why can't they make it easier. 



```python
def extract_title(markdown):
    lines = markdown.split('\n')
    for line in lines:
        new_line = line.strip()
        if new_line.startswith('# '):
            return new_line[2:]
    
    raise Exception("Title Missing")
```
Grabs H1 for the title.

```python
# Splitter Heplers
def make_delimiter_splitter(delimter:str, text_type:TextType) -> Callable[[List[TextNode]], List[TextNode]]:
    def split_nodes_delimiter(old_nodes:list[TextNode]) -> list[TextNode]:
        ...
        return new_nodes
    return split_nodes_delimiter
```
Build a closure around split_node_deliminter so that it would be able to run with a deliminting character but I wouldn't have to pass it as part of the code.  It was a slick way of assigning functions to the mapping without having to send the delimiter

```python
def make_img_link_splitter(text_type:TextType, adjuster:int) -> Callable[[List[TextNode]], List[TextNode]]:
    if not (text_type is TextType.LINK or text_type is TextType.IMAGE):
        raise ValueError("Improper Usage")
    
    def split_nodes_img_link_helper(old_nodes:List[TextNode]) -> List[TextNode]:
        ...
        return new_nodes
    return split_nodes_img_link_helper
```
The true evil genius is here.  I can build out a closure here that takes two variables in its outer function, but still allow it to be the same number of arguments in the higher-order function.  What that means is that I can call everything out of the pipeline, and not have to split my cases at the base by image, link, or other.


```python
# Mapping for splitter functions
SPLIT_BUILDER: Dict[TextType, SplitBuilder] = {
    TextType.BOLD: make_delimiter_splitter('**', TextType.BOLD),
    ...
    TextType.IMAGE: make_img_link_splitter(TextType.IMAGE, IMG_ADJUST),
    TextType.LINK: make_img_link_splitter(TextType.LINK, LINK_ADJUST)

}
```
See this section.  BOLD took a make delimiter splitter function (which returns its own function that takes input and delimits based on bold).  Image and Link take a different maker function (which takes two arguments), but return the same type of function and therefore can be run against the same code.

Now I can go:
for pipe in pipeline:
   run function @ SPLIT_BUILDER[pipe]

Adding more types just means we need to add to the SPLIT_BUILDER Dictionary and the pipeline.  Unless its in pipeline in won't run.  

```python
def markdown_to_blocks(markdown:str) -> List[str]:
```

```python
def markdown_header_validator(markdown):
def markdown_code_validator(markdown):
def markdown_quote_validator(markdown):
def markdown_unordered_list_validator(markdown):
def markdown_ordered_list_validator(markdown):


Validator = Callable[[str], BlockType]
VALIDATOR:Dict[BlockType,Validator] = {
    BlockType.HEADER: markdown_header_validator,
    BlockType.QUOTE: markdown_quote_validator,
    BlockType.CODE: markdown_code_validator,
    BlockType.UNORDERED_LIST: markdown_unordered_list_validator,
    BlockType.ORDERED_LIST: markdown_ordered_list_validator,
    BlockType.PARAGRAPH: lambda _: BlockType.PARAGRAPH,

}
```
By now this functionality should be pretty easily understandable.  We build functions, map them, then use them with the ENUM type.  Validation was slightly different for each of the types.  I am sure there is a slick way to do this, but I couldn't think of it because I'm old and don't really give that much of a crap. 

```python
def block_to_block_type(markdown:str) -> BlockType:
    if not markdown: raise ValueError("Empty Block")
    first_markdown_char = markdown[0]
    match first_markdown_char:
        case '#':
            validator = VALIDATOR[BlockType.HEADER]
        case '>':
            validator = VALIDATOR[BlockType.QUOTE]
        case '-': 
            validator = VALIDATOR[BlockType.UNORDERED_LIST]
        case _:
            if first_markdown_char.isdigit():
                validator = VALIDATOR[BlockType.ORDERED_LIST]
            elif markdown.startswith('```'):
                validator = VALIDATOR[BlockType.CODE]
            else:
                validator = VALIDATOR[BlockType.PARAGRAPH]
        
    return validator(markdown)
```
Left code here to show how to use the VALIDATOR mapping.  
These are annoying because I have to check header, then quote, then unordered list. 
Since Ordered list doesn't have a 'start string' other than 'any digit' and code is handled completely uniquely, I dropped them both into the default case.

The trick is this function returns a BlockType if and only if it is valid markdown.  So the entire purpose is to determine malformation and return a block type.  Paragraphs do nothing and just assume they are not malformed. This is probably not perfect, but its managable for this project.

```python
def trim_md_chars(block: str, block_type):
    updated_string = block
    if block_type == BlockType.QUOTE:   
        updated_string = updated_string.replace('\n> ', ' ')
        updated_string = updated_string.replace('> ', '')
    
    if block_type == BlockType.UNORDERED_LIST:
        lines = updated_string.split('\n')
        parts = [f'<li>{line[2:]}</li>' for line in lines]
        updated_string = "".join(parts)

    if block_type == BlockType.ORDERED_LIST:
        # print (repr(updated_string))
        lines = updated_string.split('\n')
        parts = [f'<li>{line[3:]}</li>' for line in lines]
        updated_string = "".join(parts)

    if block_type == BlockType.HEADER:
        space_char = updated_string.index(' ')
        updated_string = updated_string[space_char+1:]

    if block_type == BlockType.CODE:
        updated_string = updated_string.replace('```\n','')
        updated_string = updated_string.replace('\n```','\n')


    return updated_string
```

I hate hate hate this code.  
I considered building this into mapping, but it just wasn't worth the effort.
So the issue here is every single type requires its own trimming.  I was going to write a function for each one then build a closure, but it was too much work and the project was already mostly done so I didn't bother. 

## File Details - main.py
This is the main entry point of the program, and actually handles all the high level work.  
I was going to build a website_helpers.py file but again, it was already working so it didn't feel worth it.


```python
STATIC_ROOT = './static'
HTML_ROOT = './docs'
TEMPLATE_ROOT = './template'
CONTENT_ROOT = './content'
```

Because it was easier than changing the HTMLRoot I figured this would be something I changed in the future and dropped into a .env


```python
def prep_dest(dest):
def copy_tree(src, dest):
```
Functions to ensure the HTML Root only contains static content.


```python
def generate_page(from_path, template_path, dest_path, base_path):
```
Opens the files (markdown, and template), converts the markdown to html, then pulls the page title, and drops the HTML into the template.  Then writes the final_html file to the correct place (if it doesn't exist build the entire chain)

```python
def generate_pages_recursive(dir_path_content, template_path, dest_dir_path, base_path): 
```
Recursively crawls the file tree and generates all the pages

```python
def main():

    base_path = '/'

    if len(sys.argv) > 1:
        base_path = f'{sys.argv[1]}/'
    print (base_path)

    if not os.path.exists((content_path := os.path.join(CONTENT_ROOT, 'index.md'))):
        raise FileNotFoundError(f"Missing File {content_path}")
    
    if not os.path.exists((template_path := os.path.join(TEMPLATE_ROOT, 'template.html'))):
        raise FileNotFoundError(f"Missing File {template_path}")

    clean_public()
    generate_pages_recursive(CONTENT_ROOT, template_path, HTML_ROOT, base_path)
```
Main just gives us the base path (it's the BUILD_REPO for us) checks to make sure there is an index.md and a template html file, then preps the directory, and creates all the pages.  