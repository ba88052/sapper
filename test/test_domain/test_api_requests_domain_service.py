import pytest
from unittest.mock import patch, MagicMock
from domain.service.api_requests_doamin_service import ApiRequestsDomainService

class TestApiRequestsDomainService:

    def test_fetch_page_list(self):
        # 实例化 ApiRequestsDomainService
        service = ApiRequestsDomainService()
        request_tuples = [
            ('http://example.com', {'headers': {'User-Agent': 'MyApp'}}),
        ]

        # 测试 GET 方法
        response_dict_list = service.fetch_page_list(request_tuples, method="GET")
        for response_dict in response_dict_list:
            response = response_dict["response"]
            assert response.status_code == 200

        # 测试 POST 方法
        response_dict_list = service.fetch_page_list(request_tuples, method="POST")
        for response_dict in response_dict_list:
            response = response_dict["response"]
            assert response.status_code == 200




    # @patch('httpx.AsyncClient.get')
    # @patch('httpx.AsyncClient.post')
    # def test_fetch_page_list_with_error(self, mock_get, mock_post):
    #     """_summary_

    #     Args:
    #         mock_get (_type_): _description_
    #         mock_post (_type_): _description_
    #     """
    #     # 模拟状态码非 200 的响应
    #     mock_bad_response = MagicMock()
    #     mock_bad_response.status_code = 500
    #     mock_bad_response.json = MagicMock(return_value={"error": "Internal Server Error"})
    #     mock_get.return_value = mock_bad_response

    #     # 模拟引发异常的场景
    #     mock_post.side_effect = Exception("Connection Error")

    #     service = ApiRequestsDomainService()

    #     # 测试 GET 方法 - 非 200 状态码
    #     response_list = service.fetch_page_list(["http://example.com"], method="GET")
    #     for response, retry in response_list:
    #         if isinstance(response, Exception):
    #             print(f"Error occurred: {response}")
    #         else:
    #             print (response.text)
    #             assert response.status_code != 200  # 验证非 200 状态码

    #     # 测试 POST 方法 - 异常情况
    #     response_list = service.fetch_page_list(["http://example.com"], method="POST")
    #     for response, retry in response_list:
    #         assert isinstance(response, Exception)  # 验证是否捕获到异常
