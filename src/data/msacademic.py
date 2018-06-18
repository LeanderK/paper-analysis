import http.client, urllib.request, urllib.parse, urllib.error, base64
import os,json
import time

def parsePaper(paperI):
    (paper, i) = paperI
    result = getInfo(paperI)
    first = None
    try: 
        first = result['entities'][0]
    except KeyError:
        print("KeyError")
        print(result)
        first = {'error' : "KeyError", 'json' : result}
    return {**paper, **first}

def getInfo(paperI):
    (paper, i) = paperI
    print("downloading info " + str(i))
    headers = {
        # Request headers
        'Ocp-Apim-Subscription-Key': os.getenv("MSKEY"),
    }

    params = urllib.parse.urlencode({
        # Request parameters
        'query': paper['paper'],
        'complete': '0',
        'count': '10',
        'offset': '',
        'timeout': '',
        'model': 'latest',
    })
    
    json_data = None
    retryRequest1 = True
    while retryRequest1:
        try:
            conn = http.client.HTTPSConnection('api.labs.cognitive.microsoft.com')
            conn.request("GET", "/academic/v1.0/interpret?%s" % params, "{body}", headers)
            response = conn.getresponse()
            data = response.read()
            json_data = json.loads(data)
            conn.close()
            try: 
                msg = json_data['error']['message']
                if msg == 'Rate limit is exceeded. Try again later.':
                    print("rate limited!1")
                    print(json_data)
                    time.sleep(30) 
                else:
                    retryRequest1 = False
            except KeyError:
                retryRequest1 = False
        except Exception as e:
            error = "[Errno {0}] {1}".format(e.errno, e.strerror)
            print(error)
            return {'entities' : [{'error' : error}]}
    
    expr = None
    try: 
        expr = json_data['interpretations'][0]['rules'][0]['output']['value']
    except IndexError:
        print("IndexError")
        return {'entities' : [{'error' : "IndexError", 'json' : json_data}]}

    params = urllib.parse.urlencode({
        # Request parameters
        'expr': expr,
        'model': 'latest',
        'count': '10',
        'offset': '0',
        'orderby': '',
        'attributes': 'Id,Ti,Y,CC,AA.AuN,AA.AuId,AA.AfN,AA.AfId, CC',
    })
    retryRequest2 = True
    while retryRequest2:
        try:
            conn = http.client.HTTPSConnection('api.labs.cognitive.microsoft.com')
            conn.request("GET", "/academic/v1.0/evaluate?%s" % params, "{body}", headers)
            response = conn.getresponse()
            data = response.read()
            json_data = json.loads(data)
            conn.close()
            try: 
                msg = json_data['error']['message']
                if msg == 'Rate limit is exceeded. Try again later.':
                    print("rate limited!2")
                    print(json_data)
                    time.sleep(30) 
                else:
                    retryRequest2 = False
                    print("finished!")
                    return json_data
            except KeyError:
                retryRequest2 = False
                print("finished!")
                return json_data
        except Exception as e:
            error = "[Errno {0}] {1}".format(e.errno, e.strerror)
            print(error)
            return {error : error}