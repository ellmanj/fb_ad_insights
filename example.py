
if __name__ == '__main__':
    import json
    from fb_ad_insights import FbInsightsReport

    my_access_token = 'XXX'
    act_str = 'act_XXX'
    
    # set the params, according to the api documentation:
    #   https://developers.facebook.com/docs/marketing-api/insights/parameters/v2.7
    # fields are part of params, check here for reference:
    #   https://developers.facebook.com/docs/marketing-api/insights/fields/v2.7
    fields = ['ad_name', 'objective', 'reach', 'relevance_score', 'spend']
    params = dict(
        time_range=json.dumps(dict(
            since='2016-05-10',
            until='2016-09-13'
        )),
        fields=','.join(fields),
        level='ad',
        time_increment=1,
    )

    # initialize the fb insights report object with access token and ads account string
    insights = FbInsightsReport(my_access_token, act_str)

    # use the fb insights report object to start the report, wait for it to finish
    insights.initiate_async_report(params)
    insights.wait_for_report()

    # you can save the report to a file
    insights.save_report('export.csv',  'csv')

    # or you can just get the report text
    report = insights.get_report_text('csv')