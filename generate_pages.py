import json
import os

# Configuration
locations_file = 'locations.json'
modifiers_file = 'service_modifiers.json'
blog_file = 'blog.json'
template_file = 'location_template.html'
output_dir = 'locations'

# Create output directory
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# Load data
with open(locations_file, 'r', encoding='utf-8') as f:
    data = json.load(f)

with open(modifiers_file, 'r', encoding='utf-8') as f:
    modifiers = json.load(f)

with open(blog_file, 'r', encoding='utf-8') as f:
    blog_posts = json.load(f)

# Load template into memory
with open(template_file, 'r', encoding='utf-8') as f:
    template_content = f.read()

services = data['services']
locations = data['locations']

print(f"Found {len(services)} services and {len(locations)} locations.")
print(f"Generating {len(services) * len(locations)} unique pages...")

generated_count = 0

for service in services:
    service_slug = service['slug']
    # Get modifiers for this service (default to empty dict if not found)
    mods = modifiers.get(service_slug, {})
    
    for location in locations:
        # Prepare data for replacement
        slug = f"{service_slug}-{location['slug']}"
        filename = f"{slug}.html"
        filepath = os.path.join(output_dir, filename)
        
        h1_title = f"{service['h1_prefix']} {location['name']}"
        intro_text = service['intro'].replace("{{location_name}}", location['name'])
        meta_description = f"{service['meta_desc_prefix']} {location['name']}. {location['vibe']}"
        
        # Prepare lists for display (comma separated)
        best_streets_str = ", ".join(location.get('best_streets', []))
        
        # BUILD NEARBY LINKS HTML
        nearby_html = '<ul class="swiss-list" style="border-top: none;">'
        if 'nearby' in location:
            for neighbor in location['nearby']:
                neighbor_slug = f"{service_slug}-{neighbor['slug']}.html"
                nearby_html += f'<li><a href="{neighbor_slug}">{service["name"]} in {neighbor["name"]}</a><span>Explore Zone &rarr;</span></li>'
        nearby_html += '</ul>'

        # BUILD BLOG SECTION HTML
        blog_html = ""
        related_post = next((post for post in blog_posts if post['related_location'] == location['slug']), None)
        
        if related_post:
            blog_html = f"""
            <section class="section" style="background: #fafafa;">
                <div class="container grid-2" style="align-items: center;">
                    <img src="{related_post['image'].replace('../', '../')}" alt="{related_post['title']}" style="width: 100%; height: 350px; object-fit: cover;">
                    <div>
                        <p style="font-size: 0.9rem; text-transform: uppercase; letter-spacing: 0.1em; color: #999;">From the Journal</p>
                        <h2 style="margin: 10px 0;">{related_post['title']}</h2>
                        <p>{related_post['excerpt']}</p>
                        <a href="../blog/{related_post['slug']}.html" class="btn-secondary">Read Article</a>
                    </div>
                </div>
            </section>
            """

        # MERGE CONTENT
        # Vibe
        base_vibe = location.get('lifestyle_vibe', '')
        mod_vibe = mods.get('vibe_modifier', '').replace("{{location_name}}", location['name'])
        full_vibe = f"{base_vibe} <br><br><strong>Service Perspective:</strong> {mod_vibe}"
        
        # Investment
        base_invest = location.get('investment_outlook', '')
        mod_invest = mods.get('investment_modifier', '').replace("{{location_name}}", location['name'])
        full_invest = f"{base_invest} <br><br><strong>Market Insight:</strong> {mod_invest}"
        
        # Challenge
        base_challenge = location['challenge']
        mod_challenge = mods.get('challenge_modifier', '').replace("{{location_name}}", location['name'])
        full_challenge = f"{mod_challenge} <br>Furthermore, {base_challenge.lower()}"
        
        # Solution
        base_solution = location['solution']
        mod_solution = mods.get('solution_modifier', '').replace("{{location_name}}", location['name'])
        full_solution = f"{mod_solution} {base_solution}"

        # Reset page content from template
        page_content = template_content

        # Replace placeholders
        page_content = page_content.replace("{{location_name}}", location['name'])
        page_content = page_content.replace("{{service_name}}", service['name'])
        page_content = page_content.replace("{{h1_title}}", h1_title)
        page_content = page_content.replace("{{intro_text}}", intro_text)
        page_content = page_content.replace("{{meta_description}}", meta_description)
        
        # Vibe & Narrative (MERGED)
        page_content = page_content.replace("{{vibe_description}}", location['vibe'])
        page_content = page_content.replace("{{lifestyle_vibe}}", full_vibe)
        page_content = page_content.replace("{{history}}", location.get('history', ''))
        page_content = page_content.replace("{{landmarks}}", location.get('landmarks', ''))
        
        # Challenge / Solution (MERGED)
        page_content = page_content.replace("{{challenge_text}}", full_challenge)
        page_content = page_content.replace("{{solution_text}}", full_solution)
        
        # Intelligence Data
        page_content = page_content.replace("{{zoning_authority}}", location.get('zoning_authority', 'SEDUVI'))
        page_content = page_content.replace("{{permit_timeline}}", location.get('permit_timeline', '3-6 Months'))
        page_content = page_content.replace("{{cost_per_sqm}}", location.get('cost_per_sqm', 'Contact for Quote'))
        page_content = page_content.replace("{{focus_area_1}}", location['focus_areas'][0].title())
        
        # Cheat Sheet Data
        page_content = page_content.replace("{{best_streets}}", best_streets_str)
        page_content = page_content.replace("{{hidden_gems}}", location.get('hidden_gems', 'Contact us'))
        page_content = page_content.replace("{{best_coffee}}", location.get('best_coffee', ''))
        page_content = page_content.replace("{{dining_scene}}", location.get('dining_scene', ''))
        page_content = page_content.replace("{{quirks}}", location.get('quirks', ''))
        
        # Investment (MERGED)
        page_content = page_content.replace("{{investment_outlook}}", full_invest)
        page_content = page_content.replace("{{investor_tip}}", location.get('investor_tip', ''))
        
        # System
        page_content = page_content.replace("{{slug}}", slug)
        page_content = page_content.replace("{{location_slug}}", location['slug'])
        page_content = page_content.replace("{{nearby_links_html}}", nearby_html)
        page_content = page_content.replace("{{blog_section_html}}", blog_html)
        
        # Write file
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(page_content)
        
        generated_count += 1

print(f"Successfully generated {generated_count} unique pages in '{output_dir}/'.")
