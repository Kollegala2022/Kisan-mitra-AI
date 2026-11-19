"""
Ingest agricultural knowledge documents into the vector store
"""
from datetime import datetime
from sqlalchemy.orm import Session
from app.database.models import KnowledgeDocument
from app.rag.retriever import get_retriever


def add_knowledge_documents_to_rag(db: Session) -> None:
    """
    Add all knowledge documents from database to the RAG vector store
    """
    retriever = get_retriever()
    
    # Fetch all documents from database
    documents = db.query(KnowledgeDocument).all()
    
    # Format for RAG
    formatted_docs = []
    for doc in documents:
        formatted_docs.append({
            "id": doc.id,
            "content": f"{doc.title}\n\n{doc.content}",
            "metadata": {
                "title": doc.title,
                "topic": doc.topic,
                "crop": doc.crop,
                "district": doc.district,
                "source_name": doc.source_name,
                "source_url": doc.source_url,
                "language": doc.language
            }
        })
    
    if formatted_docs:
        retriever.add_documents(formatted_docs)


def seed_initial_knowledge_base(db: Session) -> None:
    """
    Seed the database with initial knowledge documents if they don't exist
    """
    # Check if documents already exist
    existing_count = db.query(KnowledgeDocument).count()
    if existing_count > 0:
        print(f"Knowledge base already has {existing_count} documents")
        return
    
    # Initial agricultural knowledge documents
    initial_documents = [
        KnowledgeDocument(
            title="Ragi (Finger Millet) Cultivation Guide",
            topic="crop",
            crop="Ragi",
            district=None,
            content="""Ragi, also known as finger millet, is a highly nutritious cereal crop suitable for Karnataka.

Growing Season: June to October (Kharif season)

Suitable Districts: All districts of Karnataka

Soil Requirements:
- Well-drained sandy loam or loam soil
- pH 5.0 to 7.0
- Good organic matter content

Sowing:
- Sow seeds at 5-6 kg/hectare
- Spacing: 22.5 cm x 10 cm
- Best time: June-July

Water Requirements:
- Moderate water requirements
- 4-5 irrigations during the season
- Requires 50-100 cm annual rainfall

Fertilizer:
- Apply 60 kg N, 30 kg P2O5, 30 kg K2O per hectare
- Use FYM 10 tonnes/hectare

Common Pests:
- Shoot fly, leaf folder, stem borer
- Control with neem spray

Diseases:
- Leaf blast (most common), neck blast
- Use resistant varieties
- Proper drainage prevents fungal diseases

Harvesting:
- Ready in 3-4 months
- When the color changes from green to brown
- Cut and dry in sun for 5-7 days

Yield: 15-20 quintals per hectare

Advantages:
- Drought tolerant
- Nutritious grain
- Low input crop
- Good market demand""",
            source_name="Karnataka Agriculture Department",
            source_url="https://agriculture.karnataka.gov.in",
            reviewed_date=datetime.utcnow(),
            language="en"
        ),
        KnowledgeDocument(
            title="Tomato Cultivation Best Practices",
            topic="crop",
            crop="Tomato",
            district=None,
            content="""Tomato is an important vegetable crop widely grown in Karnataka.

Growing Season: September to February (Kharif), February to June (Summer)

Suitable Districts: All districts, especially Belgaum, Kolar, Tumkur

Soil Requirements:
- Well-drained loamy soil
- pH 6.0 to 6.8
- Rich in organic matter

Varieties: Local, Hybrid F1, Pusa Ruby, Lakhanpal, etc.

Sowing to Planting:
- Nursery sowing: 6-8 weeks before planting
- Seed rate: 200-250 g per hectare
- Transplanting at 6-8 leaf stage

Spacing: 60 cm x 45 cm or 75 cm x 60 cm

Water Management:
- Heavy feeder crop
- Irrigation every 7-10 days
- Drip irrigation recommended

Fertilizer:
- 50 kg N, 50 kg P2O5, 50 kg K2O per hectare
- Apply in splits
- 25 tonnes FYM per hectare

Support and Training:
- Use bamboo poles or concrete structures
- Train to single stem for better quality
- Remove lower leaves for air circulation

Common Diseases:
- Early blight: Brownish spots with concentric rings
  Control: Remove affected leaves, spray carbendazim
- Late blight: Water-soaked spots
  Control: Improve drainage, use Bordeaux mixture
- Leaf curl virus: Upward curling of leaves
  Control: Control whiteflies with neem spray

Common Pests:
- Fruit borer, whitefly, aphids
- Use sticky traps, neem spray
- Install pheromone traps

Harvesting: 60-80 days after transplanting
- Pick at light pink stage for transport
- Pink or fully ripe for local market

Yield: 25-30 tonnes per hectare

Issues and Solutions:
- Yellow leaves: Usually nitrogen deficiency, apply urea
- Flower drop: Temperature stress or water stress
- Cracked fruits: Irregular watering, maintain consistent moisture""",
            source_name="Karnataka Horticulture Department",
            source_url="https://horticulture.karnataka.gov.in",
            reviewed_date=datetime.utcnow(),
            language="en"
        ),
        KnowledgeDocument(
            title="Onion Cultivation Guide",
            topic="crop",
            crop="Onion",
            district=None,
            content="""Onion is a major cash crop in Karnataka, particularly in the northern districts.

Growing Season: September to May (Main crop), February to August (Summer)

Suitable Districts: Belgaum, Gadag, Bagalkot, Bijapur (Northern Karnataka)

Climate: Cool season crop, 15-25°C ideal

Soil Requirements:
- Well-drained loamy to clayey loam
- pH 6.5 to 7.5
- Rich in organic matter (25-30 tonnes/hectare)

Varieties: N-257-9, Arka Niketan, Nasik, Bangalore Rose

Bulb Sowing: August-September (for October planting)
- Seed rate: 4-5 kg per hectare for nursery
- Transplanting at 6-8 weeks
- Transplanting spacing: 15-20 cm x 10-12 cm

Water Requirements:
- 12-15 irrigations during season
- Critical period: Bulb formation stage
- Drip irrigation saves 40% water

Fertilizer:
- 120 kg N, 60 kg P2O5, 60 kg K2O per hectare
- Nitrogen in splits (1/3 at planting, rest in 2-3 splits)

Weed Management:
- 2-3 hand weedings at 45, 75, 105 days
- Mulching reduces weeds

Diseases:
- Purple blotch: Brown spots with purple margin
  Control: Mancozeb spray 0.2%, improve drainage
- Basal rot: Fungal, affects stored bulbs
  Control: Avoid water-logging, cure bulbs properly

Pests:
- Thrips: Silvering of leaves
  Control: Neem spray, yellow sticky traps
- Stem fly: Wilting of seedlings
  Control: Avoid continuous onion cultivation

Harvesting: 4-5 months after transplanting
- When 50% tops fall
- Lift and dry in field for 3-5 days
- Continue drying in shade for 1-2 weeks

Storage:
- Store in well-ventilated rooms at 0-1°C
- Can be stored 6-8 months

Yield: 25-30 tonnes per hectare fresh, 5-6 tonnes dried

Tips for Quality Bulbs:
- Choose high quality seed
- Maintain optimal spacing
- Avoid excess nitrogen to prevent double bulbs
- Proper curing extends storage life""",
            source_name="Department of Agriculture, Belgaum",
            source_url="https://belgaum.nic.in",
            reviewed_date=datetime.utcnow(),
            language="en"
        ),
        KnowledgeDocument(
            title="Irrigation Management for Karnataka Farmers",
            topic="irrigation",
            crop=None,
            district=None,
            content="""Efficient irrigation is crucial for maximizing crop yield while conserving water in Karnataka.

Types of Irrigation:
1. Flood Irrigation: Traditional, uses more water, suitable for rice
2. Drip Irrigation: Water-efficient, saves 40-50% water, ideal for vegetables
3. Sprinkler Irrigation: Uniform coverage, 30-40% water saving
4. Micro-sprinkler: For fruits and horticultural crops

Drip Irrigation Benefits:
- 30-50% water saving compared to flood irrigation
- Better fertilizer efficiency
- Reduced disease incidence
- Suitable for undulating terrain
- Lower labor cost in long run

System Cost: Rs. 40,000-80,000 per hectare (subsidy available in some districts)

Sprinkler Irrigation:
- Suitable for vegetables, cereals, pulses
- Reduces soil compaction
- Better water penetration
- Effective for sandy soils

When to Irrigate:
- Based on soil moisture content
- Visible wilting is late indicator
- Use tensiometers for precise measurement
- Critical periods: flowering, fruit formation

Water Requirement by Crop (Seasonal):
- Rice: 100-120 cm
- Wheat: 40-60 cm
- Sugarcane: 150-200 cm
- Cotton: 60-90 cm
- Groundnut: 40-60 cm
- Vegetables: 50-80 cm

Scheduling Irrigation:
1. Determine soil moisture at root zone
2. Calculate water deficit
3. Apply irrigation to refill root zone
4. Consider rainfall in calculations

Micro-irrigation Subsidy:
- Many districts offer 50-90% subsidy
- Apply through taluk agriculture office
- Check eligibility in your district

Water Sources:
- Borewells: Check water quality
- Open wells: Regular maintenance needed
- Tanks/lakes: Seasonal availability
- Canals: Scheduled water release

Water Quality:
- Check EC (electrical conductivity) before use
- Saline water affects soil structure
- High fluoride water problematic for drinking crops
- Drip lines clog with high sediment water

Tips:
- Mulching reduces water requirement by 25-30%
- Schedule irrigation in early morning/evening
- Monitor soil moisture with simple feel method
- Keep irrigation records for planning""",
            source_name="Water Resources Department, Karnataka",
            source_url="https://wrd.karnataka.gov.in",
            reviewed_date=datetime.utcnow(),
            language="en"
        ),
        KnowledgeDocument(
            title="Common Crop Diseases and Management",
            topic="disease",
            crop=None,
            district=None,
            content="""Understanding common crop diseases helps farmers prevent and manage them effectively.

Fungal Diseases:

1. Powdery Mildew (Wheat, Pea, Grape, Cucumber):
- White powder on leaves
- Control: Sulphur spray 0.5% or Karathane 0.1%
- Avoid dense planting
- Improve air circulation

2. Leaf Spot/Leaf Blight:
- Brown spots on leaves
- Control: Remove affected leaves, spray copper fungicide
- Ensure good drainage
- Avoid overhead irrigation

3. Rust (Wheat):
- Orange/brown pustules on leaves
- Control: Use resistant varieties
- Spray Propiconazole 0.1%
- Timely sowing prevents late rust

Bacterial Diseases:

1. Bacterial Blight:
- Water-soaked spots with yellow halo
- Control: Use certified seed
- Crop rotation essential
- Spray Bordeaux mixture
- No cure once established

2. Bacterial Leaf Streak:
- Long streaks on leaves
- Control: Remove infected plants
- Clean equipment between fields

Viral Diseases:

1. Mosaic Virus (Tobacco, Tomato, Papaya):
- Mosaic pattern on leaves, reduced growth
- Control: Manage vector insects (aphids, whiteflies)
- Remove infected plants immediately
- Use disease-free seed

2. Leaf Curl Virus:
- Upward curling, yellowing of leaves
- Control: Spray insecticide for whitefly
- Use resistant varieties
- Remove infected plants

Crop-Specific Diseases:

Rice:
- Blast disease (gray spots with dark outline)
- Sheath blight (water-soaked lesions)
- Brown spot (circular spots with brown margin)

Wheat:
- Loose smut (black powder in grains)
- Powdery mildew
- Leaf rust, stem rust

Cotton:
- Leaf spot, boll rot
- Fusarium wilt

Sugarcane:
- Red rot (red coloring internally)
- Smut (black dust instead of sugar cane)

Prevention Best Practices:
1. Use healthy, certified seed
2. Practice crop rotation (at least 2-3 year gap)
3. Field sanitation (remove crop residue)
4. Proper spacing for air circulation
5. Avoid waterlogging
6. Monitor fields regularly
7. Identify diseases early
8. Isolate infected plants

When to Spray:
- At first sign of disease
- Follow fungicide/bactericide instructions
- Maintain spray schedule
- Spray during cool hours (morning/evening)
- Ensure good coverage

Note: Always consult your local agriculture extension officer for specific disease identification and management in your area.""",
            source_name="AICVIP (All India Coordinated Vegetable Improvement Project)",
            source_url="https://aicvip.icar.gov.in",
            reviewed_date=datetime.utcnow(),
            language="en"
        ),
        KnowledgeDocument(
            title="Pest Management in Crops",
            topic="pest",
            crop=None,
            district=None,
            content="""Integrated Pest Management (IPM) is the most effective approach for controlling crop pests.

Common Agricultural Pests:

1. Bollworm (Cotton, Vegetable crops):
- Larvae feed on flowers and fruits
- Creates holes in fruits
- Control: Hand-pick egg masses, spray NPV or SNPV
- Use pheromone traps
- Avoid excessive nitrogen

2. Leaf Folder (Rice, Maize, Other cereals):
- Larvae fold leaves and feed inside
- Causes skeletonization
- Control: Spray chlorpyrifos 20 EC (1.5 ml/liter)
- Maintain proper spacing
- Remove infested leaves

3. Stem Borer (Maize, Rice, Sugarcane):
- Larvae bore into stems, cause deadhearts
- Control: Use resistant varieties
- Spray Quinalphos 25 EC at boot leaf stage
- Remove and burn affected plants
- Plant border crops

4. Whitefly (Cotton, Okra, Tomato, Brinjal):
- Suck cell sap, transmit viruses
- Yellow sticky traps effective
- Control: Neem oil spray, insecticidal soap
- Spray Thiamethoxam if severe

5. Aphids (Almost all vegetables, cereals):
- Suck plant sap, cause leaf curling
- Transmit viruses
- Control: Strong water spray to dislodge
- Neem spray 5%
- Use yellow sticky traps
- Spray Dimethoate 30 EC if severe

6. Spider Mites (Groundnut, Cotton, Vegetables):
- Cause yellowing and bronzing of leaves
- Appear as fine webbing
- Control: Spray Sulphur 0.5% or Dicofol
- Maintain humidity
- Remove weeds

IPM Approach (Integrated Pest Management):

1. Monitoring:
- Scout fields regularly
- Use pheromone traps for insects
- Monitor disease incidence
- Record pest population

2. Preventive Measures:
- Use resistant varieties
- Proper field sanitation
- Crop rotation
- Suitable spacing
- Timely sowing
- Manage weeds
- Remove crop residue

3. Biological Control:
- Use parasitoids and predators
- NPV (Nuclear Polyhedrosis Virus) for bollworm
- Trichoderma for soil-borne diseases
- Encourage natural predators (ladybugs, lacewing)

4. Chemical Control (Last resort):
- Use registered pesticides
- Follow recommended doses
- Alternate between classes to avoid resistance
- Apply during cool hours
- Protect pollinators
- Follow safety precautions

Common Bio-pesticides:
- Neem oil: Effective against many insects and mites
- SNPV: Against Spodoptera (armyworm)
- NPV: Against Helicoverpa (bollworm)
- Bacillus thuringiensis: Against lepidopteran larvae

Pesticide Safety:
- Wear protective equipment
- Never eat/smoke while spraying
- Store pesticides safely away from children
- Maintain spraying equipment properly
- Follow withdrawal period before harvest
- Dispose of empty containers safely

Pheromone Traps:
- Cost-effective monitoring tool
- Yellow sticky trap catches whiteflies, thrips
- Pheromone traps for moths and beetles
- Trap placement: 1-2 per field

Natural Pest Repellents:
- Neem spray: 5-7 days interval
- Chilli-garlic spray: Economical, effective
- Soap water: For soft-bodied insects
- Lime-sulphur: For mites and scale insects

When to Spray:
- Early morning or late evening
- When insects reach economic threshold
- Spray underside of leaves thoroughly
- Repeat sprays as per instruction""",
            source_name="Directorate of Plant Protection, ICAR",
            source_url="https://pib.icar.gov.in",
            reviewed_date=datetime.utcnow(),
            language="en"
        ),
        KnowledgeDocument(
            title="Soil Health and Fertility Management",
            topic="soil",
            crop=None,
            district=None,
            content="""Good soil health is the foundation of successful and sustainable agriculture.

Understanding Soil:

Soil Types in Karnataka:
1. Black Soil (Clay soil):
- Found in Deccan plateau regions
- High water holding capacity
- Good for cotton, sugarcane, cereals
- Drainage problems in rainy season
- Needs organic matter addition

2. Red Soil:
- Found in Western Ghats, South Karnataka
- Lower water holding capacity
- Good drainage
- Low nitrogen and phosphorus
- Needs more fertilizer input

3. Laterite Soil:
- Found in hilly regions
- Acidic in nature
- Low fertility
- Good for spices, coffee, tea

4. Alluvial Soil:
- Found near river valleys
- Highly fertile
- Good water holding capacity
- Suitable for almost all crops

Soil Testing:

Why Test:
- Know exact nutrient status
- Prevent over/under fertilization
- Reduce cost of inputs
- Increase productivity

When to Test:
- Once in 2 years for normal soils
- Annually for intensive cultivation
- After change in fertilizer program

Nutrients to Check:
- Nitrogen (N), Phosphorus (P), Potassium (K)
- Secondary nutrients: Ca, Mg, S
- Micro-nutrients: Zn, Fe, Mn, Cu, B, Mo
- pH, EC (salinity), Organic matter

Where to Test: Agricultural Extension office in your taluk

Soil pH Levels:
- pH 6.0-6.8: Ideal for most crops
- pH < 6.0: Acidic, apply lime
- pH > 7.5: Alkaline, apply gypsum or sulphur

Organic Matter (Humus):
- Improves water holding capacity
- Enhances microbial activity
- Increases nutrient availability
- Better soil structure

Target: 2.5-3% in cultivated soils
Sources: FYM (Farm Yard Manure), Compost, Green manuring

Improving Soil Health:

1. Add Organic Matter:
- 5-10 tonnes FYM per hectare annually
- Compost from farm waste
- Green manuring (grow legumes, incorporate in soil)

2. Reduce Tillage:
- Minimum/zero tillage preserves structure
- Reduces erosion
- Saves labor and fuel

3. Mulching:
- Conserves moisture
- Regulates temperature
- Reduces weeds
- Reduces erosion

4. Crop Rotation:
- Alternate crops from different families
- Breaks pest/disease cycle
- Nitrogen-fixing legumes restore nitrogen
- Example: Cotton → Pulses → Cereals

5. Intercropping:
- Grow two crops together
- Legumes fix nitrogen
- Improves soil fertility

Nutrient Deficiency Signs:

Nitrogen (N):
- Yellowing of older leaves first
- Stunted growth
- Solution: Apply urea or compost

Phosphorus (P):
- Purple/reddish discoloration
- Poor growth and flowering
- Solution: Apply superphosphate or bone meal

Potassium (K):
- Brown scorching on leaf margins
- Poor fruit quality
- Solution: Apply muriate of potash

Iron (Fe):
- Yellowing between veins while veins stay green
- Solution: Iron sulphate or FeSO4 spray

Zinc (Zn):
- Small leaves, stunted growth
- Solution: Zinc sulphate spray or soil application

Micronutrient Application:
- Zinc: 25 kg/hectare ZnSO4
- Boron: 10 kg/hectare Borax
- Copper: 6-8 kg/hectare CuSO4
- Iron: 25 kg/hectare FeSO4

Best Practices:
1. Test soil regularly
2. Add balanced fertilizer based on test report
3. Use 50% organic + 50% chemical fertilizer
4. Practice crop rotation
5. Add compost/FYM annually
6. Avoid waterlogging
7. Maintain good drainage
8. Monitor crops for deficiency symptoms
9. Use biofertilizers (Azospirillum, Bacillus)""",
            source_name="Soil and Water Conservation Department, Karnataka",
            source_url="https://swcd.karnataka.gov.in",
            reviewed_date=datetime.utcnow(),
            language="en"
        ),
        KnowledgeDocument(
            title="Government Agriculture Schemes for Karnataka Farmers",
            topic="scheme",
            crop=None,
            district=None,
            content="""Karnataka State and Central government offer several schemes to support farmers.

1. PM-KISAN (Pradhan Mantri Kisan Samman Nidhi):

Benefits:
- Rs. 6,000 per year (3 instalments of Rs. 2,000 each)
- Direct transfer to bank account

Eligibility:
- All landholding farmers with land up to 2 hectares
- Exclude high-income farmers

Documents Required:
- Land records (FMB/CMB/RoR)
- Bank account details (linked to Aadhaar where possible)
- Aadhaar card

How to Apply:
- Visit nearest PM-KISAN Common Service Center
- Online: https://pmkisan.gov.in
- Taluk agriculture office

Verification: Land records verified with revenue department

2. Rashtriya Kisan Samman Yojana (Karnataka state scheme):

Benefits: Additional support to farmers in Karnataka

Eligibility: Varies by category

How to Apply: District agriculture office

3. Krishi Marata Vahini (Weather advisory service):

Benefits:
- Free weather forecasts and agriculture advisories
- SMS-based alerts
- Crop-specific guidance

How to Use:
- Register phone number with taluk office
- Free SMS service

4. Raitha Mitra (Farmer helpline):

Benefits:
- Agricultural advice
- Scheme information
- Problem resolution

Hotline: Contact district agriculture office

5. FRUITS (Farm Reforms and Unified Solutions):

Purpose: Digital platform for government agricultural services

Services:
- Scheme application
- Subsidy information
- Loan assistance guidance

How to Use:
- Visit taluk agriculture office
- They can help with FRUITS portal

6. Agricultural Input Schemes:

Subsidy on Seeds:
- 50% subsidy on certified seeds
- Apply through taluk agriculture office

Fertilizer Subsidy:
- Subsidized fertilizers at FPS (Fair Price Shop)
- Priority given to small farmers

Tools and Equipment Subsidy:
- Custom hiring centers
- 50-80% subsidy on implements
- Apply: District Agriculture Technology Management Agency (ATMA)

7. Crop Insurance (Pradhan Mantri Fasal Bima Yojana - PMFBY):

Coverage:
- Protection against crop loss due to natural calamity
- Disease, pest, weather-related losses

Premium:
- Kharif: 2% of insured value
- Rabi: 1.5% of insured value
- Farmer contribution low, Government contribution high

How to Apply:
- During sowing season through bank
- Agricultural credit card holders
- Direct application at insurance office

Claim Process:
- Report loss to taluk office within 48 hours
- Assessment by insurance surveyor
- Claim settlement in 2-4 weeks

8. Soil Health Card Scheme:

Benefits:
- Free soil testing
- Personalized fertilizer recommendations
- Reduce input cost

How to Get:
- Contact taluk agriculture office
- Free testing
- Card issued with recommendations

9. Organic Farming Promotion:

Subsidy:
- Up to 50% subsidy for organic farming certification
- Composting equipment subsidy

Certification:
- Required for premium price
- Take 3-year transition period

How to Apply: District agriculture office

10. Horticulture Promotion:

Subsidies for:
- Fruit plants (50-60% subsidy)
- Vegetable nurseries
- Spice cultivation
- Floriculture

Contact: District Horticulture office

11. Biogas and Renewable Energy:

Subsidy: 50% cost for biogas units, solar pumps

Purpose: Sustainable farming, reduce input cost

Apply: District Agriculture Office / Renewable Energy Department

Common Application Process:

1. Identify eligible scheme
2. Gather required documents (FMB, bank details, ID proof)
3. Visit taluk agriculture office
4. Fill application form
5. Submit with documents
6. Get application receipt
7. Follow up for verification
8. Receive approval and funds

Important Notes:

- Eligibility and benefits change annually
- Check official government website for latest updates
- Always apply through official channels
- Be cautious of fake intermediaries
- Keep copies of all submitted documents
- Schemes vary by district, check your district office
- Some schemes have seasonal applications
- Land records must be updated
- Farm registration often required

Where to Get Information:

1. District Agriculture Office (Main source)
2. Taluk Agriculture Office
3. Gram Panchayat
4. Official government websites:
   - agriculture.karnataka.gov.in
   - pmkisan.gov.in
   - agrimis.nic.in
5. Agriculture Extension Officers

Contact your nearest taluk agriculture office for latest scheme details and application process.""",
            source_name="Department of Agriculture, Government of Karnataka",
            source_url="https://agriculture.karnataka.gov.in",
            reviewed_date=datetime.utcnow(),
            language="en"
        ),
        KnowledgeDocument(
            title="Groundnut (Peanut) Cultivation",
            topic="crop",
            crop="Groundnut",
            district=None,
            content="""Groundnut is an important oil seed and cash crop in Karnataka.

Growing Season: 
- Kharif (June-October) in South Karnataka
- Summer (February-June) in North Karnataka

Suitable Districts: All districts, especially in rainfed regions

Climate Requirements:
- Temperature: 24-28°C ideal
- Rainfall: 50-100 cm
- Well-distributed rainfall important
- Avoid excessive moisture at harvest

Soil Requirements:
- Well-drained sandy loam or loam soil
- pH 5.5 to 7.0
- Good calcium content
- Avoid heavy clay soils

Land Preparation:
- 3-4 ploughings for good tilth
- Remove stones (important!)
- Form ridges and furrows for better drainage

Varieties:
- TMV 2, TMV 7, Chitra (bold seeded)
- AK 12-24 (bunch type)
- VG 30 (Virginia type)

Seed Requirements:
- 80-100 kg/hectare for bunch varieties
- 70-80 kg/hectare for runner varieties
- Use certified seeds
- Treat with carbendazim before sowing

Sowing:
- June-July (Kharif)
- February-March (Summer)
- Spacing: 30 cm x 20 cm (bunch), 45 cm x 20 cm (runner)
- Sow at 5-7 cm depth
- Use seed drill for uniform sowing

Fertilizer:
- 20 kg N (if not inoculated with Rhizobium)
- 40 kg P2O5
- 40 kg K2O per hectare
- Add 5 tonnes FYM/compost

Rhizobium Inoculation:
- Groundnut fixes its own nitrogen
- Inoculate seeds with Rhizobium
- Increases yield by 15-20%

Intercropping:
- Can intercrop with vegetables (radish, turnip, etc.)
- Increases total income

Irrigation:
- Drought tolerant crop, but benefits from irrigation
- 3-4 irrigations in summer
- Keep dry during flowering stage
- Drip irrigation: Rs 2,000/hectare water saving

Weed Management:
- 2-3 hand weedings at 30, 60, 90 days
- Mulching reduces weeds
- Hoeing important at flowering stage

Diseases:
- Leaf spot (rust): Brown spots on leaves
  Control: Spray mancozeb 0.2%, avoid overhead irrigation
- Tikka disease: Similar to leaf spot
  Control: Use resistant varieties, spray fungicide
- Stem rot: Reddish-brown on stem base
  Control: Avoid waterlogging, soil-drenching with Trichoderma

Pests:
- Jassid (leafhopper): Yellowing of leaves
  Control: Neem spray, avoid excess nitrogen
- Thrips: Silvering of leaves
  Control: Yellow sticky traps, neem oil spray
- Stem borer: Wilting of plants
  Control: Crop rotation, destroy infected plants

Calcium Importance:
- Groundnut is calcium-hungry crop
- Calcium deficiency causes hollow heart
- Apply gypsum 400-500 kg/hectare at flowering
- Mix with water and apply to soil

Harvesting:
- 120-160 days after sowing
- Ready when leaves turn yellow
- Dig out plants carefully, allowing pods to mature in soil for 1-2 weeks after digging
- Dry in field for 5-7 days before threshing

Threshing:
- Hand beating or threshing machine
- Ensure complete drying before storage

Yield:
- Bunch varieties: 20-25 quintals/hectare
- Runner varieties: 18-22 quintals/hectare
- Oil content: 45-50%

Post-Harvest:
- Dry to 10% moisture for storage
- Store in cool, dry place
- Use improved storage structures to prevent pest infestation
- Add neem leaves or ash for storage protection

Yield Improvement Tips:
1. Use certified, treated seeds
2. Proper land preparation, remove stones
3. Right spacing for variety
4. Timely operations (weeding, irrigation)
5. Apply gypsum at flowering
6. Protect from pests and diseases
7. Harvest at right maturity
8. Proper drying and storage""",
            source_name="Directorate of Oilseeds, ICAR",
            source_url="https://directorate.icar.gov.in/oilseeds",
            reviewed_date=datetime.utcnow(),
            language="en"
        ),
    ]
    
    # Add to database
    for doc in initial_documents:
        db.add(doc)
    
    db.commit()
    print(f"Seeded {len(initial_documents)} knowledge documents")
