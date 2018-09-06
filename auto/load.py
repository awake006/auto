from locust import task, TaskSet, HttpLocust, events
from gevent._semaphore import Semaphore
all_locust_spawned = Semaphore()
all_locust_spawned.acquire()


def on_hatch_complete(**kwargs):
    all_locust_spawned.release()


events.hatch_complete += on_hatch_complete


class BaseLocust(TaskSet):
    def on_start(self):
        all_locust_spawned.wait()


class PageObject(BaseLocust):
    def on_start(self):
        super(PageObject, self).on_start()
