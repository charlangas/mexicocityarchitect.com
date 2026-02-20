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

locations = data['locations']
services = data['services'] 

print(f"Generating pages for {len(locations)} locations...")

for location in locations:
    # SKIP CONDESA COMPLETELY TO PRESERVE MANUAL EDITS
    if location['slug'] == 'condesa':
        print("Skipping Condesa (Manual Override)...")
        continue

    for service in services:
        service_slug = service['slug']
        
        # Prepare filename
        slug = f"{service_slug}-{location['slug']}"
        filename = f"{slug}.html"
        filepath = os.path.join(output_dir, filename)
        
        # Prepare dynamic content
        page_content = template_content
        
        # Core Identity
        page_content = page_content.replace("{{location_name}}", location['name'])
        page_content = page_content.replace("{{location_slug}}", location['slug'])
        page_content = page_content.replace("{{slug}}", slug)
        
        # Meta & Hero
        page_content = page_content.replace("{{page_title}}", location['page_title'])
        page_content = page_content.replace("{{meta_description}}", f"{service['meta_desc_prefix']} {location['name']}. {location['hero_text']}")
        page_content = page_content.replace("{{hero_h1}}", location['hero_h1'])
        page_content = page_content.replace("{{hero_text}}", location['hero_text'])
        
        # Intelligence Grid
        page_content = page_content.replace("{{intel_authority}}", location['intel']['authority'])
        page_content = page_content.replace("{{intel_timeline}}", location['intel']['timeline'])
        page_content = page_content.replace("{{intel_cost}}", location['intel']['cost'])
        page_content = page_content.replace("{{intel_focus}}", location['intel']['focus'])
        
        # Sidebar
        page_content = page_content.replace("{{resident_view}}", location['resident_view'])
        
        # Landmarks List
        landmarks_html = ""
        for landmark in location['landmarks']:
            landmarks_html += f"<li>{landmark}</li>"
        page_content = page_content.replace("{{landmarks_list}}", landmarks_html)
        
        # Main Narrative
        content = location['main_content']
        page_content = page_content.replace("{{main_h1}}", content['h1'])
        page_content = page_content.replace("{{main_p1}}", content['p1'])
        page_content = page_content.replace("{{main_h2}}", content['h2'])
        page_content = page_content.replace("{{main_p2}}", content['p2'])
        
        page_content = page_content.replace("{{structural_title}}", content['structural_title'])
        page_content = page_content.replace("{{structural_text}}", content['structural_text'])
        page_content = page_content.replace("{{structural_sub}}", content['structural_sub'])
        
        page_content = page_content.replace("{{heritage_title}}", content['heritage_title'])
        page_content = page_content.replace("{{heritage_text_1}}", content['heritage_text_1'])
        page_content = page_content.replace("{{heritage_text_2}}", content['heritage_text_2'])
        
        page_content = page_content.replace("{{water_title}}", content['water_title'])
        page_content = page_content.replace("{{water_text}}", content['water_text'])
        
        # Feasibility Table
        rows_html = ""
        for row in location['feasibility']:
            rows_html += f"""
            <tr style="border-bottom: 1px solid #eee;">
                <td style="padding: 20px;">{row['type']}</td>
                <td>{row['time']}</td>
                <td>{row['risk']}</td>
                <td>{row['status']}</td>
            </tr>
            """
        page_content = page_content.replace("{{feasibility_rows}}", rows_html)
        
        # Renovations & Interiors
        page_content = page_content.replace("{{renovations_title}}", location['renovations']['title'])
        page_content = page_content.replace("{{renovations_text}}", location['renovations']['text'])
        page_content = page_content.replace("{{interiors_title}}", location['interiors']['title'])
        page_content = page_content.replace("{{interiors_text}}", location['interiors']['text'])
        
        # Cheat Sheet
        print(f"Processing cheat sheet for {location['name']}")
        cheat = location['cheat_sheet']
        page_content = page_content.replace("{{cheat_streets}}", cheat['streets'])
        page_content = page_content.replace("{{cheat_zoning}}", cheat['zoning'])
        page_content = page_content.replace("{{cheat_cost}}", cheat['cost'])
        page_content = page_content.replace("{{cheat_coffee}}", cheat['coffee'])
        page_content = page_content.replace("{{cheat_quirk}}", cheat['quirk'])
        
        # Challenge / Solution
        page_content = page_content.replace("{{challenge_text_1}}", location['challenge']['text_1'])
        page_content = page_content.replace("{{challenge_text_2}}", location['challenge']['text_2'])
        page_content = page_content.replace("{{solution_text_1}}", location['solution']['text_1'])
        page_content = page_content.replace("{{solution_text_2}}", location['solution']['text_2'])
        
        # Nearby Links
        nearby_html = '<ul class="swiss-list" style="border-top: none;">' # Removed swiss-list per observation, but user said 'like Condesa', Condesa file uses <ul>. 
        # Actually Condesa file had <ul> but template had <ul class='swiss-list'> before. 
        # I will use simple UL to match Condesa exactly as read from file.
        nearby_html = '<ul>'
        
        count = 0
        for other_loc in locations:
            if other_loc['slug'] != location['slug'] and count < 3:
                neighbor_slug = f"architects-{other_loc['slug']}.html" 
                nearby_html += f'<li><a href="{neighbor_slug}">{other_loc["name"]}</a></li>'
                count += 1
                
        nearby_html += '</ul>'
        page_content = page_content.replace("{{nearby_links_html}}", nearby_html)

        # Write file
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(page_content)
            
print("Done.")