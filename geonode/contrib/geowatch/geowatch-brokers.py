from multiprocessing import Process, cpu_count
# from multiprocessing import Lock, Queue

from geowatchutil.runtime import provision_brokers

from django.conf import settings


def run(broker):
    broker.run()

verbose = True
brokers = provision_brokers(
    settings.GEOWATCH_BROKERS_CRON,
    globalconfig=settings.GEOWATCH_CONFIG)

if not brokers:
    print "Could not provision brokers."
else:
    print str(cpu_count())+" CPUs are available."
    processes = []
    processID = 1
    for broker in brokers:
        process = Process(target=run,args=(broker,))
        process.start()
        processes.append(process)
        processID += 1

    print "Provisioned "+str(len(brokers))+" brokers."
