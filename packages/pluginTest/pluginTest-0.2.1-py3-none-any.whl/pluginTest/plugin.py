# from mkdocs.plugins import BasePlugin
# import re

# class BadgesPlugin(BasePlugin):

#     def on_page_content(self, markdown, page, config, site_navigation=None, **kwargs):
#         # Define a regular expression pattern to search for the badge Markdown
#         badge_pattern = r'\|Example badge\|works\|'
        
#         # Define the replacement HTML for the badge
#         badge_html = '''
#         <div class="badge-container">
#             <img src="https://img.shields.io/badge/example-badge-green" alt="Example Badge">
#         </div>
#         '''

#         # Use the re.sub() function to replace the Markdown pattern with the badge HTML
#         markdown = re.sub(badge_pattern, badge_html, markdown)

#         return markdown

from mkdocs.plugins import BasePlugin
from mkdocs.config import config_options
from bs4 import BeautifulSoup

class BadgesPlugin(BasePlugin):

    config_scheme = (
        ('name', config_options.Type(str, default='')),
    )

    def on_post_page(self, output_content, page, config):
        # Check if the 'name' metadata is present for the current page
        if 'name' in page.meta:
            # Parse the HTML content with BeautifulSoup
            soup = BeautifulSoup(output_content, 'html.parser')
            
            # Find the right side menu container by its class
            right_sidebar = soup.find('div', class_='md-sidebar--secondary')
            if right_sidebar:
                # Create a new div with the class 'docsOwner'
                owner_div = soup.new_tag('div', class_='docsPageOwner')
                # Set the text of the div to the 'name' from the page's metadata
                owner_div.string = page.meta['name']
                
                # Insert the new div at the top of the right sidebar
                right_sidebar.insert(0, owner_div)
                
                # Return the modified HTML as a string
                return str(soup)
        
        # If the 'name' metadata is not present, or the sidebar isn't found,
        # return the original HTML content
        return output_content
