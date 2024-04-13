import numpy as np
from collections import defaultdict
import aiofiles


async def write_to_files(file_name, content):
    async with aiofiles.open("analysis/output/" + file_name, "w") as f:
        await f.write('\n'.join(content))


async def average_rank(lists):
    # Create a dictionary to store the ranks
    rank_dict = {el: [] for lst in lists for el in lst}

    # Assign ranks
    for lst in lists:
        for rank, el in enumerate(lst, start=1):
            rank_dict[el].append(rank)

    # Calculate average ranks
    avg_ranks = {el: np.mean(ranks) for el, ranks in rank_dict.items()}

    # Create a new list sorted by average rank
    new_list = sorted(avg_ranks, key=avg_ranks.get)
    await write_to_files("average_rank.txt", new_list)

    return new_list


async def combined_ranks_unweighted(lists):
    # Create a dictionary to hold the total points for each item
    points = defaultdict(int)

    # Calculate the points for each item
    for lst in lists:
        for i, item in enumerate(reversed(lst)):
            points[item] += i + 1

    # Create the combined list
    combined_list = sorted(points, key=points.get, reverse=True)
    await write_to_files('combined_ranks_unweighted.txt', combined_list)
    return combined_list


async def combined_ranks_weighted(lists, imdb_score_data):
    # Create a dictionary to hold the total points for each item
    points = defaultdict(int)

    # Calculate the points for each item
    for lst in lists:
        for i, item in enumerate(reversed(lst)):
            points[item] += i + 1

    for t in imdb_score_data:
        points[t[0]] *= (lambda x: x if x else 1)(t[1])

    # Create the combined list
    combined_list = sorted(points, key=points.get, reverse=True)
    await write_to_files('combined_ranks_weighted.txt', combined_list)
    return combined_list
