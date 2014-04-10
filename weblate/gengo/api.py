#!/usr/bin/env python
# coding: UTF-8
"""Gengo gettext."""

import time

from django.conf import settings
from gengo import Gengo

from weblate.gengo.models import Job, Order

_gengo = None


def gengo():
    global _gengo
    if not _gengo:
        _gengo = Gengo(
            public_key=str(settings.GENGO['public_key']),
            private_key=str(settings.GENGO['private_key']),
            sandbox=settings.GENGO['sandbox'],
        )
    return _gengo


def post_jobs(jobs):
    ctime = time.time()
    r = gengo().postTranslationJobs(jobs=jobs)
    order_id = r['response']['order_id']
    Order(id=order_id, created=ctime).save()

    while True:
        r = gengo().getTranslationOrderJobs(id=order_id)
        if int(r['response']['order']['jobs_queued']) == 0:
            break
        time.sleep(1)

    for job in r['response']['order']['jobs_available']:
        Job(
            id=job,
            order_id=order_id,
            lang=None,
            source=None,
            translation=None,
            status='queued'
        ).save()

    update_statuses()


def update_statuses():
    jobs = {}
    for job in Job.get_in_progress():
        jobs[job.id] = job

    r = gengo().getTranslationJobBatch(id=','.join(str(id) for id in jobs))
    if r['response']:
        for job_data in r['response']['jobs']:
            job = jobs[int(job_data['job_id'])]
            job.status = job_data['status']
            job.source = job_data['body_src']
            job.translation = job_data.get('body_tgt', '')
            job.lang = job_data['lc_tgt']
            if job.lang == 'no':
                job.lang = 'nb'
            job.save()
