from src.models import SearchingLinks

urls_for_parser = [
    ('Ubud', 'Rent house ubud',
     'https://www.facebook.com/marketplace/112356482109204/search/?query=Rent%20house%20ubud',
     ),
    ('Ubud', 'villa ubud',
     'https://www.facebook.com/marketplace/112356482109204/search/?query=villa%20ubud&exact=false',
     ),
    ('Ubud', 'Rent house',
     'https://www.facebook.com/marketplace/112356482109204/search?query=Rent%20house',
     ),
    ('Ubud', 'ubud apartment',
     'https://www.facebook.com/marketplace/112356482109204/search?query=ubud%20apartment',
     ),
    ('Ubud', '2 bedroom',
     'https://www.facebook.com/marketplace/112356482109204/search?query=2%20bedroom',
     ),
    ('Ubud', '3 bedroom',
     'https://www.facebook.com/marketplace/112356482109204/search?query=3%20bedroom',
     )
]

for l in urls_for_parser:
    with SearchingLinks.session() as session:
        link = SearchingLinks(link=l[2], geo=l[0], query=l[1])
        session.add(link)
        session.commit()
        session.refresh(link)