import psycopg
import asyncio
from icecream import ic
from fetch_sql import get_all_imdb_score_data, get_all_sortings, get_international_imdb_score_data, get_international_sortings, get_hindi_list
from compute_lists import average_rank, combined_ranks_unweighted, combined_ranks_weighted


async def main():

    async with await psycopg.AsyncConnection.connect(host="localhost", dbname="postgres", user="rohits") as aconn:

        acur1 = aconn.cursor()
        acur2 = aconn.cursor()
        acur3 = aconn.cursor()
        acur4 = aconn.cursor()
        acur5 = aconn.cursor()

        all_sortings, all_imdb_score, international_sortings, international_imdb_score, hindi_list = await asyncio.gather(get_all_sortings(acur1), get_all_imdb_score_data(acur2), get_international_sortings(acur3), get_international_imdb_score_data(acur4), get_hindi_list(acur5))

        async with asyncio.TaskGroup() as tg:

            tg.create_task(average_rank(
                "analysis/output/", all_sortings, hindi_list))
            tg.create_task(combined_ranks_unweighted(
                "analysis/output/", all_sortings, hindi_list))
            tg.create_task(combined_ranks_weighted(
                "analysis/output/", all_sortings, all_imdb_score, hindi_list))

            tg.create_task(average_rank(
                "analysis/output/international_", international_sortings, hindi_list))
            tg.create_task(combined_ranks_unweighted(
                "analysis/output/international_", international_sortings, hindi_list))
            tg.create_task(combined_ranks_weighted(
                "analysis/output/international_", international_sortings, international_imdb_score, hindi_list))

        async with asyncio.TaskGroup() as tg:
            tg.create_task(acur1.close())
            tg.create_task(acur2.close())
            tg.create_task(acur3.close())
            tg.create_task(acur4.close())

    print("Done")

asyncio.run(main())
