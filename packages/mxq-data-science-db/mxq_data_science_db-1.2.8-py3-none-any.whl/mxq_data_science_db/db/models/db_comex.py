"""SQL models for db_comex
"""
from datetime import datetime
import logging

import pandas as pd
from sqlalchemy import delete

from sqlalchemy.ext.declarative import declarative_base
import sqlalchemy as sa

from mxq_data_science_db.db.db import SQLConnection
from mxq_data_science_db.db.models.base import BaseModel

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

Base = declarative_base()
metadata = Base.metadata


class NCM(Base, BaseModel):
    """Table with NCMs data"""

    __tablename__ = "ncm"
    ncm = sa.Column(sa.String(20), primary_key=True)
    pais = sa.Column(sa.String(2), primary_key=True)
    classificacao = sa.Column(sa.String(50), primary_key=True)
    descricao = sa.Column(sa.String(300), primary_key=True)
    material = sa.Column(sa.String(30), primary_key=True)
    parte = sa.Column(sa.Integer())
    multiplicador = sa.Column(sa.Float())


class MMIComexBRProcessed(Base, BaseModel):
    """Table for processed data for MMI BR"""

    __tablename__ = "mmi_comex_br_processed"
    ncm = sa.Column(sa.String(10), primary_key=True)
    fluxo = sa.Column(sa.String(3), primary_key=True)
    data = sa.Column(sa.DATETIME(), primary_key=True)
    ano = sa.Column(sa.Integer(), primary_key=True)
    mes = sa.Column(sa.Integer(), primary_key=True)
    pais = sa.Column(sa.String(2), primary_key=True)
    uf = sa.Column(sa.String(2), primary_key=True)
    via = sa.Column(sa.String(30), primary_key=True)
    urf = sa.Column(sa.String(80), primary_key=True)
    resina = sa.Column(sa.String(10), primary_key=True)
    kg_liquido = sa.Column(sa.Float())
    vl_fob = sa.Column(sa.Float())
    updated_at = sa.Column(
        sa.DATETIME(), nullable=False, default=sa.text("CURRENT_TIMESTAMP")
    )
    sa.Index("mmi_comex_br_processed_data_IDX", data, fluxo, resina)
    sa.Index("mmi_comex_br_processed_data_pais_IDX", data, fluxo, pais, resina)

    @classmethod
    def delete_before_insert(cls, df: pd.DataFrame):
        """Delete all records for the years in the DF

        Args:
            df (pd.DataFrame): dataframe
        """
        list_ano = list(set(df[cls.ano.name]))

        assert len(list_ano) != 0, "No year set"
        assert len(list_ano) == 1, "Only one year can be updated per time"

        ano = list_ano[0]

        with SQLConnection() as con:
            logger.info(f"Delete before upsert, ano={ano}")
            stmt = delete(cls).where(cls.ano == ano)
            con.execute(stmt)

        cls.bulk_upsert(df, chuck_size=10**4)


class MMOComexProcessed(Base, BaseModel):
    """Table for processed data for MMO"""

    __tablename__ = "mmo_comex_processed"
    data = sa.Column(sa.DATETIME(), primary_key=True)
    ano = sa.Column(sa.Integer(), primary_key=True)
    mes = sa.Column(sa.Integer(), primary_key=True)
    fluxo = sa.Column(sa.String(3), primary_key=True)
    pais_origem = sa.Column(sa.String(2), primary_key=True)
    pais_destino = sa.Column(sa.String(2), primary_key=True)
    pais_relatorio = sa.Column(sa.String(2), primary_key=True)
    ncm_relatorio = sa.Column(sa.String(20), primary_key=True)
    resina = sa.Column(sa.String(10), primary_key=True)
    peso_kg = sa.Column(sa.Float())
    fob_usd = sa.Column(sa.Float())
    updated_at = sa.Column(
        sa.DATETIME(), nullable=False, default=sa.text("CURRENT_TIMESTAMP")
    )

    @classmethod
    def delete_before_insert(cls, df: pd.DataFrame):
        """Delete all records for the years in the DF

        Args:
            df (pd.DataFrame): dataframe
        """
        # Check ano
        list_ano = list(set(df[cls.ano.name]))

        assert len(list_ano) != 0, "No year set"
        assert len(list_ano) == 1, "Only one year can be updated per time"

        # Check pais relatorio
        list_pais = list(set(df[cls.pais_relatorio.name]))

        assert len(list_pais) != 0, "No pais_relatorio set"
        assert len(list_pais) == 1, "Only pais_relatorio can be updated per time"

        # Check ncm
        list_ncm = list(set(df[cls.ncm_relatorio.name]))

        assert len(list_ncm) != 0, "No ncm_relatorio set"
        assert len(list_ncm) == 1, "Only one ncm_relatorio can be updated per time"

        ano = list_ano[0]
        pais_relatorio = list_pais[0]
        ncm_relatorio = list_ncm[0]

        with SQLConnection() as con:
            logger.info(
                f"Delete before upsert, ano={ano}, pais_relatorio={pais_relatorio}, ncm_relatorio={ncm_relatorio}"
            )
            stmt = delete(cls).where(
                cls.ano == ano,
                cls.pais_relatorio == pais_relatorio,
                cls.ncm_relatorio == ncm_relatorio,
            )
            con.execute(stmt)

        cls.bulk_upsert(df, chuck_size=10**4)
