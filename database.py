from typing import Optional

from src.database.models import Product, TgUser, FbUser, SearchLink, Land, Currency, Facility, Picture, \
    UserGroup, UserFacility, UserLand
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
            land=session.scalar(select(Land.id).filter(Land.name == data[-1].split('(')[1].replace(')', '').strip())),
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


def pg_select_users(groups: list[str]) -> list[TgUser]:  #
    users = []
    with TgUser.session() as session:
        query = session.query(TgUser).join(UserGroup) \
            .filter(UserGroup.name.in_(groups)) \
            .filter(or_(datetime.now() < TgUser.access_expire, TgUser.access_expire == None)) \
            .filter(TgUser.show_products == True)
        users.extend(query.all())
        for user in users:
            test = user.user_facility
    return users


# print(pg_select_users(['users', 'admins', 'superadmins', 'newbies'])

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


def pg_select_facility() -> list[Facility]:
    with Facility.session() as session:
        return session.scalars(select(Facility)).all()

def pg_select_related_facility(user_id, type_: int):
    with UserFacility.session() as session:
        query = session.query(Facility.name).select_from(UserFacility).join(Facility).filter(Facility.type == type_) \
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
        session.query(UserFacility).filter(UserFacility.facility_id.in_(f_id.subquery())).filter(
            UserFacility.user_id == user_id).delete(synchronize_session=False)
        session.commit()


def pg_select_lands() -> list[str]:
    with Land.session() as session:
        return session.scalars(select(Land.name)).all()


def pg_select_related_lands(user_id):
    with UserLand.session() as session:
        lands = session.query(Land).select_from(UserLand).join(Land).filter(UserLand.user_id == user_id).all()
        return [i.name for i in lands]


def pg_del_related_lands(user_id):
    with UserLand.session() as session:
        session.query(UserLand).filter(UserLand.user_id == user_id).delete(synchronize_session=False)
        session.commit()


def pg_insert_related_lands(user_id, lands):
    with UserLand.session() as session:
        lands_id = session.scalars(select(Land.id).filter(Land.name.in_(lands)))
        uls = []
        for land_id in lands_id:
            uls.append(UserLand(user_id=user_id, land_id=land_id))
        session.add_all(uls)
        session.commit()
        for ul in uls:
            session.refresh(ul)


def pg_select_userland_user(land: str) -> list:
    with UserLand.session() as session:
        ids = session.query(UserLand.user_id).select_from(UserLand).join(Land).filter(Land.name == land).all()
        return [i[0] for i in ids]


def pg_update_user_price(price_type: str, price_value: int, user_id):
    with TgUser.session() as session:
        current_user = session.get(TgUser, user_id)
        if price_type == 'min_price':
            current_user.min_price = price_value
        elif price_type == 'max_price':
            current_user.max_price = price_value
        session.add(current_user)
        session.commit()


def pg_select_facilities(type_: int, user_id: Optional[int] = None) -> list[str]:
    if user_id:
        with Facility.session() as session:
            return [f.facility.name for f in
                    session.scalars(select(UserFacility).filter(UserFacility.user_id == user_id)).all()
                    if f]
    with Facility.session() as session:
        return [f.name for f in session.scalars(select(Facility).filter(Facility.type == type_))]


def pg_del_related_rooms(user_id: int):
    with UserFacility.session() as session:
        session.query(UserFacility).filter(UserFacility.user_id == user_id).delete(synchronize_session=False)
        session.commit()


def pg_insert_related_rooms(user_id, facilities: list):
    with UserFacility.session() as session:
        facilities_id = session.scalars(select(Facility.id).filter(Facility.name.in_(facilities)))
        uls = []
        for facility_id in facilities_id:
            uls.append(UserFacility(user_id=user_id, facility_id=facility_id))
        session.add_all(uls)
        session.commit()
        for ul in uls:
            session.refresh(ul)

