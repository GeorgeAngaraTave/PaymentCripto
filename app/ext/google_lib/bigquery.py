# -*- coding: utf-8 -*-

import json
import googleapiclient.discovery
from app.config.google.bigquery import BQ_PROJECT_ID, BQ_NUM_RETRIES, BQ_TIMEOUT, BQ_USE_LEGACY_SQL
import logging as log


def sync_query(bigquery, project_id, query, timeout=10000, num_retries=5, use_legacy_sql=False):
    query_data = {
        'query': query,
        'timeoutMs': timeout,
        # Set to False to use standard SQL syntax. See:
        # https://cloud.google.com/bigquery/sql-reference/enabling-standard-sql
        'useLegacySql': use_legacy_sql
    }
    return bigquery.jobs().query(
        projectId=project_id,
        body=query_data).execute(num_retries=num_retries)


def big_query(data_query):
    if data_query is None:
        return None

    bigquery = googleapiclient.discovery.build('bigquery', 'v2')

    query_job = sync_query(
        bigquery,
        BQ_PROJECT_ID,
        data_query,
        BQ_TIMEOUT,
        BQ_NUM_RETRIES,
        BQ_USE_LEGACY_SQL
    )

    results = []
    page_token = None
    page = bigquery.jobs().getQueryResults(pageToken=page_token, **query_job['jobReference']).execute(num_retries=2)

    results.extend(page.get('rows', []))

    try:
        response = json.dumps(results)
        response = json.loads(response)
        return response
    except Exception, e:
        log.warn(e.message)
        return None


def big_response(array_keys=None, data=None):
    if array_keys is None:
        return None

    if data is None:
        return None

    if len(array_keys) > 0:
        key = array_keys
        array_list = []
        obj = {}
        cont = 0

        for item in data:
            for value in item['f']:
                obj[key[cont]] = value['v']
                cont += 1
            array_list.append(obj)
            obj = {}
            cont = 0

        return array_list
    else:
        return None
