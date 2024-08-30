import cProfile
import pstats
import run as _run

if __name__ == "__main__":
    with cProfile.Profile() as profile:
        _run.background_task()

    results = pstats.Stats(profile)
    results.sort_stats(pstats.SortKey.TIME)
    results.print_stats()
    results.dump_stats("assets/benchmark_result.prof")
