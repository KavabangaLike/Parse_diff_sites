import uuid

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from src.database.models import SearchLink, FbUser, Land, TgUser, UserGroup, Currency, Facility, Product, Picture

urls_for_parser = [
    ('Ubud',
     'https://www.facebook.com/marketplace/denpasar/propertyrentals?sortBy=creation_time_descend&query=House%20for%20rent&latitude=-8.5132&longitude=115.263&radius=7', '',
     ),
    ('Canggu',
     'https://www.facebook.com/marketplace/107286902636860/propertyrentals/?sortBy=creation_time_descend&query=House%20for%20rent&latitude=-8.6558&longitude=115.1342&radius=7', '',
     ),
    ('Sanur',
     'https://www.facebook.com/marketplace/denpasar/propertyrentals/?sortBy=creation_time_descend&query=House%20for%20rent&latitude=-8.6944&longitude=115.2597&radius=7', '',
     ),
    ('Tabanan',
     'https://www.facebook.com/marketplace/115971211750713/propertyrentals/?sortBy=creation_time_descend&query=House%20for%20rent&latitude=-8.5333&longitude=115.133&radius=4',
     '',
     ),
    ('Ungasan',
     'https://www.facebook.com/marketplace/107286902636860/propertyrentals/?sortBy=creation_time_descend&query=House%20for%20rent&latitude=-8.8271&longitude=115.168&radius=4.5',
     '',
     ),
]


# fb_users = [
#     ('geifadetteuwoi-2186@yopmail.com', 'kdsxe8t5'),
#     ('seiyoupeiviwoi-8695@yopmail.com', 'kdsxe8t5'),
#     ('kugreufraweti-9375@yopmail.com', 'kdsxe8t5'),
#     ('taffousseheze-7383@yopmail.com', 'kdsxe8t5'),
#     ('hugiveyada-5236@yopmail.com', 'kdsxe8t5'),
#     ('coihollocewe-6078@yopmail.com', 'kdsxe8t5'),
#     ('xeixotteiquissau-7998@yopmail.com', 'kdsxe8t5'),
#     ('vouyulilloicu-2430@yopmail.com', 'kdsxe8t5'),
#     ('loijedebaubrei-8212@yopmail.com', 'kdsxe8t5'),
# ]

# fb_users = [
#     ('muveiboifroissoi-6883@yopmail.com', 'kdsxe8t5'),
#     ('fadoucroureke-3912@yopmail.com', 'kdsxe8t5'),
#     ('jouzohofromma-9472@yopmail.com', 'kdsxe8t5'),
#     ('vellarepoffa-3799@yopmail.com', 'kdsxe8t5'),
#     ('yenouxeyusso-4276@yopmail.com', 'kdsxe8t5'),
# ]

# fb_users = [
#     ('rojelotragru-2889@yopmail.com', 'kdsxe8t5'),
#     ('yomauttigreutri-6249@yopmail.com', 'acahi045v7km'),
# ]

fb_users = [
     # ('sandra2v756t3c@gmail.com', 's6MuqS6q2t'),
     # ('steven82az1ts551@gmail.com', '0bwEqhKKIf'),
     # ('kevinehnz884@gmail.com', 'TfjfP7YTIE'),
     # ('vince.joanne88285@gmail.com', 'pMVFxhmEf4'),
     # ('ronald77xx32057@gmail.com', 'gfOCPSEzgL'),
     # ('marymcaih463@gmail.com','Se1aiyha1a'),
     # ('maryhzoec991@gmail.com', '090HPZfaCD'),
     # ('dorothyvlaik627@gmail.com', 'ZGysSOOk6f'),
     # ('laurafzeut892@gmail.com', 'MMvj7O3JXB'),
     # ('lheskummil8@hotmail.com', 'NoEEsZy8rO'),
     # ('middigaullawou-3759@yopmail.com', '177fc351'),
     ('moinoivibajoi-3324@yopmail.com', 'lololoshka'),
     ('feuquitracoupeu-5189@yopmail.com', 'panarama'),
     ('peuquobrammatu-6342@yopmail.com', 'bamasaka'),
     ('prurehitrilleu-4474@yopmail.com', 'doradora'),
     ('trommoteudique-6621@yopmail.com', 'sodoharu'),
]

lands = [
    ('Ubud', '112356482109204'),
    ('Canggu', '107286902636860'),
    ('Sanur', 'denpasar'),
]

users = [
    ('643668236', 'superadmins',),
    ('57360326', 'superadmins',),
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
    ('день', 1, ),
    ('месяц', 1, ),
    ('год', 1, ),
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

for link in urls_for_parser:
    with Land.session() as session:
        link_ = [SearchLink(link=link[1], query='none'), ]
        land = Land(name=link[0], link_name=uuid.uuid4())
        land.links = link_
        try:
            print(land.name)
            session.add(land)
            session.commit()
            session.refresh(land)
        except IntegrityError as ex:
            pass

# for lnd in lands:
#     with Land.session() as session:
#         links = [SearchLink(link=i[1], query='123') for i in urls_for_parser]
#
#         land = Land(name=lnd[0], link_name=lnd[1])
#         land.links = links
#         try:
#             print(land)
#             session.add(land)
#             session.commit()
#             session.refresh(land)
#         except IntegrityError as ex:
#             pass


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
