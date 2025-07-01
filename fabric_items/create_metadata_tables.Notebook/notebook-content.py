# Fabric notebook source

# METADATA ********************

# META {
# META   "kernel_info": {
# META     "name": "synapse_pyspark"
# META   },
# META   "dependencies": {}
# META }

# MARKDOWN ********************

# # Create Metadata Tables
# - shortcut_table

# PARAMETERS CELL ********************

metadata_lh_abfs_table_path = ''

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

from pyspark.sql.types import StructType, StructField, StringType


# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************


shortcut_table_csv_data = """
healthdata,Files,AdlsGen2,1f126619-984e-4ab2-b5fa-42d5680242f7,https://healthsaadlsrheus.dfs.core.windows.net,/healthdata,Folder
dicom,Files,AdlsGen2,1f126619-984e-4ab2-b5fa-42d5680242f7,https://healthsaadlsrheus.dfs.core.windows.net,/dicom,Folder
"""


shortcut_table_schema = StructType([
    StructField("name", StringType(), True),
    StructField("shortcut_location", StringType(), True),
    StructField("target_type", StringType(), True),
    StructField("target_connection_id", StringType(), True),
    StructField("target_location", StringType(), True),
    StructField("target_subpath", StringType(), True),
    StructField("data_type", StringType(), True)
])


data_rows = [row.split(",") for row in shortcut_table_csv_data.strip().split("\n")]



# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

shortcut_df = spark.createDataFrame(data_rows, schema=shortcut_table_schema)



# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

display(shortcut_df)

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

shortcut_df.write.mode('overwrite').save(f'{metadata_lh_abfs_table_path}/shortcut_table')

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************


# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }
