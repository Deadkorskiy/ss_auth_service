from flask import Blueprint, Response, jsonify
from modules.shadowsocks.service import SSConf
from modules.utils.auth import api_key_auth


router = Blueprint('shadowsocks', __name__)

@router.route('key/list/',methods=['GET'])
@api_key_auth
def key_list():
    """Get fresh list of key in YML for (content of user config file of outline-ss-server)"""
    ss_conf = SSConf.get_instance()
    response = Response(response=ss_conf.ss_outline_yml_users_config, status=200, mimetype="text/yaml")
    return response


@router.route('key/rotate/',methods=['GET'])
@api_key_auth
def rotate():
    """Force update of all keys"""
    ss_conf = SSConf.get_instance()
    ss_conf.rotate(True)
    return jsonify({"msg": "{} keys where updated".format(len(ss_conf.ss_keys))})


@router.route('key/random/<int:count>/', methods=['GET'])
@router.route('key/random/', methods=['GET'])
@api_key_auth
def random(count: int = 1):
    """Return list of `count` random keys. Max `count` is 10"""
    if count >= 11:
        return jsonify({"msg": "You requested too many keys per single request"}), 402
    if count < 1:
        count = 1
    ss_conf = SSConf.get_instance()
    keys = ss_conf.get_random_keys(count)
    return jsonify([x.serialize() for x in keys])

