# %%

import os
import dotenv
import nekt

dotenv.load_dotenv()

from tqdm import tqdm

# %%

nekt.data_access_token = os.getenv("NEKT_TOKEN")


# %%

# Custom imports
import nekt

query_dates = """
SELECT DISTINCT
	date(date) AS dt_ref
FROM
	f1_results
WHERE year(date) = '{year}'
ORDER BY
	1
"""

# Minha query de Feature Store
query = """

WITH
	results_until_date AS (
		SELECT
			*
		FROM
			f1_results
		WHERE
			date(date) <= date('{date}')
		ORDER BY
			date DESC
	),
	drivers_selected AS (
		SELECT DISTINCT
			driverid
		FROM
			results_until_date
		WHERE
			YEAR >= (
				SELECT
					MAX(YEAR) - 2
				FROM
					results_until_date
			)
	),
	tb_results AS (
		SELECT
			t1.*
		FROM
			results_until_date AS t1
			INNER JOIN drivers_selected AS t2 ON t1.driverid = t2.driverid
		ORDER BY
			YEAR
	),
	tb_life AS (
		SELECT
			driverid,
			count(DISTINCT YEAR) AS qtd_seasons,
			count(*) AS qtd_sessions,
			sum(
				CASE
					WHEN (
						status = 'Finished'
						OR status LIKE '+%'
					) THEN 1
					ELSE 0
				END
			) AS qtde_sessions_finished,
			sum(
				CASE
					WHEN mode = 'Race' THEN 1
					ELSE 0
				END
			) AS qtd_race,
			sum(
				CASE
					WHEN mode = 'Race'
					AND (
						status = 'Finished'
						OR status LIKE '+%'
					) THEN 1
					ELSE 0
				END
			) AS qtde_sessions_finished_race,
			sum(
				CASE
					WHEN mode = 'Sprint' THEN 1
					ELSE 0
				END
			) AS qtd_sprint,
			sum(
				CASE
					WHEN mode = 'Sprint'
					AND (
						status = 'Finished'
						OR status LIKE '+%'
					) THEN 1
					ELSE 0
				END
			) AS qtde_sessions_finished_sprint,
			sum(
				CASE
					WHEN POSITION = 1 THEN 1
					ELSE 0
				END
			) AS qtde_1Pos,
			sum(
				CASE
					WHEN POSITION = 1
					AND MODE = 'Race' THEN 1
					ELSE 0
				END
			) AS qtde_1Pos_race,
			sum(
				CASE
					WHEN POSITION = 1
					AND MODE = 'Sprint' THEN 1
					ELSE 0
				END
			) AS qtde_1Pos_sprint,
			sum(
				CASE
					WHEN POSITION <= 3 THEN 1
					ELSE 0
				END
			) AS qtde_podios,
			sum(
				CASE
					WHEN POSITION <= 3
					AND mode = 'Race' THEN 1
					ELSE 0
				END
			) AS qtde_podios_race,
			sum(
				CASE
					WHEN POSITION <= 3
					AND mode = 'Sprint' THEN 1
					ELSE 0
				END
			) AS qtde_podios_sprint,
			sum(
				CASE
					WHEN POSITION <= 5 THEN 1
					ELSE 0
				END
			) AS qtde_pos5,
			sum(
				CASE
					WHEN POSITION <= 5
					AND mode = 'Race' THEN 1
					ELSE 0
				END
			) AS qtde_pos5_race,
			sum(
				CASE
					WHEN POSITION <= 5
					AND mode = 'Sprint' THEN 1
					ELSE 0
				END
			) AS qtde_pos5_sprint,
			sum(
				CASE
					WHEN gridposition <= 5 THEN 1
					ELSE 0
				END
			) AS qtde_gridpos5,
			sum(
				CASE
					WHEN gridposition <= 5
					AND mode = 'Race' THEN 1
					ELSE 0
				END
			) AS qtde_gridpos5_race,
			sum(
				CASE
					WHEN gridposition <= 5
					AND mode = 'Sprint' THEN 1
					ELSE 0
				END
			) AS qtde_gridpos5_sprint,
			sum(points) AS qtde_points,
			sum(
				CASE
					WHEN mode = 'Race' THEN points
				END
			) AS qtde_points_race,
			sum(
				CASE
					WHEN mode = 'Sprint' THEN points
				END
			) AS qtde_points_sprint,
			avg(gridposition) AS avg_gridposition,
			avg(
				CASE
					WHEN mode = 'Race' THEN gridposition
				END
			) AS avg_gridposition_race,
			avg(
				CASE
					WHEN mode = 'Sprint' THEN gridposition
				END
			) AS avg_gridposition_sprint,
			avg(POSITION) AS avg_position,
			avg(
				CASE
					WHEN mode = 'Race' THEN POSITION
				END
			) AS avg_position_race,
			avg(
				CASE
					WHEN mode = 'Race' THEN POSITION
				END
			) AS avg_position_sprint,
			sum(
				CASE
					WHEN gridposition = 1 THEN 1
					ELSE 0
				END
			) AS qtde_1_gridposition,
			sum(
				CASE
					WHEN gridposition = 1
					AND mode = 'Race' THEN 1
					ELSE 0
				END
			) AS qtde_1_gridposition_race,
			sum(
				CASE
					WHEN gridposition = 1
					AND mode = 'Sprint' THEN 1
					ELSE 0
				END
			) AS qtde_1_gridposition_sprint,
			sum(
				CASE
					WHEN gridposition = 1
					AND POSITION = 1 THEN 1
					ELSE 0
				END
			) AS qtde_pole_win,
			sum(
				CASE
					WHEN gridposition = 1
					AND POSITION = 1
					AND mode = 'Race' THEN 1
					ELSE 0
				END
			) AS qtde_pole_win_race,
			sum(
				CASE
					WHEN gridposition = 1
					AND POSITION = 1
					AND mode = 'Sprint' THEN 1
					ELSE 0
				END
			) AS qtde_pole_win_sprint,
			sum(
				CASE
					WHEN points > 0 THEN 1
					ELSE 0
				END
			) AS qtd_sessions_with_points,
			sum(
				CASE
					WHEN mode = 'Race'
					AND points > 0 THEN 1
					ELSE 0
				END
			) AS qtd_sessions_with_points_race,
			sum(
				CASE
					WHEN mode = 'Sprint'
					AND points > 0 THEN 1
					ELSE 0
				END
			) AS qtd_sessions_with_points_sprint,
			sum(
				CASE
					WHEN POSITION < gridPOSITION THEN 1
					ELSE 0
				END
			) AS qtde_sessions_with_overtake,
			sum(
				CASE
					WHEN mode = 'Race'
					AND POSITION < gridPOSITION THEN 1
					ELSE 0
				END
			) AS qtde_sessions_with_overtake_race,
			sum(
				CASE
					WHEN mode = 'Sprint'
					AND POSITION < gridPOSITION THEN 1
					ELSE 0
				END
			) AS qtde_sessions_with_overtake_sprint,
			avg(gridPOSITION - POSITION) AS avg_overtake,
			avg(
				CASE
					WHEN mode = 'Race' THEN gridPOSITION - POSITION
				END
			) AS avg_overtake_race,
			avg(
				CASE
					WHEN mode = 'Sprint' THEN gridPOSITION - POSITION
				END
			) AS avg_overtake_sprint
		FROM
			tb_results
		GROUP BY
			driverid
	)
SELECT
	date('{date}') AS dt_ref,
	*
FROM
	tb_life
ORDER BY
	driverid

"""

# Carregamento das tabelas necessárias para a query
(nekt.load_table(layer_name="Bronze", table_name="f1_results")
     .createOrReplaceTempView("f1_results"))


# Sessão spark
spark = nekt.get_spark_session()

years = list(range(1991, 2025))

for y in years:

	dates = (spark.sql(query_dates.format(year=y))
		  		  .toPandas()["dt_ref"]
				  .astype(str)
				  .tolist())
	
	df_all = spark.sql(query.format(date=dates.pop(0)))

	for dt in tqdm(dates):
		df_all=df_all.union(spark.sql(query.format(date=dt)))

	# Salva dataframe resultante da query
	nekt.save_table(
			df=df_all,
			layer_name="Silver",
			table_name="fs_f1_driver_life",
			folder_name="f1",
	)

	del(df_all)


# %%


# %%
