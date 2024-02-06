import charts
import GetBenchmarkData
import multiprocessing


def make_charts():
    print("Starting to make charts...")
    data = GetBenchmarkData.get_benchmark_data()
    for key in data:
        process = multiprocessing.Process(target=charts.make_chart, args=(data[key], key, len(data[key])))
        process.start()
    print("Finished")
make_charts()


