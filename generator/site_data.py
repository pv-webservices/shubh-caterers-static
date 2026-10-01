"""Content for the Shubh Caterers website. Edit here, then run `python generate.py`."""

BUSINESS = {
    'name': 'Shubh Caterers',
    'phones': [('Pawan Agarwal', '9595956709'), ('Ajay Agarwal', '9822323230')],
    'whatsapp': '919595956709',
    'email': 'info@shubhcaterers.in',
    'address_lines': ['Sr. No. 51, Plot No. 117, Lane No. 9,', 'Bhairvnagar, Dhanori,', 'Pune - 411015, Maharashtra'],
    'address_short': 'Sr. No. 51, Plot No. 117, Lane No. 9, Bhairvnagar, Dhanori, Pune - 411015',
    'map_url': 'https://maps.app.goo.gl/AqQEvxm9zxHXycdv7',
    'map_coords': '18.586014,73.886506',
    'domain': 'https://shubhcaterers.in',
}

# slug, title, short label, icon, image, summary, intro, suitable for, highlights, featured menu picks
SERVICES = [
    ('wedding-catering', 'Wedding Catering', 'Weddings', 'rings', 'venues/wedding-buffet-night',
     'Grand pure-vegetarian wedding feasts, from the welcome drink to the last spoon of rabdi.',
     'Wedding menus are planned around the flow of your celebration, your guest profile, the venue and family traditions. We bring variety, beautiful presentation, graceful service and a warm dining experience your guests will talk about long after the pheras.',
     ['Engagement & Sagai', 'Haldi & Mehendi', 'Wedding Ceremonies', 'Reception Dinners'],
     ['Multi-cuisine vegetarian menus', 'Illuminated live counters', 'Mithai & rabdi stations', 'Buffet or table service'],
     ['Paneer Tikka', 'Dal Makhani', 'Veg Biryani', 'Butter Naan', 'Kesar Rabdi', 'Pani Puri']),
    ('cocktail-events', 'Cocktail & Mocktail Evenings', 'Cocktails', 'glass', 'food/welcome-drinks',
     'Elegant veg small plates, mocktails and live counters for sangeet nights and social evenings.',
     'Cocktail-format evenings need food guests can enjoy while they mingle. We pair passed vegetarian appetisers and live counters with a colourful mocktail, mastani and shake bar — all zero-proof and made fresh.',
     ['Sangeet Nights', 'Engagement Parties', 'Social Evenings', 'Corporate Mixers'],
     ['Passed veg appetisers', 'Mocktail & mastani bar', 'Live chaat & grill counters', 'Dessert bites'],
     ['Cheese Ball', 'Chilli Paneer', 'Mango Mastani', 'Kiwi Juice', 'Corn Tikka', 'Spring Roll']),
    ('corporate-catering', 'Corporate Catering', 'Corporates', 'briefcase', 'events/corporate-lunch-buffet',
     'Punctual, professional vegetarian catering for meetings, conferences, launches and office celebrations.',
     'Corporate catering is planned around your schedule, service speed and a menu that works for a mixed group. From breakfast and high-tea to polished buffet lunches, we keep it on time, hygienic and hassle-free.',
     ['Meetings & Conferences', 'Office Celebrations', 'Product Launches', 'Training Programs'],
     ['Breakfast & high-tea', 'Buffet lunches', 'Tea & coffee service', 'Custom event menus'],
     ['Poha', 'Veg Sandwich', 'Paneer Butter Masala', 'Jeera Rice', 'Fulka Roti', 'Gulab Jamun']),
    ('theme-party', 'Theme Parties', 'Theme Party', 'confetti', 'venues/brass-handi-counter',
     'Menus, counters and presentation styled to match your chosen celebration theme.',
     'Theme-party catering connects food, décor and service with the mood of your event. Food stations, counters and dessert displays are styled to match your theme — Rajasthani, street-food, festive or modern.',
     ['Festive Events', 'Milestone Parties', 'Family Celebrations', 'Concept Events'],
     ['Theme-aligned menus', 'Styled food stations', 'Illuminated live counters', 'Custom dessert displays'],
     ['Dal Bati Churma', 'Kacchi Dabeli', 'Pav Bhaji', 'Momos', 'Barf Gola', 'Jalebi']),
    ('private-party', 'Private Parties', 'Private Party', 'cheers', 'food/pure-veg-feast',
     'Flexible vegetarian catering for intimate get-togethers, anniversaries and home celebrations.',
     'Private events deserve a compact menu with great variety and attentive service. We plan the format around your guest count, your space and the pace of your gathering.',
     ['Family Dinners', 'Anniversaries', 'Home Gatherings', 'Kitty Parties'],
     ['Customised menus', 'Compact buffet setups', 'Live counter options', 'Dessert & beverage stations'],
     ['Hara Shahi Kabab', 'Malai Kofta', 'Kashmiri Pulao', 'Laccha Paratha', 'Rasmalai Rabdi', 'Mango Shake']),
    ('niche-events', 'Niche Events', 'Niche Events', 'star', 'food/live-chaat-counter',
     'Custom catering for unusual formats, curated experiences and special-purpose events.',
     'Some events don’t fit a template. For niche formats, we adapt the menu, equipment, service pattern and presentation to the actual venue and the experience you want to create.',
     ['Curated Gatherings', 'Community Events', 'Pop-up Formats', 'Religious Functions'],
     ['Flexible planning', 'Custom service format', 'Any cuisine, all vegetarian', 'Event-specific presentation'],
     ['Misal Pav', 'Puran Puri', 'Masala Dosa', 'Papadi Chaat', 'Falooda', 'Paan Stall']),
    ('institutional-catering', 'Institutional Catering', 'Institutional Catering', 'institution', 'food/south-indian-spread',
     'Consistent, hygienic vegetarian meal service for institutions, hostels and organisations.',
     'Institutional catering calls for consistency, hygiene, practical planning and dependable systems. Balanced vegetarian menus are structured around your schedule, head-count and nutritional needs.',
     ['Schools & Colleges', 'Hostels', 'Organisations', 'Group Meal Service'],
     ['Planned meal cycles', 'Hygienic preparation', 'Balanced vegetarian menus', 'Scalable service'],
     ['Idli Sambar', 'Upma', 'Dal Tadka', 'Mix Veg', 'Chapati', 'Plain Rice']),
    ('birthday-party', 'Birthday Parties', 'Birthday Party', 'cake', 'events/birthday-dessert-table',
     'Fun, festive vegetarian menus for kids, adults and milestone birthdays.',
     'Birthday catering can be playful, casual or premium. We design menus with crowd favourites, snacks, live counters, desserts and beverages that keep kids and grown-ups equally happy.',
     ['Kids Birthdays', 'Adult Birthdays', 'Milestone Birthdays', 'Home & Venue Parties'],
     ['Party-friendly snacks', 'Pizza, burger & momo stalls', 'Dessert tables', 'Mocktails & shakes'],
     ['Bread Pizza', 'French Fries', 'Cheese Ball', 'Ice Cream', 'Strawberry Shake', 'Chocolate Barfi']),
    ('house-warming', 'House Warming & Pooja', 'House Warming', 'home', 'events/griha-pravesh-pangat',
     'Traditional vegetarian catering for griha pravesh, satyanarayan pooja and new-home celebrations.',
     'House-warming menus are planned around ceremony timings, family traditions and the serving space available. From a traditional pangat on banana leaves to a modern buffet, we serve with care.',
     ['Griha Pravesh', 'Satyanarayan Pooja', 'Family Lunch', 'Vastu Shanti'],
     ['Traditional Maharashtrian thali', 'Banana-leaf pangat service', 'Compact service setup', 'Prasad & sweets'],
     ['Puran Puri', 'Varan', 'Masale Bhaat', 'Aloo Bhaji', 'Basundi Rabdi', 'Kothimbir Vadi']),
    ('parcels', 'Parcel Orders', 'Parcels', 'parcel', 'food/paneer-butter-masala',
     'Freshly prepared vegetarian food parcels for family functions, group meals and offices.',
     'Parcel orders are perfect when you want Shubh Caterers’ taste without a full on-site setup. Menu combinations and hygienic packaging are planned to suit your group size and occasion.',
     ['Family Functions', 'Group Meals', 'Office Orders', 'Small Celebrations'],
     ['Veg meal boxes', 'Bulk parcel orders', 'Menu customisation', 'Hygienic packaging'],
     ['Paneer Masala', 'Veg Pulao', 'Dal Fry', 'Puri', 'Gulab Jamun', 'Veg Cutlet']),
    ('baby-shower', 'Baby Shower Catering', 'Baby Shower', 'cradle', 'food/mithai-platter',
     'Soft, celebratory vegetarian menus for baby showers and godh bharai ceremonies.',
     'Baby shower menus are designed around daytime service, family preferences and a light, joyful mood — with wholesome snacks, comforting mains, sweets and refreshing beverages.',
     ['Baby Showers', 'Godh Bharai', 'Naming Ceremonies', 'Daytime Celebrations'],
     ['Light veg starters', 'Family-style menus', 'Mithai counters', 'Fresh juices & shakes'],
     ['Dhokla', 'Paneer Tikka', 'Palak Paneer', 'Ghee Rice', 'Malpua', 'Pomegranate Juice']),
]

# Full menu, cleaned from source-files/reference/catering-menu.xlsx
MENU = [
    ('breakfast', 'Breakfast & Snacks', 'food/maharashtrian-breakfast', 'Maharashtrian mornings and tea-time favourites.', [
        'Tea', 'Coffee', 'Kanda Poha', 'Upma', 'Idli Sambar Chutney', 'Medu Vada', 'Uttapam', 'Vada Pav', 'Samosa',
        'Vada Sambar', 'Bread Butter', 'Bread Pakoda', 'Chana Dal Vada', 'Sandwich', 'Gol Bhaji', 'Kanda Bhaji',
        'Mix Vada', 'Moong Dal Vada', 'Kothimbir Vadi', 'Mix Pakoda', 'Palak Bhaji', 'Mirchi Bhaji', 'Aloo Bhaji',
        'Moong Dal Bhaji', 'Dhokla', 'Khakhra', 'Misal Pav', 'Puri Bhaji', 'Tikka Puri']),
    ('soups', 'Soups', 'food/pure-veg-feast', 'Warm, comforting openers.', [
        'Tomato Soup', 'Hot & Sour Soup', 'Manchow Soup', 'Sweet Corn Soup', 'Manchurian Soup', 'Mixed Vegetable Soup']),
    ('starters', 'Starters', 'food/indo-chinese-platter', 'Tikkas, kababs, Indo-Chinese and crispy bites.', [
        'Veg Manchurian', 'Veg Cutlet', 'Hara Shahi Kabab', 'Cheese Ball', 'Veg Crush', 'Sweet Corn', 'Corn Tikka',
        'Rajma Tikka', 'Chana Tikka', 'Paneer Tikka', 'Mushroom Tikka', 'Green Mushroom', 'Fruit Tikka',
        'American Ball', 'Pudina Finger', 'Bread Pizza', 'Mini Vada', 'Chaat Tikka', 'Tiranga Paneer',
        'Aloo Dal Ki Tikki', 'Paneer Finger', 'French Fries', 'Crispy Sweet Potato', 'Paneer Roll', 'Bread Roll',
        'Chilli Potato', 'Chilli Gobi', 'Chilli Mushroom', 'Chilli Paneer', 'Spring Roll', 'Soyabean Chilli',
        'Mini Samosa', 'Veg Kabab', 'Cheese Pakoda', 'Gobi Pakoda', 'Baby Corn Pakoda', 'Palak Pakoda',
        'Aloo Pakoda', 'Moong Dal Bhajiya', 'Paneer Pakoda', 'Matcha Roll', 'Aloo Vadi', 'Tandoori Aloo']),
    ('paneer-gravies', 'Paneer & Gravy Specials', 'food/paneer-butter-masala', 'Rich, slow-cooked curries — the heart of the feast.', [
        'Paneer Masala', 'Paneer Butter Masala', 'Paneer Tikka Masala', 'Shahi Paneer', 'Kadai Paneer', 'Paneer Mumtaz',
        'Paneer Patiala', 'Paneer Nawabi', 'Malai Paneer', 'Paneer Angara', 'Paneer Afghani', 'Paneer Makhana',
        'Paneer Chaska Maska', 'Paneer Ghungroo', 'Matar Paneer', 'Paneer Makhanwala', 'Palak Paneer',
        'Baby Corn Paneer', 'Paneer Kabab', 'Basanta Paneer', 'Malai Kofta', 'Veg Bhuna', 'Palak Corn',
        'Mushroom Masala', 'Chole Mushroom', 'Matar Mushroom', 'Palak Mushroom', 'Mushroom Kurma', 'Shahi Kurma',
        'Matar Methi Malai', 'Kaju Curry', 'Gatte Ki Sabzi', 'Dum Aloo', 'Aloo Matar', 'Shak Bhaji', 'Chole Masala',
        'Punjabi Chole', 'Amritsari Chole', 'Rajma', 'Matki', 'Aloo Tamatar', 'Kala Harbara & Aloo', 'Aloo Palak',
        'Palak Baby Corn', 'Malai Chaap', 'Soya Chaap', 'Aloo Dandiya', 'Petha Sabzi', 'Pithla Besan']),
    ('dry-sabji', 'Dry Sabzi', 'events/griha-pravesh-pangat', 'Homestyle vegetables, perfectly spiced.', [
        'Mix Veg', 'Veg Handi', 'Veg Kadai', 'Veg Maratha', 'Pivla Batata', 'Bhindi Masala', 'Baingan Masala',
        'Bharwa Baingan', 'Crunchy Bhindi', 'Bhindi Fry', 'Baingan Bharta', 'Methi Bhaji', 'Aloo Methi', 'Aloo Gobi',
        'Aloo Gajar Matar Gobi', 'Aloo Baingan', 'Aloo Patta Gobi', 'Aloo Shimla Mirch', 'Aloo Fry', 'Matki Sukki',
        'Matki Usal', 'Paneer Bhurji', 'Keema Gobi', 'Aloo Matar Dry', 'Tinda Fry']),
    ('dal', 'Dal & Kadhi', 'food/pure-veg-feast', 'From Punjabi dal makhani to Maharashtrian varan.', [
        'Dal Makhani', 'Dal Fry', 'Dal Tadka', 'Varan', 'Panchratna Dal', 'Chole Ki Dal', 'Sambar', 'Dalcha (Veg)',
        'Kadhi', 'Punjabi Kadhi', 'Gujarati Kadhi', 'Rajasthani Kadhi', 'Masoor Dal Tadka', 'Akkha Masoor Dal Tadka',
        'Tomato Rajma', 'Mooli Sambar', 'South Indian Sambar', 'Dal Banjara (Rajasthani)', 'Toor Dal Tadka',
        'Hyderabadi Dal', 'Khatta Moong', 'Masala Chana Dal', 'Palak Dal', 'Green Moong Dal', 'Green Dal Fry']),
    ('rice', 'Rice, Pulao & Biryani', 'food/pure-veg-feast', 'Fragrant grains for every palate.', [
        'Plain Rice', 'Jeera Rice', 'Matar Rice', 'Veg Rice', 'White Pulao', 'Kashmiri Pulao', 'Masala Pulao',
        'Veg Biryani', 'Lemon Rice', 'Fried Rice', 'Vegetable Fried Rice', 'Satrangi Rice', 'Thai Rice', 'Ghee Rice',
        'Tawa Rice', 'Palak Rice', 'Paneer Pulao', 'Masala Khichdi', 'Dal Khichdi', 'Mango Rice', 'Umbrella Rice',
        'Curd Rice', 'Garlic Butter Rice', 'Mushroom Pulao', 'Soyabean Pulao', 'Indrayani Rice', 'Kolam Rice', 'Green Rice']),
    ('breads', 'Rotis, Parathas & Breads', 'food/paneer-butter-masala', 'Fresh off the tawa and tandoor.', [
        'Puri', 'Fulka Roti', 'Chapati', 'Triangle Paratha', 'Laccha Paratha', 'Plain Paratha', 'Aloo Paratha',
        'Gobi Paratha', 'Paneer Paratha', 'Methi Paratha', 'Mooli Paratha', 'Mix Paratha', 'Butter Naan', 'Missi Roti',
        'Tandoori Roti', 'Amritsari Naan', 'Palak Puri', 'Masala Puri', 'Masala Paratha', 'Biscuit Paratha',
        'Makki Ki Roti', 'Rumali Roti', 'Reshmi Paratha', 'Kashmiri Roti', 'Jowar Bhakri', 'Bajra Bhakri',
        'Matar Paratha', 'Cheese Paratha', 'Corn Paratha', 'Puran Puri', 'Rice Bhakri', 'Onion Paratha',
        'Chole Bhature', 'Chilli Paratha', 'Besan Chilla', 'Dal Kachori', 'Dal Bati Churma']),
    ('sweets', 'Mithai & Sweets', 'food/mithai-platter', 'Traditional halwai-style sweets for every shubh moment.', [
        'Gulab Jamun', 'Kala Jamun', 'Traffic Jam', 'Moong Dal Halwa', 'Akhrot Halwa', 'Badam Halwa', 'Dudhi Halwa',
        'Pista Halwa', 'Pineapple Halwa', 'Chamcham', 'White Rasgulla', 'Pista Barfi', 'Mango Barfi',
        'Strawberry Barfi', 'Gulkand Barfi', 'Beetroot Barfi', 'Anjeer Barfi', 'Chocolate Barfi', 'Kalakand Barfi',
        'Malai Barfi', 'Besan Barfi', 'Coconut Barfi', 'Dudhiya Barfi', 'Gajak Barfi', 'Milk Cake', 'Kaju Katli',
        'Badam Katli', 'Pista Katli', 'Mango Roll', 'Kaju Roll', 'Badam Roll', 'Strawberry Roll', 'Anjeer Roll',
        'Balushahi', 'Motichoor Laddu', 'Boondi Laddu', 'Besan Laddu', 'Rava Laddu', 'Coconut Laddu', 'Churma Laddu',
        'Jalebi', 'Boondi', 'Mysore Pak', 'Parwal Ki Mithai', 'Mohanthal', 'Mango Peda', 'White Peda', 'Malai Peda',
        'Shakkar Gulab Jamun', 'Cut Gulab Jamun', 'Sweet Samosa', 'Gujiya', 'Malpua', 'Shahi Tukda', 'Soan Papdi']),
    ('rabdi', 'Rabdi & Desserts', 'food/mithai-platter', 'Creamy, chilled and indulgent.', [
        'Rabdi', 'Sitaphal Rabdi', 'Anjeer Rabdi', 'Rasmalai Rabdi', 'Basundi Rabdi', 'Strawberry Rabdi',
        'Laccha Rabdi', 'Apple Rabdi', 'Kesar Rabdi', 'Kulhad Rabdi', 'Pineapple Rabdi', 'Chikoo Rabdi',
        'Rasgulla Rabdi', 'Coconut Rabdi', 'Rose Rabdi', 'Fruit Cream', 'Fruit Custard']),
    ('beverages', 'Juices, Mastani & Shakes', 'food/welcome-drinks', 'Fresh, chilled and 100% alcohol-free.', [
        'Orange Juice', 'Pineapple Juice', 'Strawberry Juice', 'Kiwi Juice', 'Mango Juice', 'Apple Juice',
        'Watermelon Juice', 'Pista Juice', 'Pomegranate Juice', 'Lemon Juice', 'Mango Mastani', 'Strawberry Mastani',
        'Anjeer Mastani', 'Banana Shake', 'Apple Shake', 'Mango Shake', 'Pista Shake', 'Badam Shake', 'Laccha Falooda']),
    ('live-stalls', 'Live Counters & Stalls', 'food/live-chaat-counter', 'Made-to-order theatre your guests will crowd around.', [
        'Pani Puri', 'Bhel', 'Aloo Tikki Chaat', 'Sweet Corn Bhel', 'Fruit Stall', 'Ice Cream', 'Barf Gola', 'Coffee',
        'Pizza', 'Burger', 'Paan Stall', 'Dahi Bhalla Chaat', 'Papdi Chaat', 'Rajbhog Chaat', 'Kacchi Dabeli',
        'Momos', 'Pav Bhaji', 'Bombay Pudina Chaat', 'Vegetable Chaat', 'Delhi Chaat', 'Dosa', 'Pudina Finger',
        'Chinese Stall']),
]

# Home page cuisine carousel: title, subtitle, image, menu anchor
CUISINES = [
    ('Maharashtrian Breakfast', 'Poha, misal pav, vada pav', 'food/maharashtrian-breakfast', 'breakfast'),
    ('Authentic North Indian', 'Paneer, dal makhani, naan', 'food/paneer-butter-masala', 'paneer-gravies'),
    ('South Indian', 'Dosa, idli, medu vada', 'food/south-indian-spread', 'breakfast'),
    ('Indo-Chinese', 'Manchurian, noodles, chilli paneer', 'food/indo-chinese-platter', 'starters'),
    ('Live Chaat Counters', 'Pani puri, dahi bhalla, dabeli', 'food/live-chaat-counter', 'live-stalls'),
    ('Mithai & Desserts', 'Kaju katli, jalebi, rabdi', 'food/mithai-platter', 'sweets'),
    ('Juices & Mastani', 'Mango mastani, shakes, coolers', 'food/welcome-drinks', 'beverages'),
    ('Traditional Thali', 'Puran puri, varan bhaat', 'events/griha-pravesh-pangat', 'dal'),
]

# Real event footage (public/video-*.mp4, re-encoded into assets/video)
VIDEOS = [
    ('event-1', 'Illuminated Live Counters', 'Our signature carved, back-lit counters at a night reception.'),
    ('event-3', 'Grand Buffet Line-up', 'A full buffet line-up, staffed and ready before guests arrive.'),
    ('event-4', 'Banquet Hall Service', 'Uniformed service team at a banquet dinner.'),
    ('event-5', 'Garden Buffet Service', 'Brass handis and fresh starters served at an outdoor garden event.'),
    ('event-2', 'Hygienic Buffet Service', 'Masked, gloved staff serving from brass chafing dishes.'),
    ('event-6', 'Labelled Brass Handis', 'Every dish clearly labelled for guests.'),
]

# Gallery: image, title, category
GALLERY = [
    ('venues/wedding-buffet-night', 'Wedding Buffet at Night', 'Setups'),
    ('food/live-chaat-counter', 'Live Pani Puri Counter', 'Food'),
    ('video-posters/event-1', 'Illuminated Live Counters', 'Real Events'),
    ('venues/reception-dining-hall', 'Reception Dining Hall', 'Setups'),
    ('food/mithai-platter', 'Mithai Platter', 'Food'),
    ('video-posters/event-3', 'Buffet Line-up', 'Real Events'),
    ('venues/brass-handi-counter', 'Brass Handi Counter', 'Setups'),
    ('food/paneer-butter-masala', 'Paneer Butter Masala', 'Food'),
    ('video-posters/event-4', 'Banquet Service Team', 'Real Events'),
    ('events/griha-pravesh-pangat', 'Griha Pravesh Pangat', 'Setups'),
    ('food/welcome-drinks', 'Welcome Drinks Bar', 'Food'),
    ('video-posters/event-5', 'Garden Buffet Service', 'Real Events'),
    ('events/birthday-dessert-table', 'Birthday Dessert Table', 'Setups'),
    ('food/south-indian-spread', 'South Indian Spread', 'Food'),
    ('video-posters/event-2', 'Hygienic Buffet Service', 'Real Events'),
    ('food/maharashtrian-breakfast', 'Maharashtrian Breakfast', 'Food'),
    ('events/corporate-lunch-buffet', 'Corporate Lunch Buffet', 'Setups'),
    ('food/indo-chinese-platter', 'Indo-Chinese Platter', 'Food'),
    ('video-posters/event-6', 'Labelled Brass Handis', 'Real Events'),
    ('food/pure-veg-feast', 'Pure Veg Feast', 'Food'),
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
    ('Do you serve outside Pune?', 'We are based in Dhanori, Pune. For events in other areas or outstation venues, please call us to discuss logistics.'),
    ('How do I request a quote?', 'Send the enquiry form on any page, WhatsApp us, call 9595956709 / 9822323230, or email info@shubhcaterers.in.'),
]
