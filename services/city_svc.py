from typing import List

from sqlalchemy.ext.asyncio import AsyncSession

from adapters.ibge.ibge_api import IbgeAPI
from repositories.city_repo import CityRepository


def fetch_cities():
    cities_list = IbgeAPI().fetch_cities()
    return cities_list


async def fetch_and_save_cities(db: AsyncSession):
    cities_list = fetch_cities()
    city_repo = CityRepository(db)
    return await city_repo.bulk_create_or_update(cities_list)


async def get_cities(db: AsyncSession, ids: List[int] = None, name: str = None, state_abbreviation: str = None):
    cities_list = await CityRepository(db).get(ids, name, state_abbreviation)
    return cities_list


async def get_city_by_id(db: AsyncSession, id: int):
    city = await CityRepository(db).get_by_id(id)
    return city
