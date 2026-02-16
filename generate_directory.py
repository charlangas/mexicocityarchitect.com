import json
import os

# Configuration
locations_file = 'locations.json'
output_file = 'directory.html'

# Load data
with open(locations_file, 'r', encoding='utf-8') as f:
    data = json.load(f)

services = data['services']
locations = data['locations']

html_content = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Architecture Directory Mexico City | Talacha</title>
    <link rel="stylesheet" href="style.css">
    <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@400;600;700&display=swap" rel="stylesheet">
    <link href="https://fonts.googleapis.com/css2?family=Newsreader:opsz,wght@6..72,300;6..72,400;6..72,600&display=swap" rel="stylesheet">
</head>
<body>

    <header class="header">
        <a href="index.html" class="logo"><img src="img/logo.svg" alt="Talacha Logo"></a>
        <nav>
            <ul class="nav-links">
                <li><a href="index.html">Work</a></li>
                <li><a href="about.html">Studio</a></li>
                <li><a href="#contact">Contact</a></li>
            </ul>
        </nav>
    </header>

    <main>
        <section class="section">
            <div class="container">
                <h1 style="margin-bottom: 20px;">Architecture Directory</h1>
                <p>Comprehensive guide to architectural services in Mexico City's premier neighborhoods.</p>
                
                <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 60px; margin-top: 80px;">
"""

for location in locations:
    html_content += f"""
                    <div>
                        <h2 style="font-size: 2rem; border-bottom: 1px solid #000; padding-bottom: 10px; margin-bottom: 20px;">{location['name']}</h2>
                        <ul class="swiss-list" style="border-top: none;">
    """
    for service in services:
        slug = f"locations/{service['slug']}-{location['slug']}.html"
        html_content += f"""
                            <li style="padding: 10px 0; border-bottom: 1px solid #eee;">
                                <a href="{slug}">{service['name']}</a>
                            </li>
        """
    html_content += """
                        </ul>
                    </div>
    """

html_content += """
                </div>
            </div>
        </section>
    </main>

    <footer class="footer">
        <div class="container footer-grid">
            <div>
                <h4>Talacha</h4>
                <p style="color: #666; font-size: 0.9rem; margin-top: 20px;">NYC Precision. <br>Mexican Craft.</p>
            </div>
            <div>
                <h4>Studio</h4>
                <ul>
                    <li><a href="index.html">Work</a></li>
                    <li><a href="about.html">Profile</a></li>
                    <li><a href="blog.html">Journal</a></li>
                </ul>
            </div>
            <div>
                <h4>Connect</h4>
                <ul>
                    <li><a href="#">Instagram</a></li>
                    <li><a href="#">LinkedIn</a></li>
                    <li><a href="mailto:info@talacha.mx">Email</a></li>
                </ul>
            </div>
             <div>
                <h4>Directory</h4>
                <ul>
                    <li><a href="directory.html">View All 50 Zones</a></li>
                </ul>
            </div>
        </div>
    </footer>

</body>
</html>
"""

with open(output_file, 'w', encoding='utf-8') as f:
    f.write(html_content)

print(f"Successfully generated directory page: {output_file}")
