QUERY_ALL_PERSONS = """
SELECT
    VTMA_DT_NASCIMENTO,
    floor(MONTHS_BETWEEN(CURRENT_DATE, SILD_VITIMA.VTMA_DT_NASCIMENTO) / 12) IDADE,
    VTMA_IN_SEXO,
    BDMT_BASE64,
    SNCA_DT_FATO,
    BAIR_LATITUDE,
    BAIR_LONGITUDE,
    BAIR_NM_BAIRRO, 
    CASE
    WHEN floor(MONTHS_BETWEEN(CURRENT_DATE, SILD_VITIMA.VTMA_DT_NASCIMENTO) / 12) IS NULL THEN
    (SELECT SIDP_NM_IDADE_APARENTE FROM SILD.SILD_IDADE_APARENTE WHERE SIDP_DK = VTMA_SIDP_DK)
        ELSE NULL
    END IDADE_APARENTE,
    CASE
        WHEN floor(MONTHS_BETWEEN(CURRENT_DATE, SILD_VITIMA.VTMA_DT_NASCIMENTO) / 12) IS NULL THEN
        (SELECT SIDP_DK FROM SILD.SILD_IDADE_APARENTE WHERE SIDP_DK = VTMA_SIDP_DK)
            ELSE NULL
     END INDICE_IDADE_APARENTE,
    CASE
        WHEN CIDA_LATITUDE IS NULL THEN
        (SELECT CIDA_LATITUDE FROM CORP.CORP_CIDADE WHERE CIDA_DK = BAIR_CIDA_DK)
        ELSE CIDA_LATITUDE
    END CIDA_LATITUDE,
    CASE WHEN CIDA_LONGITUDE IS NULL THEN
    (SELECT CIDA_LONGITUDE FROM CORP.CORP_CIDADE WHERE CIDA_DK = BAIR_CIDA_DK)
        ELSE CIDA_LONGITUDE
    END CIDA_LONGITUDE,
    CASE
        WHEN CIDA_NM_CIDADE IS NULL THEN
        (SELECT CIDA_NM_CIDADE FROM CORP.CORP_CIDADE WHERE CIDA_DK = BAIR_CIDA_DK)
        ELSE CIDA_NM_CIDADE
    END CIDA_NM_CIDADE,
    SNCA_IDENTIFICADOR_SINALID
from SILD_SINDICANCIA
LEFT JOIN
    SILD_ENDERECO_FATO ON SILD_SINDICANCIA.SNCA_DK = SILD_ENDERECO_FATO.SIES_SNCA_DK 
LEFT JOIN
    CORP.CORP_CIDADE
ON SILD_ENDERECO_FATO.SIES_CIDA_DK = CORP.CORP_CIDADE.CIDA_DK 
LEFT JOIN
    CORP.CORP_BAIRRO
ON SILD_ENDERECO_FATO.SIES_BAIR_DK = CORP.CORP_BAIRRO.BAIR_DK 
LEFT JOIN
    SILD_DOCUMENTO
ON SILD_SINDICANCIA.SNCA_DK = SILD_DOCUMENTO.DMTO_SNCA_DK 
AND SILD_DOCUMENTO.DMTO_TDCT_DK = 5
LEFT JOIN
    SILD_BLOB_DOCUMENTO
ON SILD_DOCUMENTO.DMTO_DK = SILD_BLOB_DOCUMENTO.BDMT_DMTO_DK 
LEFT JOIN
    SILD_VITIMA
ON SILD_VITIMA.VTMA_DK = SILD_SINDICANCIA.SNCA_VTMA_DK
"""

QUERY_SINGLE_TARGET = QUERY_ALL_PERSONS + " WHERE SNCA_IDENTIFICADOR_SINALID = '{id}'"