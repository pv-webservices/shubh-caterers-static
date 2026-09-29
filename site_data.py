"""Content for the Shubh Caterers website. Edit here, then run `python generate.py`."""

BUSINESS = {
    'name': 'Shubh Caterers',
    'phones': [('Pawan Agarwal', '9595956709'), ('Ajay Agarwal', '9822323230')],
    'whatsapp': '919595956709',
    'email': 'shubhcaterers009@gmail.com',
    'address_lines': ['Tirupati Garden, Hall No. 2,', 'Tingre Nagar, Aadarsh Colony,', 'Pune - 411015, Maharashtra'],
    'address_short': 'Tirupati Garden, Hall No. 2, Tingre Nagar, Aadarsh Colony, Pune - 411015',
    'map_query': 'Tirupati Garden, Tingre Nagar, Pune 411015',
    'domain': 'https://shubhcaterers.example',
}

# slug, title, short label, icon, image, summary, intro, suitable for, highlights, featured menu picks
SERVICES = [
    ('wedding-catering', 'Wedding Catering', 'Weddings', 'rings', 'hero-buffet',
     'Grand pure-vegetarian wedding feasts, from the welcome drink to the last spoon of rabdi.',
     'Wedding menus are planned around the flow of your celebration, your guest profile, the venue and family traditions. We bring variety, beautiful presentation, graceful service and a warm dining experience your guests will talk about long after the pheras.',
     ['Engagement & Sagai', 'Haldi & Mehendi', 'Wedding Ceremonies', 'Reception Dinners'],
     ['Multi-cuisine vegetarian menus', 'Illuminated live counters', 'Mithai & rabdi stations', 'Buffet or table service'],
     ['Paneer Tikka', 'Dal Makhani', 'Veg Biryani', 'Butter Naan', 'Kesar Rabdi', 'Pani Puri']),
    ('cocktail-events', 'Cocktail & Mocktail Evenings', 'Cocktails', 'glass', 'menu-drinks',
     'Elegant veg small plates, mocktails and live counters for sangeet nights and social evenings.',
     'Cocktail-format evenings need food guests can enjoy while they mingle. We pair passed vegetarian appetisers and live counters with a colourful mocktail, mastani and shake bar — all zero-proof and made fresh.',
     ['Sangeet Nights', 'Engagement Parties', 'Social Evenings', 'Corporate Mixers'],
     ['Passed veg appetisers', 'Mocktail & mastani bar', 'Live chaat & grill counters', 'Dessert bites'],
     ['Cheese Ball', 'Chilli Paneer', 'Mango Mastani', 'Kiwi Juice', 'Corn Tikka', 'Spring Roll']),
    ('corporate-catering', 'Corporate Catering', 'Corporates', 'briefcase', 'svc-corporate',
     'Punctual, professional vegetarian catering for meetings, conferences, launches and office celebrations.',
     'Corporate catering is planned around your schedule, service speed and a menu that works for a mixed group. From breakfast and high-tea to polished buffet lunches, we keep it on time, hygienic and hassle-free.',
     ['Meetings & Conferences', 'Office Celebrations', 'Product Launches', 'Training Programs'],
     ['Breakfast & high-tea', 'Buffet lunches', 'Tea & coffee service', 'Custom event menus'],
     ['Poha', 'Veg Sandwich', 'Paneer Butter Masala', 'Jeera Rice', 'Fulka Roti', 'Gulab Jamun']),
    ('theme-party', 'Theme Parties', 'Theme Party', 'confetti', 'about-counter',
     'Menus, counters and presentation styled to match your chosen celebration theme.',
     'Theme-party catering connects food, décor and service with the mood of your event. Food stations, counters and dessert displays are styled to match your theme — Rajasthani, street-food, festive or modern.',
     ['Festive Events', 'Milestone Parties', 'Family Celebrations', 'Concept Events'],
     ['Theme-aligned menus', 'Styled food stations', 'Illuminated live counters', 'Custom dessert displays'],
     ['Dal Bati Churma', 'Kacchi Dabeli', 'Pav Bhaji', 'Momos', 'Barf Gola', 'Jalebi']),
    ('private-party', 'Private Parties', 'Private Party', 'cheers', 'hero-feast',
     'Flexible vegetarian catering for intimate get-togethers, anniversaries and home celebrations.',
     'Private events deserve a compact menu with great variety and attentive service. We plan the format around your guest count, your space and the pace of your gathering.',
     ['Family Dinners', 'Anniversaries', 'Home Gatherings', 'Kitty Parties'],
     ['Customised menus', 'Compact buffet setups', 'Live counter options', 'Dessert & beverage stations'],
     ['Hara Shahi Kabab', 'Malai Kofta', 'Kashmiri Pulao', 'Laccha Paratha', 'Rasmalai Rabdi', 'Mango Shake']),
    ('niche-events', 'Niche Events', 'Niche Events', 'star', 'menu-chaat',
     'Custom catering for unusual formats, curated experiences and special-purpose events.',
     'Some events don’t fit a template. For niche formats, we adapt the menu, equipment, service pattern and presentation to the actual venue and the experience you want to create.',
     ['Curated Gatherings', 'Community Events', 'Pop-up Formats', 'Religious Functions'],
     ['Flexible planning', 'Custom service format', 'Any cuisine, all vegetarian', 'Event-specific presentation'],
     ['Misal Pav', 'Puran Puri', 'Masala Dosa', 'Papadi Chaat', 'Falooda', 'Paan Stall']),
    ('institutional-catering', 'Institutional Catering', 'Institutional Catering', 'institution', 'menu-south',
     'Consistent, hygienic vegetarian meal service for institutions, hostels and organisations.',
     'Institutional catering calls for consistency, hygiene, practical planning and dependable systems. Balanced vegetarian menus are structured around your schedule, head-count and nutritional needs.',
     ['Schools & Colleges', 'Hostels', 'Organisations', 'Group Meal Service'],
     ['Planned meal cycles', 'Hygienic preparation', 'Balanced vegetarian menus', 'Scalable service'],
     ['Idli Sambar', 'Upma', 'Dal Tadka', 'Mix Veg', 'Chapati', 'Plain Rice']),
    ('birthday-party', 'Birthday Parties', 'Birthday Party', 'cake', 'svc-birthday',
     'Fun, festive vegetarian menus for kids, adults and milestone birthdays.',
     'Birthday catering can be playful, casual or premium. We design menus with crowd favourites, snacks, live counters, desserts and beverages that keep kids and grown-ups equally happy.',
     ['Kids Birthdays', 'Adult Birthdays', 'Milestone Birthdays', 'Home & Venue Parties'],
     ['Party-friendly snacks', 'Pizza, burger & momo stalls', 'Dessert tables', 'Mocktails & shakes'],
     ['Bread Pizza', 'French Fries', 'Cheese Ball', 'Ice Cream', 'Strawberry Shake', 'Chocolate Barfi']),
    ('house-warming', 'House Warming & Pooja', 'House Warming', 'home', 'svc-traditional',
     'Traditional vegetarian catering for griha pravesh, satyanarayan pooja and new-home celebrations.',
     'House-warming menus are planned around ceremony timings, family traditions and the serving space available. From a traditional pangat on banana leaves to a modern buffet, we serve with care.',
     ['Griha Pravesh', 'Satyanarayan Pooja', 'Family Lunch', 'Vastu Shanti'],
     ['Traditional Maharashtrian thali', 'Banana-leaf pangat service', 'Compact service setup', 'Prasad & sweets'],
     ['Puran Puri', 'Varan', 'Masale Bhaat', 'Aloo Bhaji', 'Basundi Rabdi', 'Kothimbir Vadi']),
    ('parcels', 'Parcel Orders', 'Parcels', 'parcel', 'menu-indian',
     'Freshly prepared vegetarian food parcels for family functions, group meals and offices.',
     'Parcel orders are perfect when you want Shubh Caterers’ taste without a full on-site setup. Menu combinations and hygienic packaging are planned to suit your group size and occasion.',
     ['Family Functions', 'Group Meals', 'Office Orders', 'Small Celebrations'],
     ['Veg meal boxes', 'Bulk parcel orders', 'Menu customisation', 'Hygienic packaging'],
     ['Paneer Masala', 'Veg Pulao', 'Dal Fry', 'Puri', 'Gulab Jamun', 'Veg Cutlet']),
    ('baby-shower', 'Baby Shower Catering', 'Baby Shower', 'cradle', 'menu-sweets',
     'Soft, celebratory vegetarian menus for baby showers and godh bharai ceremonies.',
     'Baby shower menus are designed around daytime service, family preferences and a light, joyful mood — with wholesome snacks, comforting mains, sweets and refreshing beverages.',
     ['Baby Showers', 'Godh Bharai', 'Naming Ceremonies', 'Daytime Celebrations'],
     ['Light veg starters', 'Family-style menus', 'Mithai counters', 'Fresh juices & shakes'],
     ['Dhokla', 'Paneer Tikka', 'Palak Paneer', 'Ghee Rice', 'Malpua', 'Pomegranate Juice']),
]

# Full menu, cleaned from public/catering MENU.xlsx
MENU = [
    ('breakfast', 'Breakfast & Snacks', 'menu-breakfast', 'Maharashtrian mornings and tea-time favourites.', [
        'Tea', 'Coffee', 'Kanda Poha', 'Upma', 'Idli Sambar Chutney', 'Medu Vada', 'Uttapam', 'Vada Pav', 'Samosa',
        'Vada Sambar', 'Bread Butter', 'Bread Pakoda', 'Chana Dal Vada', 'Sandwich', 'Gol Bhaji', 'Kanda Bhaji',
        'Mix Vada', 'Moong Dal Vada', 'Kothimbir Vadi', 'Mix Pakoda', 'Palak Bhaji', 'Mirchi Bhaji', 'Aloo Bhaji',
        'Moong Dal Bhaji', 'Dhokla', 'Khakhra', 'Misal Pav', 'Puri Bhaji', 'Tikka Puri']),
    ('soups', 'Soups', 'hero-feast', 'Warm, comforting openers.', [
        'Tomato Soup', 'Hot & Sour Soup', 'Manchow Soup', 'Sweet Corn Soup', 'Manchurian Soup', 'Mixed Vegetable Soup']),
    ('starters', 'Starters', 'menu-chinese', 'Tikkas, kababs, Indo-Chinese and crispy bites.', [
        'Veg Manchurian', 'Veg Cutlet', 'Hara Shahi Kabab', 'Cheese Ball', 'Veg Crush', 'Sweet Corn', 'Corn Tikka',
        'Rajma Tikka', 'Chana Tikka', 'Paneer Tikka', 'Mushroom Tikka', 'Green Mushroom', 'Fruit Tikka',
        'American Ball', 'Pudina Finger', 'Bread Pizza', 'Mini Vada', 'Chaat Tikka', 'Tiranga Paneer',
        'Aloo Dal Ki Tikki', 'Paneer Finger', 'French Fries', 'Crispy Sweet Potato', 'Paneer Roll', 'Bread Roll',
        'Chilli Potato', 'Chilli Gobi', 'Chilli Mushroom', 'Chilli Paneer', 'Spring Roll', 'Soyabean Chilli',
        'Mini Samosa', 'Veg Kabab', 'Cheese Pakoda', 'Gobi Pakoda', 'Baby Corn Pakoda', 'Palak Pakoda',
        'Aloo Pakoda', 'Moong Dal Bhajiya', 'Paneer Pakoda', 'Matcha Roll', 'Aloo Vadi', 'Tandoori Aloo']),
    ('paneer-gravies', 'Paneer & Gravy Specials', 'menu-indian', 'Rich, slow-cooked curries — the heart of the feast.', [
        'Paneer Masala', 'Paneer Butter Masala', 'Paneer Tikka Masala', 'Shahi Paneer', 'Kadai Paneer', 'Paneer Mumtaz',
        'Paneer Patiala', 'Paneer Nawabi', 'Malai Paneer', 'Paneer Angara', 'Paneer Afghani', 'Paneer Makhana',
        'Paneer Chaska Maska', 'Paneer Ghungroo', 'Matar Paneer', 'Paneer Makhanwala', 'Palak Paneer',
        'Baby Corn Paneer', 'Paneer Kabab', 'Basanta Paneer', 'Malai Kofta', 'Veg Bhuna', 'Palak Corn',
        'Mushroom Masala', 'Chole Mushroom', 'Matar Mushroom', 'Palak Mushroom', 'Mushroom Kurma', 'Shahi Kurma',
        'Matar Methi Malai', 'Kaju Curry', 'Gatte Ki Sabzi', 'Dum Aloo', 'Aloo Matar', 'Shak Bhaji', 'Chole Masala',
        'Punjabi Chole', 'Amritsari Chole', 'Rajma', 'Matki', 'Aloo Tamatar', 'Kala Harbara & Aloo', 'Aloo Palak',
        'Palak Baby Corn', 'Malai Chaap', 'Soya Chaap', 'Aloo Dandiya', 'Petha Sabzi', 'Pithla Besan']),
    ('dry-sabji', 'Dry Sabzi', 'svc-traditional', 'Homestyle vegetables, perfectly spiced.', [
        'Mix Veg', 'Veg Handi', 'Veg Kadai', 'Veg Maratha', 'Pivla Batata', 'Bhindi Masala', 'Baingan Masala',
        'Bharwa Baingan', 'Crunchy Bhindi', 'Bhindi Fry', 'Baingan Bharta', 'Methi Bhaji', 'Aloo Methi', 'Aloo Gobi',
        'Aloo Gajar Matar Gobi', 'Aloo Baingan', 'Aloo Patta Gobi', 'Aloo Shimla Mirch', 'Aloo Fry', 'Matki Sukki',
        'Matki Usal', 'Paneer Bhurji', 'Keema Gobi', 'Aloo Matar Dry', 'Tinda Fry']),
    ('dal', 'Dal & Kadhi', 'hero-feast', 'From Punjabi dal makhani to Maharashtrian varan.', [
        'Dal Makhani', 'Dal Fry', 'Dal Tadka', 'Varan', 'Panchratna Dal', 'Chole Ki Dal', 'Sambar', 'Dalcha (Veg)',
        'Kadhi', 'Punjabi Kadhi', 'Gujarati Kadhi', 'Rajasthani Kadhi', 'Masoor Dal Tadka', 'Akkha Masoor Dal Tadka',
        'Tomato Rajma', 'Mooli Sambar', 'South Indian Sambar', 'Dal Banjara (Rajasthani)', 'Toor Dal Tadka',
        'Hyderabadi Dal', 'Khatta Moong', 'Masala Chana Dal', 'Palak Dal', 'Green Moong Dal', 'Green Dal Fry']),
    ('rice', 'Rice, Pulao & Biryani', 'hero-feast', 'Fragrant grains for every palate.', [
        'Plain Rice', 'Jeera Rice', 'Matar Rice', 'Veg Rice', 'White Pulao', 'Kashmiri Pulao', 'Masala Pulao',
        'Veg Biryani', 'Lemon Rice', 'Fried Rice', 'Vegetable Fried Rice', 'Satrangi Rice', 'Thai Rice', 'Ghee Rice',
        'Tawa Rice', 'Palak Rice', 'Paneer Pulao', 'Masala Khichdi', 'Dal Khichdi', 'Mango Rice', 'Umbrella Rice',
        'Curd Rice', 'Garlic Butter Rice', 'Mushroom Pulao', 'Soyabean Pulao', 'Indrayani Rice', 'Kolam Rice', 'Green Rice']),
    ('breads', 'Rotis, Parathas & Breads', 'menu-indian', 'Fresh off the tawa and tandoor.', [
        'Puri', 'Fulka Roti', 'Chapati', 'Triangle Paratha', 'Laccha Paratha', 'Plain Paratha', 'Aloo Paratha',
        'Gobi Paratha', 'Paneer Paratha', 'Methi Paratha', 'Mooli Paratha', 'Mix Paratha', 'Butter Naan', 'Missi Roti',
        'Tandoori Roti', 'Amritsari Naan', 'Palak Puri', 'Masala Puri', 'Masala Paratha', 'Biscuit Paratha',
        'Makki Ki Roti', 'Rumali Roti', 'Reshmi Paratha', 'Kashmiri Roti', 'Jowar Bhakri', 'Bajra Bhakri',
        'Matar Paratha', 'Cheese Paratha', 'Corn Paratha', 'Puran Puri', 'Rice Bhakri', 'Onion Paratha',
        'Chole Bhature', 'Chilli Paratha', 'Besan Chilla', 'Dal Kachori', 'Dal Bati Churma']),
    ('sweets', 'Mithai & Sweets', 'menu-sweets', 'Traditional halwai-style sweets for every shubh moment.', [
        'Gulab Jamun', 'Kala Jamun', 'Traffic Jam', 'Moong Dal Halwa', 'Akhrot Halwa', 'Badam Halwa', 'Dudhi Halwa',
        'Pista Halwa', 'Pineapple Halwa', 'Chamcham', 'White Rasgulla', 'Pista Barfi', 'Mango Barfi',
        'Strawberry Barfi', 'Gulkand Barfi', 'Beetroot Barfi', 'Anjeer Barfi', 'Chocolate Barfi', 'Kalakand Barfi',
        'Malai Barfi', 'Besan Barfi', 'Coconut Barfi', 'Dudhiya Barfi', 'Gajak Barfi', 'Milk Cake', 'Kaju Katli',
        'Badam Katli', 'Pista Katli', 'Mango Roll', 'Kaju Roll', 'Badam Roll', 'Strawberry Roll', 'Anjeer Roll',
        'Balushahi', 'Motichoor Laddu', 'Boondi Laddu', 'Besan Laddu', 'Rava Laddu', 'Coconut Laddu', 'Churma Laddu',
        'Jalebi', 'Boondi', 'Mysore Pak', 'Parwal Ki Mithai', 'Mohanthal', 'Mango Peda', 'White Peda', 'Malai Peda',
        'Shakkar Gulab Jamun', 'Cut Gulab Jamun', 'Sweet Samosa', 'Gujiya', 'Malpua', 'Shahi Tukda', 'Soan Papdi']),
    ('rabdi', 'Rabdi & Desserts', 'menu-sweets', 'Creamy, chilled and indulgent.', [
        'Rabdi', 'Sitaphal Rabdi', 'Anjeer Rabdi', 'Rasmalai Rabdi', 'Basundi Rabdi', 'Strawberry Rabdi',
        'Laccha Rabdi', 'Apple Rabdi', 'Kesar Rabdi', 'Kulhad Rabdi', 'Pineapple Rabdi', 'Chikoo Rabdi',
        'Rasgulla Rabdi', 'Coconut Rabdi', 'Rose Rabdi', 'Fruit Cream', 'Fruit Custard']),
    ('beverages', 'Juices, Mastani & Shakes', 'menu-drinks', 'Fresh, chilled and 100% alcohol-free.', [
        'Orange Juice', 'Pineapple Juice', 'Strawberry Juice', 'Kiwi Juice', 'Mango Juice', 'Apple Juice',
        'Watermelon Juice', 'Pista Juice', 'Pomegranate Juice', 'Lemon Juice', 'Mango Mastani', 'Strawberry Mastani',
        'Anjeer Mastani', 'Banana Shake', 'Apple Shake', 'Mango Shake', 'Pista Shake', 'Badam Shake', 'Laccha Falooda']),
    ('live-stalls', 'Live Counters & Stalls', 'menu-chaat', 'Made-to-order theatre your guests will crowd around.', [
        'Pani Puri', 'Bhel', 'Aloo Tikki Chaat', 'Sweet Corn Bhel', 'Fruit Stall', 'Ice Cream', 'Barf Gola', 'Coffee',
        'Pizza', 'Burger', 'Paan Stall', 'Dahi Bhalla Chaat', 'Papdi Chaat', 'Rajbhog Chaat', 'Kacchi Dabeli',
        'Momos', 'Pav Bhaji', 'Bombay Pudina Chaat', 'Vegetable Chaat', 'Delhi Chaat', 'Dosa', 'Pudina Finger',
        'Chinese Stall']),
]

# Home page cuisine carousel: title, subtitle, image, menu anchor
CUISINES = [
    ('Maharashtrian Breakfast', 'Poha, misal pav, vada pav', 'menu-breakfast', 'breakfast'),
    ('Authentic North Indian', 'Paneer, dal makhani, naan', 'menu-indian', 'paneer-gravies'),
    ('South Indian', 'Dosa, idli, medu vada', 'menu-south', 'breakfast'),
    ('Indo-Chinese', 'Manchurian, noodles, chilli paneer', 'menu-chinese', 'starters'),
    ('Live Chaat Counters', 'Pani puri, dahi bhalla, dabeli', 'menu-chaat', 'live-stalls'),
    ('Mithai & Desserts', 'Kaju katli, jalebi, rabdi', 'menu-sweets', 'sweets'),
    ('Juices & Mastani', 'Mango mastani, shakes, coolers', 'menu-drinks', 'beverages'),
    ('Traditional Thali', 'Puran puri, varan bhaat', 'svc-traditional', 'dal'),
]

# Real event footage (public/video-*.mp4, re-encoded into assets/video)
VIDEOS = [
    ('event-1', 'Illuminated Live Counters', 'Our signature carved, back-lit counters at a night reception.'),
    ('event-3', 'Grand Buffet Line-up', 'A full buffet line-up, staffed and ready before guests arrive.'),
    ('event-4', 'Banquet Hall Service', 'Uniformed service team at a banquet dinner.'),
    ('event-5', 'Garden Chaat Counter', 'Fresh chaat and soup counter at an outdoor event.'),
    ('event-2', 'Hygienic Buffet Service', 'Masked, gloved staff serving from brass chafing dishes.'),
    ('event-6', 'Labelled Brass Handis', 'Every dish clearly labelled for guests.'),
]

# Gallery: image, title, category
GALLERY = [
    ('hero-buffet', 'Wedding Buffet at Night', 'Setups'),
    ('menu-chaat', 'Live Pani Puri Counter', 'Food'),
    ('event-1-poster', 'Illuminated Live Counters', 'Real Events'),
    ('hero-reception', 'Reception Dining Hall', 'Setups'),
    ('menu-sweets', 'Mithai Platter', 'Food'),
    ('event-3-poster', 'Buffet Line-up', 'Real Events'),
    ('about-counter', 'Brass Handi Counter', 'Setups'),
    ('menu-indian', 'Paneer Butter Masala', 'Food'),
    ('event-4-poster', 'Banquet Service Team', 'Real Events'),
    ('svc-traditional', 'Griha Pravesh Pangat', 'Setups'),
    ('menu-drinks', 'Welcome Drinks Bar', 'Food'),
    ('event-5-poster', 'Garden Soup Counter', 'Real Events'),
    ('svc-birthday', 'Birthday Dessert Table', 'Setups'),
    ('menu-south', 'South Indian Spread', 'Food'),
    ('event-2-poster', 'Hygienic Buffet Service', 'Real Events'),
    ('menu-breakfast', 'Maharashtrian Breakfast', 'Food'),
    ('svc-corporate', 'Corporate Lunch Buffet', 'Setups'),
    ('menu-chinese', 'Indo-Chinese Platter', 'Food'),
    ('event-6-poster', 'Labelled Brass Handis', 'Real Events'),
    ('hero-feast', 'Pure Veg Feast', 'Food'),
]

# Testimonials as supplied in the client's homepage reference design
TESTIMONIALS = [
    ('The food and service by Shubh Caterers was simply outstanding. Our wedding guests are still praising the taste and presentation!', 'Priya & Amol', 'Wedding'),
    ('Professional, punctual and delicious food. Highly recommended for corporate events.', 'Rahul Mehta', 'Corporate Event'),
    ('They made my daughter’s birthday party so special with amazing food and live counters. Truly a great experience!', 'Sneha Kulkarni', 'Birthday Party'),
]

PROCESS = [
    ('Share Your Occasion', 'Call, WhatsApp or send the enquiry form with your event type, date, venue and guest count.'),
    ('Curate the Menu', 'Pick from 350+ vegetarian dishes. We suggest combinations that suit your guests, season and budget.'),
    ('Plan the Service', 'Buffet flow, live counters, staffing and presentation are planned around your venue.'),
    ('Celebrate, Worry-free', 'Our uniformed team sets up, serves with care and leaves your guests asking for seconds.'),
]

FAQS = [
    ('Is Shubh Caterers pure vegetarian?', 'Yes. Every menu we serve is 100% vegetarian. Share any special dietary or no onion-garlic requirement while planning and we will discuss what is possible.'),
    ('Can the menu be customised?', 'Absolutely. Choose from our 350+ dish menu or ask for your family favourites — we shape the menu around your event, guests and budget.'),
    ('Which events do you cater?', 'Weddings, receptions, sangeet evenings, corporate events, birthdays, house warming and pooja ceremonies, baby showers, theme parties, institutional meals and parcel orders.'),
    ('Do you provide live counters?', 'Yes — pani puri, chaat, dosa, pav bhaji, pizza, momos, Chinese, barf gola, ice cream, paan and more, depending on the venue and menu plan.'),
    ('How is pricing decided?', 'Pricing depends on the menu, guest count, service format and venue. Share your requirements and we will send a clear, no-obligation quote.'),
    ('How early should I book?', 'For weddings and large events, we recommend booking as early as possible, especially during the wedding season. Smaller events can often be arranged at shorter notice — just call us.'),
    ('Do you serve outside Pune?', 'We are based in Tingre Nagar, Pune. For events in other areas or outstation venues, please call us to discuss logistics.'),
    ('How do I request a quote?', 'Fill the enquiry form (it opens WhatsApp with your details), call 9595956709 / 9822323230, or email shubhcaterers009@gmail.com.'),
]
