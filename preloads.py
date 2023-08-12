from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from src.models import SearchLink, FbUser, Land, TgUser, UserGroup, Currency, Facility, Product, Picture

urls_for_parser = [
    ('Villa',
     'https://www.facebook.com/marketplace/', '/search/?query=',
     ),
    ('Rent house',
     'https://www.facebook.com/marketplace/', '/search?query=',
     ),
    ('Apartment',
     'https://www.facebook.com/marketplace/', '/search?query=',
     ),
    ('2 bedroom',
     'https://www.facebook.com/marketplace/', '/search?query=',
     ),
    ('3 bedroom',
     'https://www.facebook.com/marketplace/', '/search?query=',
     )
]


fb_users = [
    ('geifadetteuwoi-2186@yopmail.com', 'kdsxe8t5'),
    ('seiyoupeiviwoi-8695@yopmail.com', 'kdsxe8t5'),
    ('kugreufraweti-9375@yopmail.com', 'kdsxe8t5'),
    ('taffousseheze-7383@yopmail.com', 'kdsxe8t5'),
    ('hugiveyada-5236@yopmail.com', 'kdsxe8t5'),
    ('coihollocewe-6078@yopmail.com', 'kdsxe8t5'),
    ('xeixotteiquissau-7998@yopmail.com', 'kdsxe8t5'),
    ('vouyulilloicu-2430@yopmail.com', 'kdsxe8t5'),
    ('loijedebaubrei-8212@yopmail.com', 'kdsxe8t5'),
]

lands = [
    ('Ubud', '112356482109204'),
    ('Canggu', '107286902636860'),
    ('Sanur', 'denpasar'),
]

users = [
    ('643668236', 'superadmins',),
   # ('57360326', 'superadmins',),
]

groups = [
    ('newbies',),
    ('users',),
    ('admins',),
    ('superadmins',),
]

currency = [
    'rp',
    '$',
    'idr',
]

facilities = [
    ('бассейн', 3, ),
    ('стиральная машина', 3, ),
    ('электричество', 3, ),
    ('уборка', 3, ),
    ('замена белья', 3, ),
    ('парковка для машины', 3, ),
    ('паркова для байков', 3, ),
    ('общий зал', 3, ),
    ('тихое место без соседей', 3, ),
    ('кухня', 3, ),
    ('ванна', 3, ),
    ('газебо', 3, ),
]

for lnd in lands:
    with Land.session() as session:
        links = [SearchLink(link=i[1]+lnd[1]+i[2]+i[0], query=i[0]) for i in urls_for_parser]

        land = Land(name=lnd[0], link_name=lnd[1])
        land.links = links
        try:
            session.add(land)
            session.commit()
            session.refresh(land)
        except IntegrityError as ex:
            pass


for usr in fb_users:
    with FbUser.session() as session:
        user = FbUser(login=usr[0],
                      password=usr[1])
        try:
            session.add(user)
            session.commit()
            session.refresh(user)
        except IntegrityError:
            pass


for grup in groups:
    with UserGroup.session() as session:
        group = UserGroup(name=grup[0])
        try:
            session.add(group)
            session.commit()
            session.refresh(group)
        except IntegrityError:
            pass


for usr in users:
    with TgUser.session() as session:
        user = TgUser(id=usr[0])
        user.user_group_id = session.scalar(select(UserGroup.id).filter(UserGroup.name == 'superadmins'))
        try:
            session.add(user)
            session.commit()
            session.refresh(user)
        except IntegrityError as ex:
            pass 

for curr in currency:
    with Currency.session() as session:
        currency_ = Currency(symbol=curr)
        try:
            session.add(currency_)
            session.commit()
            session.refresh(currency_)
        except IntegrityError:
            pass


for facility in facilities:
    with Facility.session() as session:
        facility_ = Facility(name=facility[0], type=facility[1])
        try:
            session.add(facility_)
            session.commit()
            session.refresh(facility_)
        except IntegrityError:
            pass


def pg_select_products(limit: int, offset: int): ##
    with Product.session() as session:
        query = session.query(Product.product_id,
                       Product.title,
                       Product.product_link,
                       Product.price,
                       Product.description,
                       Product.profile_url,
                       Product.expose_datetime,
                       Picture.link).join(Picture, Picture.product_id==Product.id).limit(limit).offset(offset)

        result = query.all()
        return [*result]


#with TgUser.session() as session:
    #users = session.scalars(select(TgUser.user_group_id, TgUser.id)).all()
    #print(users)
