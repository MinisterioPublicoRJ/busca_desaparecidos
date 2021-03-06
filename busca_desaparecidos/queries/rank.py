query = """WITH 
SID_IDADE_APARENTE AS (
SELECT SIDP_DK,  
	CAST(NVL(SUBSTR(SIDP_NM_IDADE_APARENTE, 1, INSTR(SIDP_NM_IDADE_APARENTE, '-')-1), 1) AS INT) AS INICIO,
    CAST(REPLACE(REPLACE(SUBSTR(SIDP_NM_IDADE_APARENTE, INSTR(SIDP_NM_IDADE_APARENTE, '-')+1), '>',''), '<','') AS INT) AS FIM
FROM SILD.SILD_IDADE_APARENTE
WHERE SILD_IDADE_APARENTE.SIDP_DK <> 19
),
PESSOAS_POSSIVEIS AS (
	SELECT
    VTMA_DT_NASCIMENTO,
    FLOOR(MONTHS_BETWEEN(SNCA_DT_FATO, SILD_VITIMA.VTMA_DT_NASCIMENTO) / 12) IDADE,
    VTMA_IN_SEXO,
    CASE 
    	WHEN SNCA_DT_FATO < to_date('1900-01-01', 'yyyy-mm-dd') THEN to_date('1900-01-01', 'yyyy-mm-dd')
    	ELSE SNCA_DT_FATO
    END SNCA_DT_FATO,
    BAIR_LATITUDE,
    BAIR_LONGITUDE,
    BAIR_NM_BAIRRO,
    VTMA_SIDP_DK,
    CASE 
		WHEN VTMA_DT_NASCIMENTO IS NULL AND VTMA_SIDP_DK IS NULL THEN NULL
		WHEN VTMA_DT_NASCIMENTO IS NOT NULL THEN (
			SELECT MAX(SIDP_DK) 
			FROM 
			SID_IDADE_APARENTE
			WHERE CAST(ABS(SNCA_DT_FATO - VTMA_DT_NASCIMENTO)/365.2425 AS INT)
				BETWEEN SID_IDADE_APARENTE.INICIO AND SID_IDADE_APARENTE.FIM
		)
		ELSE
			VTMA_SIDP_DK
    END IDADE_APARENTE_PESSOA,
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
	FROM SILD_SINDICANCIA
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
),
SCORES AS (
	SELECT ALVO.SNCA_IDENTIFICADOR_SINALID AS SNCA_IDENTIFICADOR_ALVO,
	TODOMUNDO.SNCA_IDENTIFICADOR_SINALID AS SNCA_IDENTIFICADOR_TODOMUNDO,
	TODOMUNDO.VTMA_DT_NASCIMENTO,
	CASE 
		WHEN ALVO.VTMA_IN_SEXO IS NULL THEN 0.01
		WHEN TODOMUNDO.VTMA_IN_SEXO IS NULL THEN 0.5
		WHEN ALVO.VTMA_IN_SEXO = TODOMUNDO.VTMA_IN_SEXO THEN 0.01
		WHEN ALVO.VTMA_IN_SEXO <> TODOMUNDO.VTMA_IN_SEXO THEN 1
	END SEX_SCORE,
	CASE
		WHEN ALVO.SNCA_DT_FATO IS NOT NULL AND TODOMUNDO.SNCA_DT_FATO IS NOT NULL THEN
			trunc(ABS(ALVO.SNCA_DT_FATO - TODOMUNDO.SNCA_DT_FATO))
		ELSE null
	END DATE_SCORE,
	CASE 
		WHEN ALVO.VTMA_DT_NASCIMENTO IS NULL AND ALVO.VTMA_SIDP_DK IS NULL THEN 19
		WHEN TODOMUNDO.VTMA_DT_NASCIMENTO IS NULL AND TODOMUNDO.VTMA_SIDP_DK IS NULL THEN 19
		ELSE
			ABS((
				SELECT MAX(SIDP_DK) 
				FROM 
				SID_IDADE_APARENTE
				WHERE CAST(ABS(TODOMUNDO.SNCA_DT_FATO - ALVO.VTMA_DT_NASCIMENTO)/365.2425 AS INT)
					BETWEEN SID_IDADE_APARENTE.INICIO AND SID_IDADE_APARENTE.FIM
			) - TODOMUNDO.IDADE_APARENTE_PESSOA)
	END DIFERENCA_IDADE_APARENTE,
	CASE
		WHEN alvo.bair_latitude IS NULL AND alvo.cida_latitude IS NULL THEN 0.0
		WHEN todomundo.bair_latitude IS NULL AND todomundo.cida_latitude IS NULL THEN null
		else
		SQRT(
			POWER(
				NVL(ALVO.BAIR_LATITUDE, ALVO.CIDA_LATITUDE)
						-
				NVL(TODOMUNDO.BAIR_LATITUDE, TODOMUNDO.CIDA_LATITUDE), 
					2) + 
			POWER(
				NVL(ALVO.BAIR_LONGITUDE, ALVO.CIDA_LONGITUDE) 
						- 
				NVL(TODOMUNDO.BAIR_LONGITUDE, TODOMUNDO.CIDA_LONGITUDE), 
					2)
		)
	END DISTANCIA
	FROM PESSOAS_POSSIVEIS TODOMUNDO
	INNER JOIN PESSOAS_POSSIVEIS ALVO ON 1=1
	WHERE ALVO.SNCA_IDENTIFICADOR_SINALID = '{{ id_sinalid }}'
),
nulospreenchidos AS (
	SELECT 
		SNCA_IDENTIFICADOR_ALVO,
		SNCA_IDENTIFICADOR_TODOMUNDO,
		VTMA_DT_NASCIMENTO,
		nvl(SEX_SCORE, 
			(SELECT max(sex_score) FROM SCORES)+1) AS SEX_SCORE,
		nvl(DATE_SCORE, 
			(SELECT max(DATE_SCORE) FROM SCORES)+1) AS DATE_SCORE,
		nvl(DIFERENCA_IDADE_APARENTE, 
			(SELECT max(DIFERENCA_IDADE_APARENTE) FROM SCORES)+1) AS DIFERENCA_IDADE_APARENTE,
		nvl(DISTANCIA, 
			(SELECT max(DISTANCIA) FROM SCORES)+1) AS DISTANCIA
	FROM SCORES
),
maximos AS (
	SELECT 
		SNCA_IDENTIFICADOR_ALVO,
		SNCA_IDENTIFICADOR_TODOMUNDO,
		VTMA_DT_NASCIMENTO,
		SEX_SCORE,
		DATE_SCORE,
		DIFERENCA_IDADE_APARENTE,
		DISTANCIA,
		(SELECT max(sex_score) FROM nulospreenchidos) M_SEX_SCORE,
		(SELECT max(DATE_SCORE) FROM nulospreenchidos) M_DATE_SCORE,
		(SELECT max(DIFERENCA_IDADE_APARENTE) FROM nulospreenchidos) M_DIFERENCA_IDADE_APARENTE,
		(SELECT max(DISTANCIA) FROM nulospreenchidos) M_DISTANCIA
	FROM nulospreenchidos
),
normalizada AS (
	SELECT 
		SNCA_IDENTIFICADOR_ALVO,
		SNCA_IDENTIFICADOR_TODOMUNDO,
		VTMA_DT_NASCIMENTO,
		SEX_SCORE,
		SEX_SCORE/M_SEX_SCORE AS N_SEX_SCORE,
		DATE_SCORE,
		DATE_SCORE/M_DATE_SCORE AS N_DATE_SCORE,
		DIFERENCA_IDADE_APARENTE,
		DIFERENCA_IDADE_APARENTE/M_DIFERENCA_IDADE_APARENTE AS N_DIFERENCA_IDADE_APARENTE,
		DISTANCIA,
		DISTANCIA/M_DISTANCIA AS N_DISTANCIA
	FROM maximos
	GROUP BY 
		SNCA_IDENTIFICADOR_ALVO,
		SNCA_IDENTIFICADOR_TODOMUNDO,
		VTMA_DT_NASCIMENTO,
		SEX_SCORE,
		DATE_SCORE,
		DIFERENCA_IDADE_APARENTE,
		DISTANCIA,
		M_SEX_SCORE,
		M_DATE_SCORE,
		M_DIFERENCA_IDADE_APARENTE,
		M_DISTANCIA
		
)
SELECT
	SNCA_IDENTIFICADOR_ALVO,
	SNCA_IDENTIFICADOR_TODOMUNDO,
	VTMA_DT_NASCIMENTO,
	N_SEX_SCORE,
	N_DATE_SCORE,
	N_DIFERENCA_IDADE_APARENTE,
	N_DISTANCIA,
	N_SEX_SCORE+N_DATE_SCORE+N_DIFERENCA_IDADE_APARENTE+N_DISTANCIA AS SOMA
FROM normalizada
ORDER BY N_SEX_SCORE+N_DATE_SCORE+N_DIFERENCA_IDADE_APARENTE+N_DISTANCIA
"""
