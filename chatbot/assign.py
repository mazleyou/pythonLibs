import requests
import json

with open('config.json', 'r') as f:
    config = json.load(f)

ENV = 'DEFAULT'
# env = 'TEST'

# azure portal에 생성된 Luis Authoring resource의 구독 ID 값
SUBSCRIPTION_ID = config[ENV]['SUBSCRIPTION_ID']
# azure portal에 생성된 Luis Authoring resource의 리소스 그룹
RESOURCE_GROUP = config[ENV]['RESOURCE_GROUP']
# azure portal에 생성된 Luis Authoring resource 명에서 authoring 제외한 값
ACCOUNT_NAME = config[ENV]['ACCOUNT_NAME']
# Luis 사이트에 생성한 app 의 ID 값
APP_ID = config[ENV]['APP_ID']
# azure portal에 생성된 Luis Authoring resource 의 key 값
SUBSCRIPTION_KEY = config[ENV]['SUBSCRIPTION_KEY']
# azure portal에 로인 후 https://resources.azure.com/api/token?plaintext=true 사이트에 접속시 리턴되는 token값
AUTH_TOKEN = config[ENV]['AUTH_TOKEN']

URL = 'https://westus.api.cognitive.microsoft.com/luis/authoring/v3.0-preview/apps/{0}/azureaccounts'.format(APP_ID)

DATA = {
    'AzureSubscriptionId': SUBSCRIPTION_ID,
    'ResourceGroup': RESOURCE_GROUP,
    'AccountName': ACCOUNT_NAME
}

HEADERS = {
    'Authorization': 'Bearer {0}'.format(AUTH_TOKEN),
    'Content-Type': 'application/json',
    'Ocp-Apim-Subscription-Key': SUBSCRIPTION_KEY
}

def web_request(method_name, url, dict_data, is_urlencoded=True):
    """Web GET or POST request를 호출 후 그 결과를 dict형으로 반환 """


    method_name = method_name.upper()  # 메소드이름을 대문자로 바꾼다
    if method_name not in ('GET', 'POST'):
        raise Exception('method_name is GET or POST plz...')

    if method_name == 'GET':  # GET방식인 경우
        response = requests.get(url=url, params=dict_data)
    elif method_name == 'POST':  # POST방식인 경우
        if is_urlencoded is True:
            response = requests.post(url=url, data=dict_data,
                                     headers=HEADERS)
        else:
            response = requests.post(url=url, data=json.dumps(dict_data), headers=HEADERS)

    dict_meta = {'status_code': response.status_code, 'ok': response.ok, 'encoding': response.encoding,
                 'Content-Type': response.headers['Content-Type']}
    if 'json' in str(response.headers['Content-Type']):  # JSON 형태인 경우
        return {**dict_meta, **response.json()}
    else:  # 문자열 형태인 경우
        return {**dict_meta, **{'text': response.text}}


response = web_request(method_name='POST', url=URL, dict_data=DATA, is_urlencoded=False)

print(response)


# curl 실행문
#
# curl -v -X POST "https://westus.api.cognitive.microsoft.com/luis/authoring/v3.0-preview/apps/a2721ccb-ee4f-4444-9d3d-a9c75171fc6f/azureaccounts" \
# -H "Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiIsIng1dCI6Im5PbzNaRHJPRFhFSzFqS1doWHNsSFJfS1hFZyIsImtpZCI6Im5PbzNaRHJPRFhFSzFqS1doWHNsSFJfS1hFZyJ9.eyJhdWQiOiJodHRwczovL21hbmFnZW1lbnQuY29yZS53aW5kb3dzLm5ldC8iLCJpc3MiOiJodHRwczovL3N0cy53aW5kb3dzLm5ldC8xNmJhMGJjZi04ZTkzLTRhNDQtYWViZC1jMTA4NWZmOWY2YWUvIiwiaWF0IjoxNjIwMDE5OTkyLCJuYmYiOjE2MjAwMTk5OTIsImV4cCI6MTYyMDAyMzg5MiwiYWNyIjoiMSIsImFpbyI6IkFTUUEyLzhUQUFBQTh1Q1p5RHJHNUxUZnVOc2VId1JXa3VMekhoRGRkZXltVWFET1puWFA3dEE9IiwiYW1yIjpbInB3ZCJdLCJhcHBpZCI6IjVlMWJhNTRkLTQ1MDQtNDc5OS05NjAwLTZkMDVlNThmMDY4MiIsImFwcGlkYWNyIjoiMiIsImZhbWlseV9uYW1lIjoi6rmAIiwiZ2l2ZW5fbmFtZSI6Iu2YhOyEnSIsImdyb3VwcyI6WyJkMDdkZmU4YS1iZmUyLTQzZWItYWY4ZS1lYTZjMDI1NWEwZTMiXSwiaXBhZGRyIjoiMzkuNy40OC45MyIsIm5hbWUiOiLquYAg7ZiE7ISdIiwib2lkIjoiZmJmZmUwN2MtZTgyOC00NmQxLThjODctMWNlMjllZWY3MjZjIiwicHVpZCI6IjEwMDMyMDAwM0VFQzRDOTAiLCJwd2RfZXhwIjoiMCIsInB3ZF91cmwiOiJodHRwczovL3BvcnRhbC5taWNyb3NvZnRvbmxpbmUuY29tL0NoYW5nZVBhc3N3b3JkLmFzcHgiLCJyaCI6IjAuQVNzQXp3dTZGcE9PUkVxdXZjRUlYX24ycmsybEcxNEVSWmxIbGdCdEJlV1BCb0lyQUNrLiIsInNjcCI6InVzZXJfaW1wZXJzb25hdGlvbiIsInN1YiI6IjNEX0lENVlmcldxRUVxWFpGZE9vSm45alc5ME9mVlV2c0pxNTVYZmMxWjgiLCJ0aWQiOiIxNmJhMGJjZi04ZTkzLTRhNDQtYWViZC1jMTA4NWZmOWY2YWUiLCJ1bmlxdWVfbmFtZSI6Imhza2ltQHRhaWhvaXRzLm9ubWljcm9zb2Z0LmNvbSIsInVwbiI6Imhza2ltQHRhaWhvaXRzLm9ubWljcm9zb2Z0LmNvbSIsInV0aSI6IlpMRGVBXzFIZ2syOEJ4cFVFUk9TQVEiLCJ2ZXIiOiIxLjAiLCJ3aWRzIjpbIjYyZTkwMzk0LTY5ZjUtNDIzNy05MTkwLTAxMjE3NzE0NWUxMCIsImI3OWZiZjRkLTNlZjktNDY4OS04MTQzLTc2YjE5NGU4NTUwOSJdLCJ4bXNfdGNkdCI6MTUxMjU0NTc2MH0.ayg1_kPqdXRxTTggleUXmgkfOSwV3FgOU9ppzSeYugh33i0stEXojlcP96ReFSBhxu973fj3PLE750WoZmOAijOeDRjzS8foqYLZjlNLMJ1qgS1YjXnR05KFaUIuHihFeXYv6hFZm0M1Z2h9MUlDddQB69_3tjD803QeoNDlCn8yPUyggudMHObKS7tDrFgj6WOw3-FpinsuS5lPxHUGUB2eyanHIIS7TRztDATGB1xMopD0sILhSSfYnHY2ge3QWb_cZZ1lvhurL-wiwtm8PEEaYHMCE2v83ZJMIbn5lr2UnlIyuisXmPGHH36FAWAJuoOEAYq5uTZGK3QCGm7K7g" \
# -H "Content-Type: application/json" \
# -H "Ocp-Apim-Subscription-Key: 47c90f73ddf44dbaaf6ac22e8065b3c3" \
# --data-ascii '{"AzureSubscriptionId":"049c8480-9f25-4d01-859d-890c714009e7", "ResourceGroup":"carrot-chatbot-test-hskim", "AccountName":"carrot-luis-hskim"}'