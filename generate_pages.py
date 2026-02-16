import json
import os

# Configuration
locations_file = 'locations.json'
template_file = 'location_template.html'
output_dir = 'locations'

# Create output directory
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# Load data
with open(locations_file, 'r', encoding='utf-8') as f:
    data = json.load(f)

# Load template
with open(template_file, 'r', encoding='utf-8') as f:
    template_content = f.read()

services = data['services']
locations = data['locations']

print(f"Found {len(services)} services and {len(locations)} locations.")
print(f"Generating {len(services) * len(locations)} pages...")

generated_count = 0

for service in services:
    for location in locations:
        # Prepare data for replacement
        slug = f"{service['slug']}-{location['slug']}"
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
                # Link to the SAME service type in the neighbor location
                # e.g., if on 'architects-polanco', link to 'architects-condesa'
                neighbor_slug = f"{service['slug']}-{neighbor['slug']}.html"
                nearby_html += f'<li><a href="{neighbor_slug}">Architecture in {neighbor["name"]}</a><span>Explore Zone &rarr;</span></li>'
        nearby_html += '</ul>'

        # Replace placeholders
        page_content = template_content
        page_content = page_content.replace("{{location_name}}", location['name'])
        page_content = page_content.replace("{{service_name}}", service['name'])
        page_content = page_content.replace("{{h1_title}}", h1_title)
        page_content = page_content.replace("{{intro_text}}", intro_text)
        page_content = page_content.replace("{{meta_description}}", meta_description)
        
        # Vibe & Narrative
        page_content = page_content.replace("{{vibe_description}}", location['vibe'])
        page_content = page_content.replace("{{lifestyle_vibe}}", location.get('lifestyle_vibe', ''))
        page_content = page_content.replace("{{history}}", location.get('history', ''))
        page_content = page_content.replace("{{landmarks}}", location.get('landmarks', ''))
        
        # Challenge / Solution
        page_content = page_content.replace("{{challenge_text}}", location['challenge'])
        page_content = page_content.replace("{{solution_text}}", location['solution'])
        
        # Intelligence Data
        page_content = page_content.replace("{{zoning_authority}}", location.get('zoning_authority', 'SEDUVI'))
        page_content = page_content.replace("{{permit_timeline}}", location.get('permit_timeline', '3-6 Months'))
        page_content = page_content.replace("{{cost_per_sqm}}", location.get('cost_per_sqm', 'Contact for Quote'))
        page_content = page_content.replace("{{focus_area_1}}", location['focus_areas'][0].title()) # Primary focus
        
        # Cheat Sheet Data
        page_content = page_content.replace("{{best_streets}}", best_streets_str)
        page_content = page_content.replace("{{hidden_gems}}", location.get('hidden_gems', 'Contact us'))
        page_content = page_content.replace("{{best_coffee}}", location.get('best_coffee', ''))
        page_content = page_content.replace("{{dining_scene}}", location.get('dining_scene', ''))
        page_content = page_content.replace("{{quirks}}", location.get('quirks', ''))
        
        # Investment
        page_content = page_content.replace("{{investment_outlook}}", location.get('investment_outlook', ''))
        page_content = page_content.replace("{{investor_tip}}", location.get('investor_tip', ''))
        
        # System
        page_content = page_content.replace("{{slug}}", slug)
        page_content = page_content.replace("{{location_slug}}", location['slug'])
        page_content = page_content.replace("{{nearby_links_html}}", nearby_html)
        
        # Write file
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(page_content)
        
        generated_count += 1

print(f"Successfully generated {generated_count} pages in '{output_dir}/'.")