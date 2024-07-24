class function:
    pass


def check_request_success(response: dict, err_msg: str) -> dict | None:
    '''\nrequest를 보냈을 때 성공했는지 여부를 판단합니다. 만약 성공했다면 보낸 데이터를 그대로 보내지만, 실패했다면 주어진 error message로 Exception을 발생시킵니다.
    \nArgs:
        response: response.json() 데이터입니다.(Coinone 한정)
        err_msg: request가 실패한 경우에 띄울 예외 메시지입니다. error code가 들어갈 %s 자리가 필요합니다.
    
    \nReturns:
        보낸 데이터를 그대로 반환합니다. 만약 예외가 발생할 경우 None을 반환합니다.
    '''
    if response['result'] == 'success':
        return response
    
    raise Exception(err_msg % response['error_code'])


def floor(x: float, n: int) -> float:
    x = str(x)
    ind = x.find('.')
    x = x[:ind + n + 1]
    return float(x)