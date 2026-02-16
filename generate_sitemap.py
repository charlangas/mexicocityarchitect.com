import os
from datetime import datetime

base_url = "https://www.mexicocityarchitect.com"
output_file = "sitemap.xml"

# Pages to explicitly exclude
excluded_files = [
    "google", # google verification files often look like google<hash>.html
    "thank-you.html",
    "404.html",
    "blog_template.html",
    "location_template.html",
    "index2.html",
    "index3.html",
    "blogpost.html", # Assuming this is a template based on generic name
    "service_template.html",
    "project_template.html"
]

# Directories to scan
directories_to_scan = [
    ".", # Root
    "locations",
    "blog",
    "portfolio",
    "services"
]

print("Generating sitemap...")

xml_content = """<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
"""

def get_last_mod(filepath):
    return datetime.fromtimestamp(os.path.getmtime(filepath)).strftime('%Y-%m-%d')

def add_url(path, priority="0.8", changefreq="monthly"):
    global xml_content
    # Ensure path doesn't start with / or ./
    clean_path = path.lstrip("./").lstrip("/")
    
    # Check if file exists
    if not os.path.exists(path):
        return

    # Check exclusions
    filename = os.path.basename(path)
    if filename in excluded_files or filename.startswith("google") or "_template" in filename:
        return

    url = f"{base_url}/{clean_path}"
    last_mod = get_last_mod(path)
    
    xml_content += f"""  <url>
    <loc>{url}</loc>
    <lastmod>{last_mod}</lastmod>
    <changefreq>{changefreq}</changefreq>
    <priority>{priority}</priority>
  </url>
"""

# Scan directories
for directory in directories_to_scan:
    if not os.path.exists(directory):
        continue
        
    for filename in os.listdir(directory):
        if filename.endswith(".html"):
            filepath = os.path.join(directory, filename)
            
            # Determine priority based on directory/file
            priority = "0.8"
            if directory == ".":
                if filename == "index.html":
                    priority = "1.0"
                else:
                    priority = "0.9"
            elif directory == "locations":
                priority = "0.7"
            elif directory == "blog":
                priority = "0.6" # Blog posts often have lower priority than main pages
            
            add_url(filepath, priority=priority)

xml_content += "</urlset>"

with open(output_file, "w") as f:
    f.write(xml_content)

print(f"Sitemap generated at {output_file} with {xml_content.count('<url>')} URLs.")
