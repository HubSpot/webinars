from django.conf import settings
from sanetime import time
import hapicrank.task_queues as tq
import logging

class SyncParcel(object):

    def trigger(self):
        if self.parent_sync.debug: return self  # allow manual jumping through sync
        try:
            return self.trigger_task.enqueue(max_retries=5)
        except BaseException as err: 
            self.parent_sync.error = 'Task queue failed to accept enqueue request: err=%s' % str(err)
            logging.debug("TQDEBUG: %s" % self.parent_sync.error)
            self.parent_sync.save()
        return self

    @property
    def trigger_task(self):
        url = '%s%s'%(settings.APP_URL, self.trigger_path)
        logging.debug("TQDEBUG: url is %s" % url)
        uid = '%s|%s|%s' % (self.__class__.phase_type, self.__class__.object_type, self.id)
        logging.debug("TQDEBUG: uid is %s" % uid)
        qid = self.parent_sync.id % settings.NUM_QUEUES
        logging.debug('TQDEBUG: qid is %s' % qid)
        return tq.Task(queue=settings.TASK_QUEUES[qid], method='POST', url=url, uid=uid)

    @property
    def trigger_path(self):
        tpath = "/webinars/%s_syncs/%s/%ss/%s/go" % (self.__class__.object_type, self.parent_sync.id, self.__class__.phase_type, self.id)
        logging.debug("TQDEBUG: trigger_path is %s" % tpath)
        return tpath

    @property
    def postbin_partial_path(self):
        return "%s?postbin=" % self.trigger_path
    
    @property
    def taskqueue_path(self):
        taskpath = "%s?taskqueue=True" % self.trigger_path
        logging.debug("TQDEBUG: taskpath is %s" % taskpath)
        return taskpath

    def lock_for_work(self):
        if self.parent_sync.completed_at: return False
        if self.started_at: return False
        now = time()
        locked = (self.__class__.objects.filter(id=self.id, started_at__isnull=True).update(started_at=now) == 1)
        if not locked: return False
        self.started_at = now  # the update wouldn't have updated self-- so I'm just making it consistent here
        return True

    def open_for_rework(self):
        self.started_at = None
        self.completed_at = None
        self.save()

