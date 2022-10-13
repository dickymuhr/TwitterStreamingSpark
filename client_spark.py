from __future__ import print_function
from pyspark import SparkContext
from pyspark.streaming import StreamingContext

sc = SparkContext(appName="StreamingTwitterAnalysis")
sc.setLogLevel("ERROR")
ssc = StreamingContext(sc,600)

socket_stream = ssc.socketTextStream("127.0.0.1", 9091)
lines = socket_stream.window(3600)
hashtags = lines.flatMap(lambda text: text.split(" ")).filter(lambda word: word.lower().startswith('#'))
hashtags_tuple = hashtags.map(lambda word:(word.lower(),1) ).reduceByKey(lambda a,b:a+b)
hashtags_counts_sorted_dstream = hashtags_tuple.transform(lambda foo:foo.sortBy(lambda x:x[0].lower()).sortBy(lambda x:x[1], ascending=False))

hashtags_counts_sorted_dstream.pprint()

ssc.start()
ssc.awaitTermination()