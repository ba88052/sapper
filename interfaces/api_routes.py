import base64
import json

from flask import Blueprint, g, make_response, request

from application.sapper_application_service import SapperApplicationService

# 會吃main.py的flask啟動設定
routes = Blueprint("routes", __name__)


def get_pubsub_message():
    """
    獲取pub/sub的訊息

    Returns:
        dict: order_dict，pub/sub內部挾帶的訊息，以dict格式呈現
    """
    message = json.loads(request.data.decode("utf-8"))
    if "message" in message and "data" in message["message"]:
        message = message["message"]["data"]
        decoded_message = base64.b64decode(message).decode("utf-8")
        order_dict = json.loads(decoded_message)
        print(order_dict)
        return order_dict
    return None


@routes.route("/sapper/execute_table_transform_job", methods=["POST"])
def execute_collect_mission():
    """
    專門用來接收pub/sub的訊息，觸發將傳入範圍切小後打出去的接口
    """
    order_dict = get_pubsub_message()
    print("AAAA")
    SapperApplicationService(
        message=order_dict, application_infra_respository=g.APPLICATION_INFRA_ADAPTOR, domain_infra_respository=g.DOMAIN_INFRA_ADAPTER
    ).execute()
    print("PPPPP")
    return make_response((f"success", 204))


# @routes.route("/test", methods=["POST"])
# def test():
#     order_dict = get_pubsub_message()
#     return make_response(("Dead mail for Scuessssssss", 204))
