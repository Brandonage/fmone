# fmone

FMonE is a lightweight monitoring tool that has been conceived for use in a Fog or Edge computing environment. It is designed to run as a Docker container.

`~$ docker run -v /var/run/docker.sock:/var/run/docker.sock -v /proc:/proc_host fmone-agent 1 1 host inout console`

It can also be run as a normal python process.

`~$ python fmone/fmonitor/fmone-agent.py 1 1 host inout console`

Some dependencies need to be installed first in this case:
* psutil
* pika
* pymongo
* docker
* kafka-python

For the list of the different parameters please read the documentation on the [Docker Hub](https://hub.docker.com/r/alvarobrandon/fmone-agent/)

Some examples of running fmone are.

* The simplest way. Monitor the metrics of the host and print them through the console. Note how we do not need any additional parameters:
`~$ python fmone/fmonitor/fmone-agent.py 1 1 host inout console`

* Monitor every second the docker containers running on the host, don't filter the metrics and publish them to a RabbitMQ container that has a hostname "my-rabbit" with a routing key "region"
`~$ python fmone/fmonitor/fmone-agent.py 1 1 docker inout rabbitmq --mq_machine_out my-rabbit:5672 --routing_key_out region`

* Pull out every second the metrics from the RabbitMQ container and calculate the average plus store it in a MongoDB in collection regionmetrics every 5 seconds:
`~$ python fmone/fmonitor/fmone-agent.py 1 5 rabbitmq average mongodb --mq_machine_in my-rabbit:5672 --routing_key_in regional --mongo_machine_out my-mongo --mongo_collection_out regionmetrics`

