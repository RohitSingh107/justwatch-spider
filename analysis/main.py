

import psycopg
import asyncio
import sys

from fetch_sql import get_all_imdb_score_data, get_all_sortings, get_international_imdb_score_data, get_international_sortings
from compute_lists import average_rank, combined_ranks_unweighted, combined_ranks_weighted



async def main():

    async with await psycopg.AsyncConnection.connect(host="localhost", dbname="postgres", user="rohits") as aconn:
        async with aconn.cursor() as acur:

            if len(sys.argv) > 1 and sys.argv[1] == "international":
                all_sortings, all_imdb_score = await asyncio.gather(get_international_sortings(acur), get_international_imdb_score_data(acur))
            else:
                all_sortings, all_imdb_score = await asyncio.gather(get_all_sortings(acur), get_all_imdb_score_data(acur))

            async with asyncio.TaskGroup() as tg:

                tg.create_task(average_rank("analysis/output/", all_sortings))
                tg.create_task(combined_ranks_unweighted("analysis/output/" , all_sortings))
                tg.create_task(combined_ranks_weighted("analysis/output/", all_sortings, all_imdb_score))

    print("Done")



asyncio.run(main())
