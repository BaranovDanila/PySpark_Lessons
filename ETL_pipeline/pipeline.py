import pyspark.sql.functions as F
import pyspark.sql.types as t

from pyspark.sql import SparkSession, DataFrame


def extract_data(spark: SparkSession) -> DataFrame:
    path = 'data/cars.csv'
    return spark.read.option('header', 'true').csv(path)


def transform_data(df: DataFrame) -> DataFrame:
    '''
    Make some aggregations with input DataFrame.
    Return DataFrame representing
    amount info, min / max / avg price in USD, average produced year for each manufacturer.
    '''

    output_df = (
        df.groupby('manufacturer_name').
        agg(
            F.count('manufacturer_name').alias('count_ads'),
            F.round(F.avg('year_produced')).cast(t.IntegerType()).alias('avg_year_produced'),
            F.min('price_usd').alias('min_price'),
            F.max('price_usd').alias('max_price'),
            F.round(F.avg('price_usd'), 2).alias('avg_price')
        )
    )
    return output_df


def save_data(df: DataFrame) -> None:
    df.coalesce(4).write.mode('overwrite').format('json').save('output.json')


def main():
    spark = SparkSession.builder.appName('ETL').getOrCreate()
    df = extract_data(spark=spark)
    output_df = transform_data(df)
    save_data(output_df)


if __name__ == '__main__':
    main()
