import json
import os
import google.generativeai as genai
import time

# --- CONFIGURATION ---
locations_file = 'locations.json'
md_dir = 'neighborhood-context'
os.environ["GOOGLE_API_KEY"] = "AIzaSyB9XNx8sV1H5rTi8OUfUlmVGxXNKplSqF8"
genai.configure(api_key=os.environ["GOOGLE_API_KEY"])

# --- LOAD DATA ---
with open(locations_file, 'r', encoding='utf-8') as f:
    data = json.load(f)

locations = data['locations']

# --- GOLD STANDARD TEMPLATE (CONDESA) ---
# We use the structure of what the user wants based on the Condesa page content provided in previous context.
# This JSON structure reflects the ideal output schema.
condesa_example = {
    "page_title": "English-Speaking Architects: Condesa | 2026 Investment & Technical Guide",
    "hero_h1": "Building Your Dream in Condesa",
    "hero_text": "You've seen the Amsterdam oval on Instagram; now learn what it takes to own it. We bridge the gap between US NCARB/AIA standards and local CDMX reality, transforming Art Deco relics into 2026-ready assets.",
    "intel": {
        "authority": "INBA (Heritage)",
        "timeline": "12 - 36 Months",
        "cost": "$1,800 - $3,000 USD",
        "focus": "Art Deco Restoration"
    },
    "resident_view": "I live on Mazatlán. I know the sound of the <strong>gasero</strong> at 7 AM and the rhythm of the Amsterdam dog-walk. Building here is a love letter to a sinking lakebed.",
    "landmarks": [
        "Edificio Basurto (Art Deco)",
        "Parque México Clock Tower",
        "The Edificio Condesa"
    ],
    "main_content": {
        "h1": "Living in a Countess's Estate",
        "p1": "Condesa takes its name from the Countess of Miravalle, whose 18th-century estate once covered this entire zone. By the 1920s, the estate's private horse racing track was subdivided, creating the unique oval shape of <strong>Avenida Amsterdam</strong> that defines the neighborhood today. Life here moves at a human pace, balanced between the leafy refuge of Parque España and a sidewalk café culture that feels more Parisian than North American.",
        "h2": "The Architecture of the \"Hipódromo\"",
        "p2": "Building in Condesa means working within the highest concentration of Art Deco architecture in the Western Hemisphere. You'll find \"Aztec Deco\" gems alongside Streamline Moderne masterpieces. As your architect, my job is to preserve these <strong>good bones</strong> while stripping away 80 years of decaying systems to make way for 2026 technology.",
        "structural_title": "Structural Specialty: The Lakebed Reality",
        "structural_text": "The biggest secret of Condesa? The ground is moving. We are in <strong>Seismic Zone III</strong>, which means the neighborhood sits on 50+ meters of soft, high-plasticity clay from the ancient Lake Texcoco bed. These clays amplify seismic waves significantly compared to the firm rock of Santa Fe.",
        "structural_sub": "For your project, \"standard\" foundations won't cut it. We specialize in <strong>seismic retrofitting</strong> using carbon fiber wrapping and friction piles that reach into the deeper, firmer strata. We bridge the gap between US NCARB/AIA rigorous engineering standards and the local <strong>maistro</strong> labor practices, ensuring that your investment stays standing when the earth moves.",
        "heritage_title": "Heritage Integration: Navigating INAH & INBAL",
        "heritage_text_1": "Condesa is an <strong>Área de Conservación Patrimonial</strong>. If your property was built before 1900, it falls under <strong>INAH</strong> (National Institute of Anthropology and History). If it's a 20th-century Art Deco masterpiece, it's governed by <strong>INBAL</strong> (Fine Arts).",
        "heritage_text_2": "Renovating a facade here is not a matter of taste; it's a matter of law. INBAL mandates specific color palettes—often limited to whites, grays, and earth tones like <strong>Pantone 465 C</strong> (gold-tan) or <strong>7420 C</strong> (deep red). You must replicate original iron or wood window profiles; swapping them for aluminum is strictly prohibited. Our role is to navigate these <strong>Heritage Hurdles</strong> so you avoid <strong>Clausurado</strong> (stoppage) stickers.",
        "water_title": "The Cutzamala Crisis & Your Cistern",
        "water_text": "The <strong>Cutzamala system</strong> is the massive network of dams and pipelines pumping water across mountains to supply Mexico City. It currently faces a 40% leakage rate and historic infrastructure strain. In Condesa, we assume the grid will fail. We integrate a minimum <strong>10,000-liter cistern</strong> per property as a standard <strong>Life-Insurance</strong> policy, ensuring you have water even when the Cutzamala undergoes maintenance."
    },
    "feasibility": [
        {"type": "Heritage Renovation", "time": "18 - 36 Months", "risk": "High (Zone III)", "status": "Strict (INBAL/INAH)"},
        {"type": "New Build (H/3/20)", "time": "12 - 24 Months", "risk": "High (Friction Piles)", "status": "Contextual Oversight"},
        {"type": "Interior Overhaul", "time": "3 - 6 Months", "risk": "Low Impact", "status": "Internal Freedom"}
    ],
    "renovations": {
        "title": "Specialized Renovations",
        "text": "Restoring a Condesa Art Deco building is an exercise in <strong>Invisible Modernization</strong>. We keep the soul—the high ceilings, the volcanic <strong>recinto</strong> floors—while completely overhauling the plumbing, electrical, and soundproofing. We install <strong>multichamber PVC windows</strong> to block 45 dB of street noise, ensuring your home is as quiet as a New York penthouse."
    },
    "interiors": {
        "title": "High-End Interior Design",
        "text": "Our interior philosophy for Condesa is <strong>Mexican Modernism</strong>. We source local <strong>cantera</strong> stone and <strong>chukum</strong> plaster to create spaces grounded in CDMX but functioning to international luxury standards. Lighting is our secret weapon, designed to mitigate the deep, narrow floor plans of historic buildings."
    },
    "cheat_sheet": {
        "streets": "Amsterdam, Veracruz, Mazatlán",
        "zoning": "H/3/20 or HM/5/20",
        "cost": "MXN 30k - 50k (Luxury Finish)",
        "coffee": "Chiquitito Café or Blend Station",
        "quirk": "The highest concentration of dogs per capita in Mexico."
    },
    "challenge": {
        "text_1": "The primary challenge in Condesa is balancing modern openness with the structural realities of lakebed soil and strict heritage protections.",
        "text_2": "In the Cuauhtémoc Alcaldía, you don't just \"get a permit.\" You file a <strong>Manifestación de Construcción</strong>. The <strong>DRO (Director Responsable de Obra)</strong> carries personal legal liability for your building's structural safety."
    },
    "solution": {
        "text_1": "We use lightweight steel framing and advanced glazing to bring light into these structures while reinforcing seismic resistance. We specialize in facades that look 1925 but perform like 2026.",
        "text_2": "We eliminate the <strong>Gringo Tax</strong> through radical transparency. While international owners are often quoted MXN 60,000/m², the fair market rate for luxury CDMX labor ranges from <strong>MXN 30,000 to 50,000</strong>."
    }
}

# --- GEMINI MODEL SETUP ---
model = genai.GenerativeModel('gemini-2.5-flash')

def generate_content(location_name, location_slug, md_content):
    prompt = f"""
    You are an expert architectural copywriter specializing in ultra-high-net-worth real estate in Mexico City. 
    Your goal is to write website copy for a page about {location_name}. 
    
    SOURCE MATERIAL:
    Use the following markdown research to inform your writing. Be specific, technical, and accurate based on this text:
    {md_content}

    CORE GUIDELINES:
    1. Write a Love Letter with a Hard Edge: Describe the neighborhood's beauty with deep affection, but anchor every claim in 2026 data. If the soil is soft, say it. If the permits are a nightmare, explain why. Find or describe a specific, curious, or interesting fact that is not common knowledge. (Example: A secret acoustic canyon, a specific street name origin, or a hidden architectural detail only a resident would notice).
    
    2. 2026 Context: Discuss the neighborhood as it exists today in 2026—mention the impact of the "Cutzamala" water updates, the rise of the digital nomad economy, and current 2026 ROI trends. Connect the neighborhood's 18th or 19th-century origins to its 2026 reality. How has the original urban plan (e.g., Porfirian estates or colonial villas) dictated the way people live there today?
    
    3. Technical Specificity: Use architectural and legal jargon accurately (e.g., Manifestación de Construcción, DRO, INBAL, Land Use H/3/20). Detail the specific conservation rules (INAH/INBAL). What are the exact "Heritage Hurdles" a buyer will face? Mention specific facades or cataloged streets. Focus on the "Geotechnical Reality." Is it Zone I (Firm), II (Transition), or III (Lakebed)? Explain how this specific soil affects luxury renovations and foundation costs. Explain how we bridge the gap between US NCARB/AIA standards and local CDMX maistro labor to eliminate the "Gringo Tax."

    4. Forbidden Phrases: Never use "vibrant heart," "hidden gem," or "unforgettable experience."

    STYLE GUIDE:
    - Tone: Sophisticated, warm but authoritative, "insider", expensive, architectural, precise.
    - Voice: First-person plural ("We") or First-person singular ("I") for the resident view.
    - Formatting: Use HTML <strong> tags for emphasis on key terms (like specific materials, zoning codes, or local slang). Do NOT use markdown **bold**.
    - Length: The copy must be substantial, detailed, and at least as long as the example below.
    
    OUTPUT FORMAT:
    You must output a valid JSON object that exactly matches the structure of the example below. Do not wrap it in markdown code blocks. Just return the raw JSON string.

    EXAMPLE (This is the "Gold Standard" for Condesa. Match this structure and depth):
    {json.dumps(condesa_example)}

    SPECIFIC INSTRUCTIONS FOR {location_name}:
    - "resident_view": Write as a local architect who lives in Condesa but deeply admires this neighborhood. Describe what draws you here—a specific dish, the unique light at 5 PM, or the architectural character—without claiming residence. Keep it intimate and sensory.
    - "cheat_sheet": Extract real data.
    - "feasibility": Create 3 realistic project scenarios based on the markdown data.
    """
    
    try:
        response = model.generate_content(prompt)
        # Simple cleanup to ensure valid JSON if the model adds markdown ticks
        clean_text = response.text.strip()
        if clean_text.startswith("```json"):
            clean_text = clean_text[7:]
        if clean_text.endswith("```"):
            clean_text = clean_text[:-3]
        return json.loads(clean_text)
    except Exception as e:
        print(f"Error generating {location_name}: {e}")
        return None

# --- MAIN LOOP ---
updated_locations = []
existing_slugs = {loc['slug']: loc for loc in locations}

# Get list of all markdown files
md_files = [f for f in os.listdir(md_dir) if f.endswith('.md')]

for md_file in md_files:
    slug = md_file.replace('.md', '')
    
    # Handle filename discrepancies
    if slug == 'lomas':
        target_slug = 'lomas-de-chapultepec'
    else:
        target_slug = slug
        
    print(f"Processing {target_slug} from {md_file}...")
    
    if target_slug == 'condesa':
        print("Skipping Condesa (Manual Master)...")
        updated_locations.append(existing_slugs['condesa'])
        continue

    # Prepare location object
    if target_slug in existing_slugs:
        loc = existing_slugs[target_slug]
    else:
        # Create new entry
        name = slug.replace('-', ' ').title()
        # Fix specific capitalizations if needed
        if name == 'Coyoacan': name = 'Coyoacán'
        if name == 'Juarez': name = 'Juárez'
        
        loc = {
            "name": name,
            "slug": target_slug
        }
        
    md_path = os.path.join(md_dir, md_file)
    with open(md_path, 'r', encoding='utf-8') as f:
        md_content = f.read()
        
    generated_data = generate_content(loc['name'], loc['slug'], md_content)
    
    if generated_data:
        loc.update(generated_data)
        updated_locations.append(loc)
        print(f"Successfully generated copy for {loc['name']}")
        time.sleep(2) # Avoid rate limits
    else:
        print(f"Failed to generate for {loc['name']}, keeping old data (if any).")
        if target_slug in existing_slugs:
            updated_locations.append(existing_slugs[target_slug])

# Ensure we don't lose any existing locations that didn't have markdown files (if any)
processed_slugs = [l['slug'] for l in updated_locations]
for loc in locations:
    if loc['slug'] not in processed_slugs:
        print(f"Warning: {loc['slug']} had no markdown file but exists in JSON. Keeping it.")
        updated_locations.append(loc)

# Sort alphabetically by name for tidiness
updated_locations.sort(key=lambda x: x['name'])

# --- SAVE ---
data['locations'] = updated_locations
with open(locations_file, 'w', encoding='utf-8') as f:
    json.dump(data, f, indent=2, ensure_ascii=False)

print("All locations updated.")
