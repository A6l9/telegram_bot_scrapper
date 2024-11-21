from typing import Iterable, List

from loguru import logger
from sqlalchemy import Select, update
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import Query
from sqlalchemy.sql.ddl import DropTable
from typing_extensions import Any
from database.models import Users
from database.database import Base

class BaseInterface:
    def __init__(self, db_url: str):
        """
        Класс-интерфейс для работы с БД. Держит сессию и предоставляет методы для работы с БД.

        :param db_url: Путь к БД формата: "database+driver://name:password@host/db_name"
        self.base базовый класс моделей с которыми будете работать.
        """
        self.engine = create_async_engine(db_url, pool_timeout=60, pool_size=900, max_overflow=100)
        self.async_ses = async_sessionmaker(bind=self.engine, class_=AsyncSession, expire_on_commit=False)
        self.base = Base

    async def initial(self):
        """
        Метод иницилизирует соединение с БД.
        :return:
        """
        async with self.engine.begin() as conn:
            await conn.run_sync(self.base.metadata.create_all)

    async def _drop_all(self):
        """
        Метод для удаления всех таблиц текущей БД.
        :return:
        """
        async with self.engine.begin() as conn:
            await conn.run_sync(self.base.metadata.drop_all)

    async def del_has_rows(self, rows_object):
        async with self.async_ses() as session:
            for rec in rows_object:
                await session.delete(rec)
            await session.commit()

    async def delete_rows(self, model: Any, **filter_by):
        async with self.async_ses() as session:
            records = await session.execute(Query(model).filter_by(**filter_by))
            res = records.scalars()
            if res:
                try:
                    for rec in res:
                        await session.delete(rec)
                    await session.commit()
                    return True
                except Exception:
                    pass

    async def get_all_set(self, table_model, field) -> set:
        """
        Метод принимает класс модели и название поля,
        и возвращает множество всех полученных значений.
        :param table_model: Класс модели
        :param field: Название поля
        :return: set
        """
        async with self.async_ses() as session:
            rows = await session.execute(Select(table_model.__table__.c[field]))
            return {row for row in rows.scalars()}

    async def drop_tables(self, table_models: Iterable):
        """
        Метод принимает коллекцию классов моделей и удаляет данные таблицы из БД.
        :param table_models:
        :return:
        """
        async with self.async_ses() as session:
            for table in table_models:
                await session.execute(DropTable(table.__table__))
                logger.info(f'{table.__tablename__} is dropped')
            await session.commit()

    async def add_row(self, model: Any, **kwargs):
        """
        Метод принимает класс модели и поля со значениями,
        и создает в таблице данной модели запись с переданными аргументами.
        :param model: Класс модели
        :param kwargs: Поля и их значения
        :return:
        """

        async with self.async_ses() as session:
            row = model(**kwargs)
            session.add(row)
            try:
                await session.commit()
                return row
            except Exception as ex:
                logger.exception(ex)
                logger.warning(f'FAILED ADD ROW, {model.__name__}, {kwargs=}')
                return


    async def get_row(self, model: Any, to_many=False, order_by='id', filter=None, **kwargs):
        """
        Метод принимает класс модели и имена полей со значениями,
        и если такая строка есть в БД - возвращает ее.
        :param to_many: Флаг для возврата одного или нескольких значений
        :param model: Класс модели
        :param kwargs: Поля и их значения
        :return:
        """
        async with self.async_ses() as session:
            if filter:
                row = await session.execute(
                    Query(model).filter_by(**kwargs).filter(filter['filter']).order_by(order_by))
            else:
                row = await session.execute(Query(model).filter_by(**kwargs).order_by(order_by))
            if to_many:
                res = [*row.scalars()]
            else:
                res = row.scalar()
            return res

    async def get_or_create_row(self, model: Any, filter_by=None, **kwargs):
        """
        Метод находит в БД запись, и возвращает ее. Если записи нет - создает и возвращает.
        :param model: Класс модели
        :param filter_by: Параметры для поиска записи. По умолчанию поиск идет по **kwargs
        :param kwargs: Поля и их значения
        :return:
        """
        if not filter_by:
            filter_by = kwargs

        async with self.async_ses() as session:
            row = await session.execute(Query(model).filter_by(**filter_by))
            res = row.scalar()
            if res is None:
                res = model(**kwargs)
                session.add(res)
                try:
                    await session.commit()
                except Exception as ex:
                    logger.warning(f'COMMIT FAILED: {model.__name__}, {kwargs=}')
            return res

    async def update_user_row(self, model, tg_user_id, **kwargs):

        async with self.async_ses() as session:
            row = await session.execute(update(model).where(Users.tg_user_id == str(tg_user_id )).values(**kwargs))

            try:
                await session.commit()
            except Exception as ex:
                print(ex)
                print(f'failed update {model.__tablename__}')


    async def get_user_tags(self, model: Any=Users, to_many=False, order_by='id', filter=None, **kwargs):
        """
        Метод принимает класс модели и имена полей со значениями,
        и если такая строка есть в БД - возвращает ее.
        :param to_many: Флаг для возврата одного или нескольких значений
        :param model: Класс модели
        :param kwargs: Поля и их значения
        :return:
        """
        async with self.async_ses() as session:
            if filter:
                row = await session.execute(
                    Query(model).filter_by(**kwargs).filter(filter['filter']).order_by(order_by))
            else:
                row = await session.execute(Query(model).filter_by(**kwargs).order_by(order_by))
            if to_many:
                res = [*row.scalars()]
            else:
                res = row.scalar()
            return res

    async def update_data_user(self, model, usr_id):
        """
        Метод для изменения полей в таблице Users
        :return:
        """
        async with self.async_ses() as session:
            try:
                await session.commit()
                logger.debug(f'Successfully update data user {usr_id}')
            except Exception as ex:
                print(ex)
                print(f'failed update {model.__tablename__}')

    async def add_rows(self, lst: List):
        """
        Метод принимает класс модели и поля со значениями,
        и создает в таблице данной модели запись с переданными аргументами.
        :param lst: Список
        :return:
        """
        async with self.async_ses() as session:
            async with session.begin():
                session.add_all(lst)
            try:
                await session.commit()
                logger.info('Add new row')
            except Exception as exc:
                logger.exception(exc)


    async def get_users_info(self, model: Any=Users, to_many: bool=True):
        async with self.async_ses() as session:
            row_mans = await session.execute(Query(model).filter_by(sex='man'))
            row_girls = await session.execute(Query(model).filter_by(sex='woman'))
            row_users = await session.execute(Query(model).filter_by())
            row_users_nodone_profile = await session.execute(Query(model).filter_by(done_questionnaire=False))
            if to_many:
                res = [len([*row_mans.scalars()]), len([*row_girls.scalars()]),
                       len([*row_users]), len([*row_users_nodone_profile])]
            return res
