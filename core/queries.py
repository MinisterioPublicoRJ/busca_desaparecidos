QUERY_ALL_PERSONS = """
select SNCA_DT_FATO, BAIR_LATITUDE, BAIR_LONGITUDE, BAIR_NM_BAIRRO,
CASE
        WHEN CIDA_LATITUDE IS NULL THEN
        (SELECT CIDA_LATITUDE FROM CORP.CORP_CIDADE WHERE CIDA_DK = BAIR_CIDA_DK)
        ELSE CIDA_LATITUDE END CIDA_LATITUDE,
CASE
        WHEN CIDA_LONGITUDE IS NULL THEN
        (SELECT CIDA_LONGITUDE FROM CORP.CORP_CIDADE WHERE CIDA_DK = BAIR_CIDA_DK)
        ELSE CIDA_LONGITUDE END CIDA_LONGITUDE,
CASE
        WHEN CIDA_NM_CIDADE IS NULL THEN
        (SELECT CIDA_NM_CIDADE FROM CORP.CORP_CIDADE WHERE CIDA_DK = BAIR_CIDA_DK)
        ELSE CIDA_NM_CIDADE END CIDA_NM_CIDADE,
SNCA_IDENTIFICADOR_SINALID
from SILD_SINDICANCIA
LEFT JOIN SILD_ENDERECO_FATO ON SILD_SINDICANCIA.SNCA_DK = SILD_ENDERECO_FATO.SIES_DK
LEFT JOIN CORP.CORP_CIDADE ON SILD_ENDERECO_FATO.SIES_CIDA_DK = CORP.CORP_CIDADE.CIDA_DK
LEFT JOIN CORP.CORP_BAIRRO ON SILD_ENDERECO_FATO.SIES_BAIR_DK = CORP.CORP_BAIRRO.BAIR_DK
"""

QUERY_SINGLE_TARGET = QUERY_ALL_PERSONS + " WHERE SNCA_IDENTIFICADOR_SINALID = '{id}'"
