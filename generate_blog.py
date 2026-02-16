import json
import os

# Config
blog_file = 'blog.json'
template_file = 'blog_template.html'
output_dir = 'blog'

if not os.path.exists(output_dir):
    os.makedirs(output_dir)

with open(blog_file, 'r') as f:
    posts = json.load(f)

with open(template_file, 'r') as f:
    template_content = f.read()

# Generate Individual Posts
for post in posts:
    content = template_content
    content = content.replace("{{title}}", post['title'])
    content = content.replace("{{date}}", post['date'])
    content = content.replace("{{excerpt}}", post['excerpt'])
    content = content.replace("{{content}}", post['content'])
    content = content.replace("{{related_location}}", post['related_location'])
    content = content.replace("{{image}}", post['image'])
    
    filename = f"{output_dir}/{post['slug']}.html"
    with open(filename, 'w') as f:
        f.write(content)

# Generate Index Page (blog.html)
index_html = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Journal | Talacha</title>
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
</head>
<body>
    <header class="header">
        <a href="index.html" class="logo"><img src="img/logo.svg" alt="Talacha Logo"></a>
        <nav>
            <ul class="nav-links">
                <li><a href="index.html">Work</a></li>
                <li><a href="about.html">Studio</a></li>
                <li><a href="blog.html">Journal</a></li>
            </ul>
        </nav>
    </header>
    <main class="section" style="padding-top: 150px;">
        <div class="container">
            <h1 style="margin-bottom: 60px;">Journal</h1>
            <div class="grid-3">
"""

for post in posts:
    index_html += f"""
        <div>
            <a href="blog/{post['slug']}.html" style="border: none;">
                <img src="{post['image'].replace('../', '')}" style="width: 100%; height: 250px; object-fit: cover; margin-bottom: 20px;">
                <p style="font-size: 0.8rem; color: #999; text-transform: uppercase;">{post['date']}</p>
                <h3 style="font-size: 1.5rem; margin: 10px 0;">{post['title']}</h3>
                <p style="font-size: 1rem; color: #555;">{post['excerpt']}</p>
            </a>
        </div>
    """

index_html += """
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

with open('blog.html', 'w') as f:
    f.write(index_html)

print("Blog generated.")
