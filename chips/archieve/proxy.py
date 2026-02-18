from flask import Flask, request, jsonify
import requests
from flask_cors import CORS

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})


# 后端地址（保持不变）
BACKEND_URL = "http://127.0.0.1:5000"

# 示例代理：注册接口
@app.route('/register', methods=['POST'])
def proxy_register():
    try:
        resp = requests.post(f"{BACKEND_URL}/register", json=request.get_json())
        return jsonify(resp.json()), resp.status_code
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# 更新底池统计接口
@app.route('/pot', methods=['GET'])
def proxy_pot():
    try:
        resp = requests.get(f"{BACKEND_URL}/pot")
        return jsonify(resp.json()), resp.status_code
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# 更新玩家下注接口
@app.route('/update_bet', methods=['POST'])
def proxy_update_bet():
    try:
        resp = requests.post(f"{BACKEND_URL}/update_bet", json=request.get_json())
        return jsonify(resp.json()), resp.status_code
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# 更新玩家金额接口：修改当前金额
@app.route('/update', methods=['POST'])
def proxy_update():
    try:
        resp = requests.post(f"{BACKEND_URL}/update", json=request.get_json())
        return jsonify(resp.json()), resp.status_code
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
# 获取所有玩家数据接口
@app.route('/players', methods=['GET'])
def proxy_get_players():
    try:
        resp = requests.get(f"{BACKEND_URL}/players")
        return jsonify(resp.json()), resp.status_code
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# 清空所有玩家数据接口
@app.route('/clear', methods=['POST'])
def proxy_clear_players():
    try:
        resp = requests.post(f"{BACKEND_URL}/clear")
        return jsonify(resp.json()), resp.status_code
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8001)
