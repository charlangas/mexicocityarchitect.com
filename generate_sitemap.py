import os
from datetime import datetime

base_url = "https://www.mexicocityarchitect.com"
locations_dir = "locations"
output_file = "sitemap.xml"

print("Generating sitemap...")

xml_content = """<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
"""

# Add main pages
main_pages = [
    "index.html",
    "about.html",
    "services.html", # Assuming this exists
    "portfolio.html",
    "blog.html",
]

for page in main_pages:
    # Check if file exists to avoid 404s in sitemap
    if os.path.exists(page):
        # Format the date as YYYY-MM-DD
        last_mod = datetime.fromtimestamp(os.path.getmtime(page)).strftime('%Y-%m-%d')
        xml_content += f"""  <url>
    <loc>{base_url}/{page}</loc>
    <lastmod>{last_mod}</lastmod>
    <changefreq>monthly</changefreq>
    <priority>0.8</priority>
  </url>
"""

# Add location pages
if os.path.exists(locations_dir):
    for filename in os.listdir(locations_dir):
        if filename.endswith(".html"):
            last_mod = datetime.fromtimestamp(os.path.getmtime(os.path.join(locations_dir, filename))).strftime('%Y-%m-%d')
            xml_content += f"""  <url>
    <loc>{base_url}/locations/{filename}</loc>
    <lastmod>{last_mod}</lastmod>
    <changefreq>monthly</changefreq>
    <priority>0.7</priority>
  </url>
"""

xml_content += "</urlset>"

with open(output_file, "w") as f:
    f.write(xml_content)

print(f"Sitemap generated at {output_file}")