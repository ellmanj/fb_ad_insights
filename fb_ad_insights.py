import requests
import time
import codecs


class FbInsightsReport():
    fb_base_url = "https://graph.facebook.com"
    version_str = 'v2.7'
    base_url = '/'.join([fb_base_url, version_str])
    export_url = 'https://www.facebook.com/ads/ads_insights/export_report'

    def _gen_act_insights_url(self):
        return '/'.join([self.base_url, self.act_str, 'insights'])

    def __init__(self, access_token, act_str):
        self.access_token = access_token
        self.report_id = None
        self.act_str = act_str

    def initiate_async_report(self, params):
        params.update(dict(access_token=self.access_token))
        result = requests.post(self._gen_act_insights_url(), params=params)
        self.report_id = result.json()['report_run_id']

    def wait_for_report(self, wait_secs=10):
        while True:
            result = requests.get('/'.join([self.base_url, str(self.report_id)]),
                                  params=dict(
                                      access_token=self.access_token
                                  ))
            print("Percent done: " + str(result.json()['async_percent_completion']))
            if result.json()['async_status'] == 'Job Completed':
                print "Done!"
                break
            time.sleep(wait_secs)

    def save_report(self, filename, format_type):
        # format_type is either 'xls' or 'csv'
        with codecs.open(filename, 'w', 'utf-8') as f:
            f.write(self.get_report_text(format_type))

    def get_report_text(self, format_type):
        # format_type is either 'xls' or 'csv'
        result = requests.get(self.export_url,
                              params=dict(
                                  access_token=self.access_token,
                                  report_run_id=self.report_id,
                                  format=format_type,
                                  )
        )
        return result.text
