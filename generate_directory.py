import json
import os

# Configuration
locations_file = 'locations.json'
output_file = 'directory.html'

# Load data
with open(locations_file, 'r', encoding='utf-8') as f:
    data = json.load(f)

locations = data['locations']

# HTML Header
html_content = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="description" content="Explore our architectural guides for Mexico City's premier neighborhoods.">
    <title>Neighborhoods | Talacha</title>
    <link rel="stylesheet" href="style.css">
    <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@400;600;700&display=swap" rel="stylesheet">
    <link href="https://fonts.googleapis.com/css2?family=Newsreader:opsz,wght@6..72,300;6..72,400;6..72,600&display=swap" rel="stylesheet">
    <!-- Google tag (gtag.js) -->
    <script async src="https://www.googletagmanager.com/gtag/js?id=G-YBB82P1LG1"></script>
    <script>
      window.dataLayer = window.dataLayer || [];
      function gtag(){dataLayer.push(arguments);}
      gtag('js', new Date());

      gtag('config', 'G-YBB82P1LG1');
    </script>
    <style>
        .directory-grid {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(350px, 1fr));
            gap: 40px;
            margin-top: 60px;
        }
        .neighborhood-card {
            border: 1px solid #000;
            transition: transform 0.2s;
            display: flex;
            flex-direction: column;
        }
        .neighborhood-card:hover {
            transform: translateY(-5px);
        }
        .neighborhood-image {
            width: 100%;
            height: 250px;
            object-fit: cover;
            border-bottom: 1px solid #000;
            filter: grayscale(100%);
            transition: filter 0.3s;
        }
        .neighborhood-card:hover .neighborhood-image {
            filter: grayscale(0%);
        }
        .card-content {
            padding: 30px;
            flex-grow: 1;
            display: flex;
            flex-direction: column;
            justify-content: space-between;
        }
        .card-content h2 {
            font-size: 1.8rem;
            margin-bottom: 15px;
        }
        .card-content p {
            font-size: 1rem;
            color: #666;
            margin-bottom: 25px;
            line-height: 1.6;
        }
    </style>
</head>
<body>

    <header class="header">
        <a href="index.html" class="logo"><img src="img/logo.svg" alt="Talacha Logo"></a>
        <nav>
            <ul class="nav-links">
                <li><a href="index.html">Work</a></li>
                <li><a href="about.html">Studio</a></li>
                <li><a href="blog.html">Journal</a></li>
                <li><a href="index.html#contact">Contact</a></li>
            </ul>
        </nav>
    </header>

    <main class="section" style="padding-top: 150px;">
        <div class="container">
            <h1 style="margin-bottom: 20px;">Neighborhoods</h1>
            <p>Comprehensive architectural guides for Mexico City's most desirable zones.</p>
            
            <div class="directory-grid">
"""

# Generate Cards
for loc in locations:
    name = loc['name']
    slug = loc['slug']
    
    # Get a short description (first sentence of hero_text or resident_view if hero_text is too marketing-y)
    # Using hero_text but truncating to first sentence.
    description = loc.get('hero_text', '')
    if '.' in description:
        description = description.split('.')[0] + '.'
    
    # Image path
    image_path = f"img/locations/{slug}-hero.png"
    
    # Link
    link = f"locations/architects-{slug}.html"
    
    card_html = f"""
                <div class="neighborhood-card">
                    <a href="{link}" style="border: none;">
                        <img src="{image_path}" alt="{name}" class="neighborhood-image">
                        <div class="card-content">
                            <div>
                                <h2>{name}</h2>
                                <p>{description}</p>
                            </div>
                            <span class="btn-secondary" style="text-align: center; width: 100%;">View Guide</span>
                        </div>
                    </a>
                </div>
    """
    html_content += card_html

# HTML Footer
html_content += """
            </div>
        </div>
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
                    <li><a href="tel:+525594356985">55 9435 6985</a></li>
                </ul>
            </div>
             <div>
                <h4>Directory</h4>
                <ul>
                    <li><a href="directory.html">View all neighborhoods</a></li>
                </ul>
            </div>
        </div>
    </footer>

</body>
</html>
"""

# Write File
with open(output_file, 'w', encoding='utf-8') as f:
    f.write(html_content)

print(f"Successfully generated {output_file}")