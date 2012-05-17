import requests
import time


def status(phenny, input):
    def get_status(url, service):
        start = time.time()
        r = requests.get(url)
        end = time.time() - start
        if r.content == "null" or len(r.content) == 0:
            status = "FAIL!!!!"
        else:
            status = r.status_code
        return {'duration' : end, 'status_code': status, 'url': "{0}{1}".format(url[:10], "..."), 'service': service}

    urls = {
        "navigator": "Navigator?ActivityId=d84c7686-cb60-450d-bbe0-8acf419d44e7&ClientIp=127.0.0.1&Plan=SolrImage&EnableSlotting=True&Debug=Debug&IsAnonymous=False&EnableOutlineForAll=True&Permissions=HasPermissionSearchRM,HasPermissionViewPromotion,HasPermissionSearchRF,HasPermissionSearchRS,HasPermissionLogonToExternalSite,HasPermissionCreateUpdateContributorContract&CountryCode=US&Language=en-US&Navigator=nav-NumberOfPeople,nav-Gender,nav-Age,nav-Ethnicity,ImageType,ColorFormat,Orientation,IsModelReleased,IsPropertyReleased,nav-Style,nav-Layout,nav-Viewpoint,IsInRfCd",
        "search": "Search?Plan=SolrImage&SearchText=dog&Permissions=HasPermissionSearchRF,HasPermissionSearchRM&CountryCode=US&Language=en-US&ActivityId=aac2cd58-c1ba-4708-a97fcd146402080e&SessionId=223f47bd-2a3b-4122-ae7d-82344a1d5d6d"}

    endpoints = {
        'dev1': 'http://DL00DEV1API01.corbis.pre/Search/V3/Search',
        'dev2': 'http://DL00DEV2API01.corbis.pre/Search/V3/Search',
        'dev3': 'http://DL00DEV3API01.corbis.pre/Search/V3/Search',
        'sqa1': 'http://sqa1apiint64.corbis.pre/Search/V3/',
        'sqa2': 'http://sqa2apiint64.corbis.pre/Search/V3/',
        'sqa3': 'http://sqa3apiint64.corbis.pre/Search/V3/',
        'stg': 'http://stgapiint64.corbis.com/Search/V3/',
        'beta': 'http://betaapiint.corbis.com/Search/V3/',
        'prod': 'http://apiint64.corbis.com/Search/V3/',
    }

    if not input.group(2):
        return phenny.reply("Need an envronment or url. Example: sqa1 or http://corbis.com")

    environment = input.group(2)

    if environment.startswith("http"):
        stat = get_status(environment, 'custom')
        phenny.say("Service: %(service)s Status: %(status_code)s Duration: %(duration)s" % stat)
    else:
        for service in urls:
            try:
                stat = get_status(endpoints[environment] + urls[service], service)
                phenny.say("Service: %(service)s Status: %(status_code)s Duration: %(duration)s" % stat)
            except Exception, e:
                phenny.say("It either works or it doesn't.  Try a real url or environment and I'll try a real test.")
            finally:
                pass


status.commands = ['status']
status.priority = 'high'
if __name__ == '__main__':
    print __doc__.strip()
