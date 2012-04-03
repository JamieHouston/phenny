import requests


def status(phenny, input):
    urls = {
        "navigator": "Navigator?ActivityId=d84c7686-cb60-450d-bbe0-8acf419d44e7&ClientIp=127.0.0.1&Plan=SolrImage&EnableSlotting=True&Debug=Debug&IsAnonymous=False&EnableOutlineForAll=True&Permissions=HasPermissionSearchRM,HasPermissionViewPromotion,HasPermissionSearchRF,HasPermissionSearchRS,HasPermissionLogonToExternalSite,HasPermissionCreateUpdateContributorContract&CountryCode=US&Language=en-US&Navigator=nav-NumberOfPeople,nav-Gender,nav-Age,nav-Ethnicity,ImageType,ColorFormat,Orientation,IsModelReleased,IsPropertyReleased,nav-Style,nav-Layout,nav-Viewpoint,IsInRfCd",
        "search": "Search?Plan=SolrImage&SearchText=dog&Permissions=HasPermissionSearchRF,HasPermissionSearchRM&CountryCode=US&Language=en-US&ActivityId=aac2cd58-c1ba-4708-a97fcd146402080e&SessionId=223f47bd-2a3b-4122-ae7d-82344a1d5d6d"}

    endpoints = {
        'sqa1': 'http://sqa1apiint64.corbis.pre/Search/V3/',
        'sqa2': 'http://sqa1apiint64.corbis.pre/Search/V3/',
        'sqa3': 'http://sqa1apiint64.corbis.pre/Search/V3/',
        'stg': 'http://stgapiint64.corbis.com/Search/V3/',
        'beta': 'http://betaapiint.corbis.com/Search/V3/',
        'prod': 'http://apiint64.corbis.com/Search/V3/',
    }

    if not input.group(2):
        return phenny.reply("Need an environment. Example: sqa1")
    environment = input.group(2)
    r = requests.get(endpoints[environment] + urls["search"])
    answer = "{0}: {1}".format(environment, r.status_code)
    phenny.say(answer)

status.commands = ['status']
status.priority = 'high'
if __name__ == '__main__':
    print __doc__.strip()
