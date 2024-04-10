import os
from aliyun.log import LogClient, GetLogsRequest
from cryptography.fernet import Fernet

class SlsLogStore:
    def __init__(self, key=None):
        self.access_key_id, self.access_key_secret = self.get_access_key(key)

    def get_access_key(self, key):
        encryption_account = {
            "access_key_id": 'gAAAAABmFlzfOJRPM9r8y37flIiJkM3TO6NrVdYK62cZGsqoEzymIzCZ8LbUdnkoPk5K8ibOo4GD-DPOos00B0ocaWcvkvsVfu-DtcSbxCJFkAOJVS0x9-8=',
            "access_key_secret": 'gAAAAABmFl0AY5ych1DeBtlpv2efMzqzrRaerEjOgB5H5cJKjlyWVMQ5e0KutYM7tBvHIxL3BUR1MqIqdkXY6ZF9Mpg30miCa2zKbkz2FPuQ9Z2EoiMx5vc='
        }
        if not key:
            key = os.environ.get('fernet_key')
            if not key:
                raise Exception("请先设置fernet_key")

        cipher_suite = Fernet(key.encode('utf-8'))
        access_key_id = cipher_suite.decrypt(encryption_account.get('access_key_id').encode('utf-8')).decode('utf-8')
        access_key_secret = cipher_suite.decrypt(encryption_account.get('access_key_secret').encode('utf-8')).decode('utf-8')

        return access_key_id, access_key_secret

    def sls_config_res(self, tp, from_timestamp, to_timestamp, query) -> list:
        result = []
        config = {
            "hz_log": {
                "endpoint": "cn-hangzhou.log.aliyuncs.com",
                "project_name": "hz-k8s",
                "logstore_name": "hz-k8s"
            },
            "hz_ingress": {
                "endpoint": "cn-hangzhou.log.aliyuncs.com",
                "project_name": "hz-k8s",
                "logstore_name": "nginx-ingress"
            },
            "usa_log": {
                "endpoint": "us-west-1.log.aliyuncs.com",
                "project_name": "usa-k8s",
                "logstore_name": "usa-log"
            },
            "usa_ingress": {
                "endpoint": "us-west-1.log.aliyuncs.com",
                "project_name": "usa-k8s",
                "logstore_name": "usa-ingress"
            }
        }
        endpoint, project_name, logstore_name = config.get(tp).values()
        client = LogClient(endpoint, self.access_key_id, self.access_key_secret)
        request = GetLogsRequest(project_name, logstore_name, from_timestamp, to_timestamp, query=query)
        response = client.get_logs(request)
        for log in response.get_logs():
            result.append(dict(log.contents))
        return result

    def hz_ingress_log(self, from_timestamp, to_timestamp, query) -> list:
        """
        查询杭州的ingress日志
        @param from_timestamp: 开始时间戳
        @param to_timestamp: 结束时间戳
        @param query: 查询条件
        @return: 查询结果(List类型)
        """
        try:
            result = self.sls_config_res('hz_ingress', from_timestamp, to_timestamp, query)
        except Exception as e:
            raise Exception(f"查询杭州的ingress日志失败: {e}")
        return result

    def hz_service_log(self, from_timestamp, to_timestamp, query) -> list:
        """
        查询杭州的服务日志
        @param from_timestamp: 开始时间戳
        @param to_timestamp: 结束时间戳
        @param query: 查询条件
        @return: 查询结果(List类型)
        """
        try:
            result = self.sls_config_res('hz_log', from_timestamp, to_timestamp, query)
        except Exception as e:
            raise Exception(f"查询杭州的service日志失败: {e}")
        return result

    def usa_ingress_log(self, from_timestamp, to_timestamp, query) -> list:
        """
        查询美国的ingress日志
        @param from_timestamp: 开始时间戳
        @param to_timestamp: 结束时间戳
        @param query: 查询条件
        @return: 查询结果(List类型)
        """
        try:
            result = self.sls_config_res('usa_ingress', from_timestamp, to_timestamp, query)
        except Exception as e:
            raise Exception(f"查询美国的ingress日志失败: {e}")
        return result

    def usa_service_log(self, from_timestamp, to_timestamp, query) -> list:
        """
        查询美国的服务日志
        @param from_timestamp: 开始时间戳
        @param to_timestamp: 结束时间戳
        @param query: 查询条件
        @return: 查询结果(List类型)
        """
        try:
            result = self.sls_config_res('usa_log', from_timestamp, to_timestamp, query)
        except Exception as e:
            raise Exception(f"查询美国的service日志失败: {e}")
        return result
