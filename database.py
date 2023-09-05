from src.models import Product, TgUser, FbUser, SearchLink, Land, Currency, ProductFacility, Facility, Picture, \
    UserGroup, UserFacility
from sqlalchemy import select, or_
from datetime import datetime


# from src.utils.google_sheet import gh_prepare_data, gh_insert


def pg_insert_product(data):  ##
    with Product.session() as session:
        product = Product(
            product_id=data[0].split('/')[5],
            product_link=data[0],
            title=data[1],
            price=data[2],
            currency=session.scalar(select(Currency.id).filter(Currency.symbol == 'rp')),  ##
            in_month=True,  ##
            land=session.scalar(select(Land.id).filter(Land.name == data[-1])),
            description=data[4],
            profile_url=data[5],
            expose_datetime=data[7],
        )

        pictures = [Picture(link=i) for i in data[6].split(',')]
        product.pictures = pictures
        facilities = [Facility(name=i, type=3) for i in data[3]]  ##
        # product.facilities = facilities
        session.add(product)
        session.commit()
        session.refresh(product)


def pg_select_product_links():  #
    with Product.session() as session:
        query = select(Product.product_id)
        return [*session.scalars(query).all()]


def pg_select_products(limit: int, offset: int):  ##
    with Product.session() as session:
        query = session.scalars(
            select(Product)
            .limit(limit)
            .offset(offset)
        )

        result = query.all()
        for pic in result[0].pictures:
            print(pic.product_id, pic.link)
        return [*result]


def pg_insert_new_user(user_id: str, access_expire: datetime, username: str, role='newbies'):  #
    with TgUser.session() as session:
        user = TgUser(id=user_id, access_expire=access_expire, username=username, show_products=True)
        user.user_group_id = session.scalar(select(UserGroup.id).filter(UserGroup.name == role))
        session.add(user)
        session.commit()
        session.refresh(user)


def pg_select_users_id(groups: list[str]) -> list[str]:  #
    users = []
    for group in groups:
        with TgUser.session() as session:
            query = session.query(TgUser.id).join(UserGroup) \
                .filter(UserGroup.name == group) \
                .filter(or_(datetime.now() < TgUser.access_expire, TgUser.access_expire == None)) \
                .filter(TgUser.show_products == True)
            users.extend(query.all())
    return [i[0] for i in users]


def pg_select_fb_users():  #
    with FbUser.session() as session:
        query = select(FbUser.login,
                       FbUser.password)
        users = session.execute(query)
        return [*users]


def pg_select_links():  #
    with SearchLink.session() as session:
        links = session.query(
            SearchLink.link,
            SearchLink.query,
            Land.name).join(Land, Land.id == SearchLink.land_id, isouter=True).all()
        return [*links]


def pg_change_user_group(user_id, group: str):
    with TgUser.session() as session:
        user = session.get(TgUser, user_id)
        user.user_group_id = session.scalar(select(UserGroup.id).filter(UserGroup.name == group))
        session.add(user)
        session.commit()
        session.refresh(user)


def pg_change_user_access_period(user_id, period: datetime | None) -> None:
    with TgUser.session() as session:
        user = session.get(TgUser, user_id)
        user.access_expire = period
        session.add(user)
        session.commit()
        session.refresh(user)


def pg_show_ads(user_id, action: bool) -> None:
    with TgUser.session() as session:
        user = session.get(TgUser, user_id)
        user.show_products = action
        session.add(user)
        session.commit()
        session.refresh(user)


def pg_select_facility(type_: int):
    with Facility.session() as session:
        facility = session.scalars(select(Facility.name).filter(Facility.type == type_))
        return [*facility.all()]


def pg_select_related_facility(user_id, type_: int):
    with UserFacility.session() as session:
        query = session.query(Facility.name).select_from(UserFacility).join(Facility).filter(Facility.type == type_)\
            .filter(UserFacility.user_id == user_id)
        return [i[0] for i in query.all()]


def pg_insert_related_facility(user_id, facility_names: list[str]):
    with UserFacility.session() as session:
        for facility in facility_names:
            facility_ = UserFacility(user_id=user_id)
            facility_.facility_id = session.scalar(select(Facility.id).filter(Facility.name == facility))
            session.add(facility_)
            session.commit()
            session.refresh(facility_)


def pg_delete_related_facility(user_id, facility_name: str):  # WARNING
    with UserFacility.session() as session:
        f_id = session.query(Facility.id).filter(Facility.name == facility_name)
        session.query(UserFacility).filter(UserFacility.facility_id.in_(f_id.subquery())).filter(UserFacility.user_id == user_id).delete(synchronize_session=False)
        session.commit()

# gh_insert(*gh_prepare_data(*pg_select_products(1, 45)))
# pg_insert_related_facility('643668236', ['месяц', 'год', 'бассейн', 'стиральная машина'])
# print(pg_select_related_facility('643668236', 3))
# print(pg_select_facility(1))

# pg_delete_related_facility('643668236', 'бассейн')
# print(pg_select_links())
#pg_select_products(10, 0)