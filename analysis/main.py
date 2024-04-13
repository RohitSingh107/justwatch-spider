

import psycopg
import asyncio

from fetch_sql import get_all_imdb_score_data, get_all_sortings
from compute_lists import average_rank, combined_ranks_unweighted, combined_ranks_weighted



async def main():

    async with await psycopg.AsyncConnection.connect(host="localhost", dbname="postgres", user="rohits") as aconn:
        async with aconn.cursor() as acur:

            all_sortings, all_imdb_score = await asyncio.gather(get_all_sortings(acur), get_all_imdb_score_data(acur))

            async with asyncio.TaskGroup() as tg:
                tg.create_task(average_rank(all_sortings))
                tg.create_task(combined_ranks_unweighted(all_sortings))
                tg.create_task(combined_ranks_weighted(all_sortings, all_imdb_score))

    print("Done")



asyncio.run(main())
