import base64
import json
import os.path

from tencentcloud.common import credential
from tencentcloud.common.profile.client_profile import ClientProfile
from tencentcloud.common.profile.http_profile import HttpProfile
from tencentcloud.common.exception.tencent_cloud_sdk_exception import TencentCloudSDKException
from tencentcloud.ocr.v20181119 import ocr_client, models

findstr = '设置'
app_id = '1253177369'
secret_id = 'AKIDHh3Vm2Nq9QhvyVvENZlw3787ZyMizAGJ'
secret_key = '3zvhQVS2bAb4eDg2KdktX3RhFlDY1V2j'
imgpath = './docs/image/ocr.jpg'


with open(imgpath, 'rb') as f:
    base64data = base64.b64encode(f.read())  # 得到 byte 编码的数据
    imgdata = str(base64data, 'utf-8') #转换为utf8编码的字符串

try:
    # 实例化一个认证对象，入参需要传入腾讯云账户secretId，secretKey,此处还需注意密钥对的保密
    # 密钥可前往https://console.cloud.tencent.com/cam/capi网站进行获取
    cred = credential.Credential(secret_id, secret_key)
    # 实例化一个http选项，可选的，没有特殊需求可以跳过
    httpProfile = HttpProfile()
    httpProfile.endpoint = "ocr.tencentcloudapi.com"

    # 实例化一个client选项，可选的，没有特殊需求可以跳过
    clientProfile = ClientProfile()
    clientProfile.httpProfile = httpProfile
    # 实例化要请求产品的client对象,clientProfile是可选的
    client = ocr_client.OcrClient(cred, "ap-beijing", clientProfile)

    # 实例化一个请求对象,每个接口都会对应一个request对象
    req = models.GeneralFastOCRRequest()
    params = {
        "ImageBase64": imgdata
    }
    req.from_json_string(json.dumps(params))

    # 返回的resp是一个GeneralFastOCRResponse的实例，与请求对象对应
    resp = client.GeneralFastOCR(req)
    # 输出json格式的字符串回包
    rel = (json.loads(resp.to_json_string()))['TextDetections']
    for dText in rel:
        if dText['DetectedText'] == findstr:
            wd = dText['DetectedText']
            wx, wy = int(dText['ItemPolygon']['X'] + dText['ItemPolygon']['Width'] / 2), int(
                dText['ItemPolygon']['Y'] + dText['ItemPolygon']['Height'] / 2)
            print(wd, wx, wy)

except TencentCloudSDKException as err:
    print(err)
