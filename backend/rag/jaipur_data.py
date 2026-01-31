"""
Curated RAG Data for Jaipur
Sources:
- Wikipedia: https://en.wikipedia.org/wiki/List_of_tourist_attractions_in_Jaipur
- Rajasthan Tourism: https://www.tourism.rajasthan.gov.in/jaipur.html
- Incredible India: https://www.incredibleindia.gov.in/en/rajasthan/jaipur
- TripAdvisor: https://www.tripadvisor.in/Attractions-g304555-Activities-Jaipur
- MakeMyTrip: https://www.makemytrip.com/tripideas/places-to-visit-in-jaipur
"""

JAIPUR_RAG_DATA = [
    # ========== PALACES AND FORTS ==========
    {
        "text": """Amer Fort (Amber Fort) is a magnificent fort located in Amer, about 11 km from Jaipur. Built in red sandstone and marble, it is known for its artistic Hindu style elements. The fort overlooks Maota Lake and is a UNESCO World Heritage Site as part of the Hill Forts of Rajasthan. Key attractions include the Diwan-i-Aam (Hall of Public Audience), Diwan-i-Khas (Hall of Private Audience), Sheesh Mahal (Mirror Palace), and Sukh Niwas. The fort is accessible by foot, car, or elephant ride. Best visited in the morning to avoid crowds. Entry fee applies. Allow 2-3 hours for a complete visit.""",
        "metadata": {
            "city": "Jaipur",
            "poi_name": "Amer Fort",
            "category": "historic",
            "section": "see",
            "source": "wikipedia",
            "url": "https://en.wikipedia.org/wiki/List_of_tourist_attractions_in_Jaipur",
            "duration_minutes": 180,
            "entry_fee": "Yes",
            "best_time": "Morning"
        },
        "id": "jaipur_amer_fort"
    },
    {
        "text": """Hawa Mahal (Palace of Winds) is Jaipur's most iconic landmark, built in 1799 by Maharaja Sawai Pratap Singh. This five-story pink sandstone structure has 953 small windows (jharokhas) decorated with intricate latticework. It was designed to allow royal women to observe street life without being seen. The unique honeycomb-like facade allows cool air to pass through, acting as a natural air conditioner. Located in the heart of the old city on Badi Chaupar. Best photographed from the street in morning light. Entry fee is nominal. Allow 30-60 minutes for visit.""",
        "metadata": {
            "city": "Jaipur",
            "poi_name": "Hawa Mahal",
            "category": "historic",
            "section": "see",
            "source": "wikipedia",
            "url": "https://en.wikipedia.org/wiki/List_of_tourist_attractions_in_Jaipur",
            "duration_minutes": 60,
            "entry_fee": "Yes",
            "best_time": "Morning"
        },
        "id": "jaipur_hawa_mahal"
    },
    {
        "text": """City Palace is a stunning palace complex in the heart of Jaipur, built by Maharaja Sawai Jai Singh II. It is a blend of Rajasthani and Mughal architecture. The palace complex includes the Chandra Mahal and Mubarak Mahal, courtyards, gardens, and buildings. The Chandra Mahal is still a royal residence. The palace houses a museum with royal costumes, armory, art, and manuscripts. Key attractions include the Peacock Gate, the huge silver urns (Guinness World Record), and Pritam Niwas Chowk with its four decorated doorways. Allow 2-3 hours for a complete visit.""",
        "metadata": {
            "city": "Jaipur",
            "poi_name": "City Palace",
            "category": "historic",
            "section": "see",
            "source": "wikipedia",
            "url": "https://en.wikipedia.org/wiki/List_of_tourist_attractions_in_Jaipur",
            "duration_minutes": 120,
            "entry_fee": "Yes",
            "best_time": "Morning or late afternoon"
        },
        "id": "jaipur_city_palace"
    },
    {
        "text": """Nahargarh Fort stands on the edge of the Aravalli Hills, overlooking Jaipur city. Built in 1734 by Maharaja Sawai Jai Singh II, it was originally named Sudarshangarh but later renamed Nahargarh (abode of tigers). The fort offers stunning panoramic views of the city, especially at sunset. It houses the Madhavendra Bhawan, a palace with interconnected suites for the king and his 12 queens. The fort is connected to Jaigarh Fort by fortified walls. Popular for evening visits and has a cafe with city views. Allow 1.5-2 hours for visit.""",
        "metadata": {
            "city": "Jaipur",
            "poi_name": "Nahargarh Fort",
            "category": "historic",
            "section": "see",
            "source": "wikipedia",
            "url": "https://en.wikipedia.org/wiki/List_of_tourist_attractions_in_Jaipur",
            "duration_minutes": 120,
            "entry_fee": "Yes",
            "best_time": "Sunset"
        },
        "id": "jaipur_nahargarh_fort"
    },
    {
        "text": """Jaigarh Fort is located on the promontory called Cheel ka Teela (Hill of Eagles) of the Aravalli range, overlooking the Amer Fort and Maota Lake. Built by Jai Singh II in 1726, it was primarily a military structure to protect Amer Fort. The fort houses the world's largest cannon on wheels - Jaivana. It has a well-preserved structure with armory, museum, granary, and the royal treasury. Connected to Amer Fort through underground passages. The fort offers excellent views and relatively fewer crowds. Allow 1.5-2 hours for visit.""",
        "metadata": {
            "city": "Jaipur",
            "poi_name": "Jaigarh Fort",
            "category": "historic",
            "section": "see",
            "source": "wikipedia",
            "url": "https://en.wikipedia.org/wiki/List_of_tourist_attractions_in_Jaipur",
            "duration_minutes": 120,
            "entry_fee": "Yes",
            "best_time": "Morning"
        },
        "id": "jaipur_jaigarh_fort"
    },
    {
        "text": """Jal Mahal (Water Palace) is a palace located in the middle of Man Sagar Lake. Built in red sandstone, the five-story structure has four floors submerged when the lake is full. Built by Maharaja Sawai Pratap Singh, it was used as a summer retreat and duck hunting lodge. The palace has been restored and features a Mughal-style rooftop garden. Visitors can only view the palace from the shore as entry is restricted. The lake attracts many migratory birds. Best viewed at sunset when the palace is illuminated. Allow 30 minutes for viewing.""",
        "metadata": {
            "city": "Jaipur",
            "poi_name": "Jal Mahal",
            "category": "historic",
            "section": "see",
            "source": "wikipedia",
            "url": "https://en.wikipedia.org/wiki/List_of_tourist_attractions_in_Jaipur",
            "duration_minutes": 30,
            "entry_fee": "No (external viewing only)",
            "best_time": "Sunset"
        },
        "id": "jaipur_jal_mahal"
    },
    {
        "text": """Rambagh Palace was built in 1835 as a garden house for the queen's handmaid and later became the residence of Maharaja Sawai Man Singh II. Now converted into a luxury heritage hotel by Taj Hotels, it offers a glimpse into royal living. The palace features Mughal Gardens, marble corridors, hand-carved lattice screens, and exquisite interiors. Non-guests can enjoy high tea or dinner at the restaurants. The palace grounds are beautifully maintained with peacocks roaming freely.""",
        "metadata": {
            "city": "Jaipur",
            "poi_name": "Rambagh Palace",
            "category": "historic",
            "section": "see",
            "source": "wikipedia",
            "url": "https://en.wikipedia.org/wiki/List_of_tourist_attractions_in_Jaipur",
            "duration_minutes": 60,
            "entry_fee": "Restaurant reservations recommended",
            "best_time": "Evening for high tea"
        },
        "id": "jaipur_rambagh_palace"
    },
    
    # ========== MUSEUMS ==========
    {
        "text": """Albert Hall Museum is the oldest museum in Rajasthan, located in Ram Niwas Garden. Built in Indo-Saracenic style, it was designed by Sir Samuel Swinton Jacob. The museum houses a rich collection of artifacts including paintings, carpets, ivory, metal sculptures, and an Egyptian mummy. The building itself is a work of art with intricate carvings and beautiful architecture. The museum is illuminated at night, offering a spectacular view. Entry fee applies. Allow 1.5-2 hours for visit. Closed on Fridays.""",
        "metadata": {
            "city": "Jaipur",
            "poi_name": "Albert Hall Museum",
            "category": "museum",
            "section": "see",
            "source": "wikipedia",
            "url": "https://en.wikipedia.org/wiki/List_of_tourist_attractions_in_Jaipur",
            "duration_minutes": 90,
            "entry_fee": "Yes",
            "best_time": "Afternoon or evening for illumination"
        },
        "id": "jaipur_albert_hall"
    },
    {
        "text": """Jantar Mantar is an astronomical observation site built in 1734 by Maharaja Sawai Jai Singh II. It is a UNESCO World Heritage Site and features the world's largest stone sundial (Samrat Yantra). The collection of 19 astronomical instruments allows the observation of celestial positions with the naked eye. The instruments were used for measuring time, predicting eclipses, tracking stars, and determining celestial altitudes. Guided tours are highly recommended to understand the instruments. Entry fee applies. Allow 1-1.5 hours for visit.""",
        "metadata": {
            "city": "Jaipur",
            "poi_name": "Jantar Mantar",
            "category": "historic",
            "section": "see",
            "source": "wikipedia",
            "url": "https://en.wikipedia.org/wiki/List_of_tourist_attractions_in_Jaipur",
            "duration_minutes": 60,
            "entry_fee": "Yes",
            "best_time": "Morning for accurate sundial readings"
        },
        "id": "jaipur_jantar_mantar"
    },
    
    # ========== TEMPLES ==========
    {
        "text": """Birla Mandir (Lakshmi Narayan Temple) is a Hindu temple made entirely of white marble, located at the base of Moti Dungri hill. Built by the Birla family in 1988, it is dedicated to Lord Vishnu and Goddess Lakshmi. The temple features intricate carvings, stained glass windows, and mythological scenes. The temple welcomes people of all faiths and has quotes from various religious texts inscribed on its walls. Best visited in the evening when illuminated. No entry fee but footwear must be removed.""",
        "metadata": {
            "city": "Jaipur",
            "poi_name": "Birla Mandir",
            "category": "temple",
            "section": "see",
            "source": "wikipedia",
            "url": "https://en.wikipedia.org/wiki/List_of_tourist_attractions_in_Jaipur",
            "duration_minutes": 45,
            "entry_fee": "No",
            "best_time": "Evening"
        },
        "id": "jaipur_birla_mandir"
    },
    {
        "text": """Galtaji Temple (Monkey Temple) is an ancient Hindu pilgrimage site located in a mountain pass about 10 km from Jaipur. The temple complex includes natural fresh water springs, pavilions, and temples built into the hillside. The site is known for the large population of monkeys living there. The temple has seven sacred kunds (water tanks) where pilgrims take holy dips. The Galta Kund is believed to never dry up. The architecture features pink sandstone with painted walls. Allow 1.5-2 hours including travel time.""",
        "metadata": {
            "city": "Jaipur",
            "poi_name": "Galtaji Temple",
            "category": "temple",
            "section": "see",
            "source": "wikipedia",
            "url": "https://en.wikipedia.org/wiki/List_of_tourist_attractions_in_Jaipur",
            "duration_minutes": 90,
            "entry_fee": "Nominal",
            "best_time": "Morning"
        },
        "id": "jaipur_galtaji"
    },
    {
        "text": """Govind Dev Ji Temple is one of the most famous temples in Jaipur, dedicated to Lord Krishna. Located within the City Palace complex, it houses the deity originally worshipped in Vrindavan. The temple sees huge crowds during Janmashtami and other Krishna festivals. The temple follows a unique schedule with seven darshans (viewings) per day. The deity is dressed in different attire for each darshan. The temple's music and bhajans create a spiritual atmosphere.""",
        "metadata": {
            "city": "Jaipur",
            "poi_name": "Govind Dev Ji Temple",
            "category": "temple",
            "section": "see",
            "source": "wikipedia",
            "url": "https://en.wikipedia.org/wiki/List_of_tourist_attractions_in_Jaipur",
            "duration_minutes": 45,
            "entry_fee": "No",
            "best_time": "During darshan timings"
        },
        "id": "jaipur_govind_devji"
    },
    
    # ========== GARDENS AND PARKS ==========
    {
        "text": """Central Park Jaipur is a large public park located in the heart of the city, spread over 250 acres. It features a jogging track, open-air gym, and the tallest national flag in Rajasthan. The park has beautiful landscaped gardens, fountains, and is illuminated at night. It's a popular spot for morning and evening walks. The park also has a musical fountain show. Entry is free. Best visited in the morning for exercise or evening for walks.""",
        "metadata": {
            "city": "Jaipur",
            "poi_name": "Central Park",
            "category": "garden",
            "section": "do",
            "source": "rajasthan_tourism",
            "url": "https://www.tourism.rajasthan.gov.in/jaipur.html",
            "duration_minutes": 60,
            "entry_fee": "No",
            "best_time": "Morning or evening"
        },
        "id": "jaipur_central_park"
    },
    {
        "text": """Ram Niwas Garden is a historic garden built by Maharaja Sawai Ram Singh II in 1868. It houses the Albert Hall Museum, a zoo, a bird park, a greenhouse, and a modern art gallery. The garden is a green oasis in the city with walking paths and seating areas. The zoo has a variety of animals including lions, tigers, and crocodiles. The garden is popular with locals for morning walks. Entry fee for zoo. Allow 2-3 hours to explore completely.""",
        "metadata": {
            "city": "Jaipur",
            "poi_name": "Ram Niwas Garden",
            "category": "garden",
            "section": "do",
            "source": "wikipedia",
            "url": "https://en.wikipedia.org/wiki/List_of_tourist_attractions_in_Jaipur",
            "duration_minutes": 120,
            "entry_fee": "Free (Zoo has entry fee)",
            "best_time": "Morning"
        },
        "id": "jaipur_ram_niwas"
    },
    {
        "text": """Sisodia Rani Garden is a beautiful terraced garden located 8 km from Jaipur on the Agra road. Built in 1728 by Maharaja Sawai Jai Singh II for his queen from the Sisodia clan of Udaipur, it features fountains, water channels, painted pavilions, and murals depicting scenes from the love story of Radha-Krishna. The garden is built in the Mughal style with multiple levels. It's less crowded than other attractions and offers a peaceful escape. Allow 1-1.5 hours including travel time.""",
        "metadata": {
            "city": "Jaipur",
            "poi_name": "Sisodia Rani Garden",
            "category": "garden",
            "section": "see",
            "source": "wikipedia",
            "url": "https://en.wikipedia.org/wiki/List_of_tourist_attractions_in_Jaipur",
            "duration_minutes": 60,
            "entry_fee": "Yes",
            "best_time": "Morning"
        },
        "id": "jaipur_sisodia_rani"
    },
    
    # ========== SHOPPING ==========
    {
        "text": """Johari Bazaar is the jewelry market of Jaipur, famous for its precious and semi-precious stones, gold, and silver jewelry. The bazaar is known for kundan and meenakari (enamel work) jewelry that Jaipur is famous for. The shops also sell traditional Rajasthani textiles, bandhani (tie-dye), and handicrafts. Bargaining is expected and recommended. The bazaar is located in the old walled city near Hawa Mahal. Best visited in late afternoon when shops are fully operational. Allow 2-3 hours for shopping.""",
        "metadata": {
            "city": "Jaipur",
            "poi_name": "Johari Bazaar",
            "category": "shopping",
            "section": "buy",
            "source": "tripadvisor",
            "url": "https://www.tripadvisor.in/Attractions-g304555-Activities-Jaipur",
            "duration_minutes": 120,
            "entry_fee": "No",
            "best_time": "Late afternoon to evening"
        },
        "id": "jaipur_johari_bazaar"
    },
    {
        "text": """Bapu Bazaar is one of the busiest markets in Jaipur, known for textiles, mojaris (traditional footwear), perfumes, and handicrafts. The street stretches from Sanganeri Gate to New Gate. It's famous for colorful Jaipuri quilts (razai), bed sheets, and cotton fabrics. The market also has leather goods, camel-leather items, and traditional Rajasthani items. Prices are more reasonable than tourist-oriented shops. Bargaining is essential. Best visited in the afternoon.""",
        "metadata": {
            "city": "Jaipur",
            "poi_name": "Bapu Bazaar",
            "category": "shopping",
            "section": "buy",
            "source": "makemytrip",
            "url": "https://www.makemytrip.com/tripideas/places-to-visit-in-jaipur",
            "duration_minutes": 90,
            "entry_fee": "No",
            "best_time": "Afternoon"
        },
        "id": "jaipur_bapu_bazaar"
    },
    {
        "text": """Tripolia Bazaar is famous for lac bangles, brass utensils, and traditional items. Located between Tripolia Gate and Choti Chaupar, it's one of the oldest markets in the walled city. The market is known for its colorful lac bangles in various designs. You can watch artisans making bangles in their workshops. The bazaar also sells brass and copperware, textiles, and traditional items. Less touristy than other markets. Allow 1-2 hours for exploration.""",
        "metadata": {
            "city": "Jaipur",
            "poi_name": "Tripolia Bazaar",
            "category": "shopping",
            "section": "buy",
            "source": "incredible_india",
            "url": "https://www.incredibleindia.gov.in/en/rajasthan/jaipur",
            "duration_minutes": 90,
            "entry_fee": "No",
            "best_time": "Afternoon"
        },
        "id": "jaipur_tripolia_bazaar"
    },
    
    # ========== FOOD ==========
    {
        "text": """Jaipur is famous for its rich Rajasthani cuisine. Must-try dishes include Dal Baati Churma (baked wheat balls with lentils), Laal Maas (spicy red meat curry), Gatte ki Sabzi (gram flour dumplings in gravy), and Ker Sangri (desert beans and berries). For street food, try pyaaz kachori (onion-filled pastry), mirchi bada (stuffed chili fritters), and ghewar (sweet disc-shaped dessert). Famous spots include LMB (Laxmi Mishthan Bhandar) in Johari Bazaar for sweets and snacks, Rawat Mishthan Bhandar for pyaaz kachori, and Chokhi Dhani for authentic Rajasthani village dining experience.""",
        "metadata": {
            "city": "Jaipur",
            "poi_name": "Jaipur Food Guide",
            "category": "food",
            "section": "eat",
            "source": "tripadvisor",
            "url": "https://www.tripadvisor.in/Attractions-g304555-Activities-Jaipur",
            "duration_minutes": 90,
            "entry_fee": "Varies",
            "best_time": "Lunch or dinner"
        },
        "id": "jaipur_food_guide"
    },
    {
        "text": """Chokhi Dhani is an ethnic village resort located about 20 km from Jaipur. It offers an authentic Rajasthani village experience with traditional food, folk dances, puppet shows, and cultural activities. The complex recreates a traditional Rajasthani village with mud houses, handicraft shops, and various entertainment options. The traditional thali dinner includes Dal Baati Churma, Gatte ki Sabzi, and many local delicacies. Best visited in the evening for the complete cultural experience. Entry includes dinner. Allow 3-4 hours for visit.""",
        "metadata": {
            "city": "Jaipur",
            "poi_name": "Chokhi Dhani",
            "category": "food",
            "section": "eat",
            "source": "makemytrip",
            "url": "https://www.makemytrip.com/tripideas/places-to-visit-in-jaipur",
            "duration_minutes": 180,
            "entry_fee": "Yes (includes dinner)",
            "best_time": "Evening"
        },
        "id": "jaipur_chokhi_dhani"
    },
    
    # ========== PRACTICAL INFO ==========
    {
        "text": """Jaipur, known as the Pink City, is the capital of Rajasthan and was founded in 1727 by Maharaja Sawai Jai Singh II. It was the first planned city of India. The city gets its name from the terracotta pink color of its buildings, painted in 1876 to welcome Prince Albert. Best time to visit is October to March when the weather is pleasant (15-25°C). Summers (April-June) are extremely hot (35-45°C). Monsoon (July-September) brings moderate rainfall. The city is well-connected by air (Jaipur International Airport), rail (Jaipur Junction), and road. Auto-rickshaws, cabs, and metro are available for local transport.""",
        "metadata": {
            "city": "Jaipur",
            "poi_name": "Jaipur Overview",
            "category": "general",
            "section": "understand",
            "source": "rajasthan_tourism",
            "url": "https://www.tourism.rajasthan.gov.in/jaipur.html",
            "duration_minutes": 0,
            "entry_fee": "N/A",
            "best_time": "October to March"
        },
        "id": "jaipur_overview"
    },
    {
        "text": """Getting around Jaipur: The city is compact and most attractions in the old city can be covered on foot. For longer distances, auto-rickshaws (always negotiate fare beforehand or insist on meter), Ola/Uber cabs, and the Jaipur Metro (Pink Line) are available. Full-day taxi hire costs around ₹1500-2500. The walled city (old city) has narrow lanes best explored on foot. Most forts are on the outskirts and require hired transport. Elephant rides at Amer Fort are available but controversial - consider jeep rides instead. E-rickshaws are available in the old city.""",
        "metadata": {
            "city": "Jaipur",
            "poi_name": "Getting Around",
            "category": "general",
            "section": "get_around",
            "source": "rajasthan_tourism",
            "url": "https://www.tourism.rajasthan.gov.in/jaipur.html",
            "duration_minutes": 0,
            "entry_fee": "N/A",
            "best_time": "N/A"
        },
        "id": "jaipur_transport"
    },
    {
        "text": """Safety tips for Jaipur: The city is generally safe for tourists but take normal precautions. Beware of gem scams - don't buy from touts or unverified shops. Bargain hard in markets - initial prices are often inflated 3-4x. Avoid eating from unhygienic street stalls. Carry water bottles as it gets very hot. Dress modestly when visiting temples. Keep valuables secure in crowded markets. Use prepaid taxis from the airport/station. The tourist police helpline is 1363. Medical facilities are good with several private hospitals available.""",
        "metadata": {
            "city": "Jaipur",
            "poi_name": "Safety Tips",
            "category": "general",
            "section": "stay_safe",
            "source": "incredible_india",
            "url": "https://www.incredibleindia.gov.in/en/rajasthan/jaipur",
            "duration_minutes": 0,
            "entry_fee": "N/A",
            "best_time": "N/A"
        },
        "id": "jaipur_safety"
    },
    {
        "text": """Weather and when to visit Jaipur: Best time is October to March (15-25°C). Summers (April-June) are extremely hot (35-45°C). Monsoon (July-September) brings moderate rainfall; showers are usually short and afternoon thunderstorms are common. If it rains, indoor options include Albert Hall Museum, City Palace museum, Jantar Mantar (partially covered), Birla Mandir, and shopping at Johari Bazaar or Bapu Bazaar. Carry an umbrella and light rain gear in monsoon.""",
        "metadata": {
            "city": "Jaipur",
            "poi_name": "Weather and Best Time",
            "category": "general",
            "section": "understand",
            "source": "rajasthan_tourism",
            "url": "https://www.tourism.rajasthan.gov.in/jaipur.html",
            "duration_minutes": 0,
            "entry_fee": "N/A",
            "best_time": "October to March"
        },
        "id": "jaipur_weather_best_time"
    },
    {
        "text": """What if it rains in Jaipur: Monsoon brings short, heavy showers. Best rainy-day options: Albert Hall Museum (fully indoor, Indo-Saracenic architecture and artifacts), City Palace (indoor museums and courtyards), Birla Mandir (covered temple), Jantar Mantar (some instruments under cover), and covered markets like Johari Bazaar and Bapu Bazaar. Forts like Amer and Nahargarh have covered areas but paths can get slippery. Avoid Galtaji (outdoor) and Jal Mahal viewing in heavy rain. Carry umbrella; many attractions remain open.""",
        "metadata": {
            "city": "Jaipur",
            "poi_name": "Rainy Day Options",
            "category": "general",
            "section": "see",
            "source": "incredible_india",
            "url": "https://www.incredibleindia.gov.in/en/rajasthan/jaipur",
            "duration_minutes": 0,
            "entry_fee": "Varies",
            "best_time": "Monsoon backup"
        },
        "id": "jaipur_rainy_day"
    },
    {
        "text": """Indoor activities in Jaipur: Albert Hall Museum (full indoor), City Palace (museums and galleries), Jantar Mantar (partially covered), Birla Mandir (temple), Govind Dev Ji Temple, shopping at Johari Bazaar and Bapu Bazaar (covered lanes), and heritage hotels like Rambagh Palace for high tea. These are good backups for hot afternoons or rainy days.""",
        "metadata": {
            "city": "Jaipur",
            "poi_name": "Indoor Activities",
            "category": "general",
            "section": "do",
            "source": "tripadvisor",
            "url": "https://www.tripadvisor.in/Attractions-g304555-Activities-Jaipur",
            "duration_minutes": 0,
            "entry_fee": "Varies",
            "best_time": "Hot or rainy days"
        },
        "id": "jaipur_indoor"
    },
    {
        "text": """Is a multi-day Jaipur plan doable: Yes. A 2–3 day plan is realistic. The city is compact; old city attractions (City Palace, Jantar Mantar, Hawa Mahal, markets) can be covered on foot or short rides. Forts (Amer, Jaigarh, Nahargarh) are on the outskirts; allow 30–45 min travel each way. Suggested pacing: 2–3 major sights per day with travel time (e.g. 120 min max travel per day). Full-day taxi (₹1500–2500) makes fort loops efficient. Pace depends on your preference: relaxed (fewer POIs, more breaks) or packed (more sights, less downtime).""",
        "metadata": {
            "city": "Jaipur",
            "poi_name": "Plan Feasibility",
            "category": "general",
            "section": "get_around",
            "source": "rajasthan_tourism",
            "url": "https://www.tourism.rajasthan.gov.in/jaipur.html",
            "duration_minutes": 0,
            "entry_fee": "N/A",
            "best_time": "N/A"
        },
        "id": "jaipur_plan_doable"
    },
    {
        "text": """Suggested 3-day Jaipur itinerary: Day 1 - Start early with Amer Fort (3 hours), then Jaigarh Fort (1.5 hours), lunch at LMB restaurant, afternoon at City Palace and Jantar Mantar (2.5 hours), evening at Hawa Mahal and Johari Bazaar. Day 2 - Morning at Nahargarh Fort for views, visit Albert Hall Museum, lunch break, afternoon at Birla Mandir and Galtaji Temple, evening at Chokhi Dhani for dinner and cultural show. Day 3 - Explore Bapu Bazaar and local markets, visit Jal Mahal for photos, relax at Central Park, departure or extend trip.""",
        "metadata": {
            "city": "Jaipur",
            "poi_name": "3-Day Itinerary",
            "category": "general",
            "section": "itinerary",
            "source": "makemytrip",
            "url": "https://www.makemytrip.com/tripideas/places-to-visit-in-jaipur",
            "duration_minutes": 0,
            "entry_fee": "N/A",
            "best_time": "N/A"
        },
        "id": "jaipur_3day_itinerary"
    }
]

# List of all POIs with basic info for quick reference
JAIPUR_POIS = [
    {"name": "Amer Fort", "category": "historic", "duration": 180, "must_see": True},
    {"name": "Hawa Mahal", "category": "historic", "duration": 60, "must_see": True},
    {"name": "City Palace", "category": "historic", "duration": 120, "must_see": True},
    {"name": "Nahargarh Fort", "category": "historic", "duration": 120, "must_see": True},
    {"name": "Jaigarh Fort", "category": "historic", "duration": 120, "must_see": False},
    {"name": "Jal Mahal", "category": "historic", "duration": 30, "must_see": True},
    {"name": "Jantar Mantar", "category": "historic", "duration": 60, "must_see": True},
    {"name": "Albert Hall Museum", "category": "museum", "duration": 90, "must_see": False},
    {"name": "Birla Mandir", "category": "temple", "duration": 45, "must_see": False},
    {"name": "Galtaji Temple", "category": "temple", "duration": 90, "must_see": False},
    {"name": "Govind Dev Ji Temple", "category": "temple", "duration": 45, "must_see": False},
    {"name": "Central Park", "category": "garden", "duration": 60, "must_see": False},
    {"name": "Ram Niwas Garden", "category": "garden", "duration": 120, "must_see": False},
    {"name": "Sisodia Rani Garden", "category": "garden", "duration": 60, "must_see": False},
    {"name": "Johari Bazaar", "category": "shopping", "duration": 120, "must_see": True},
    {"name": "Bapu Bazaar", "category": "shopping", "duration": 90, "must_see": False},
    {"name": "Tripolia Bazaar", "category": "shopping", "duration": 90, "must_see": False},
    {"name": "Chokhi Dhani", "category": "food", "duration": 180, "must_see": True},
    {"name": "Rambagh Palace", "category": "historic", "duration": 60, "must_see": False},
]

# Festivals
JAIPUR_FESTIVALS = [
    {
        "name": "Elephant Festival",
        "time": "March (during Holi)",
        "description": "Colorful festival featuring decorated elephants, performances, and processions at Chaugan Stadium."
    },
    {
        "name": "Gangaur",
        "time": "March-April",
        "description": "Women's festival dedicated to Goddess Gauri (Parvati), featuring processions with decorated idols."
    },
    {
        "name": "Teej",
        "time": "July-August",
        "description": "Monsoon festival celebrating the union of Shiva and Parvati with swings, songs, and processions."
    },
    {
        "name": "Jaipur Literature Festival",
        "time": "January",
        "description": "World's largest free literary festival held at Diggi Palace with authors from around the world."
    }
]
