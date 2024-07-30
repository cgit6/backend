# 這裡做路徑控制
from app import app, db
from flask import request, jsonify
from models import Friend


# 下面實作 CRUD 的路徑

# Get all friends
@app.route("/api/friends",methods=["GET"])
def get_friends():
    friends = Friend.query.all() # 從資料庫
    result = [friend.to_json() for friend in friends]
    return jsonify(result), 200


# 創建一筆資料
@app.route("/api/friends", methods=["POST"])
def create_friend():
    try:
        data = request.get_json() 
        # print("data: ",data)
        # 檢查有沒有遺漏值，但是這段可以用 schema 替換
        required_fields = ["name", "role","description", "gender"]
        for field in required_fields:
            if field not in data:
                return jsonify({"訊息":f'缺少必填字段: {field}'}), 400
        
        
        name = data.get("name")
        role = data.get("role")
        description = data.get("description")
        gender = data.get("gender") # 需要性別是因為頭像api 需要

        # 根據性別獲取頭像圖像
        # 後面會使用頭像api來產生大頭照
        if gender == "male":
            img_url = f"https://avatar.iran.liara.run/public/boy?username={name}"
        elif gender == "female":
            img_url = f"https://avatar.iran.liara.run/public/girl?username={name}"
        else:
            img_url = None # 如果沒有填寫
        
        # 更新資料庫
        new_friend = Friend(name=name, role=role, description=description, gender=gender, img_url=img_url)
        db.session.add(new_friend) # 有點像 git add .
        db.session.commit() # 儲存
        return jsonify({"訊息":"創建成功"}), 201
    except Exception as e:
        db.session.rollback() # 撤銷之前提出的更改
        print(e)
        return jsonify({"訊息":f"創建失敗: {e}"}), 500
# 大致流程:
# 整體錯誤控制使用 try...except...
# 在 try 中
# 獲取 client 送過來的訊息
# 檢查有沒有遺漏值
# 將資料存進變數中
# 更新資料庫
# 如果錯誤 => 撤銷提出的更改


# 刪除功能，基礎結構
# @app.route("api/friends/<int:id>", methods=["POST"])
# def delete_friend(id):
#     try:
#         pass
#     except Exception as e:
#         pass

@app.route("/api/friends/<int:id>", methods=["DELETE"])
def delete_friend(id):
    try:
        friend = Friend.query.get(id)
        # 檢查有沒有存在
        if friend is None:
            return jsonify({"訊息": "找不到 Friend"}), 404
        
        # 執行刪除
        db.session.delete(friend)
        db.session.commit() # 更新資料庫
        return jsonify({"訊息":"成功刪除"}), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({"訊息": str(e)}), 500


# 更新單一筆數據
# 採用 patch 更新方式做局部更新
@app.route("/api/friends/<int:id>", methods=["PATCH"])
def patch_friend(id):
    try:
        friend = Friend.query.get(id)
        # 檢查有沒有存在
        if friend is None:
            return jsonify({"訊息":"更新錯誤，資料不存在"}), 404

        data = request.json # 獲取提出的更新訊息
        friend.name = data.get("name", friend.name)
        friend.role = data.get("role", friend.role)
        friend.description = data.get("description", friend.description)

        # 更新數據庫
        db.session.commit() # 🤔直接更新?
        return jsonify({"訊息": "更新成功","詳細內容": friend.to_json()}), 200

    except Exception as e:
        db.session.rollback() # 返回上一動
        return jsonify({"訊息": "更新失敗"}), 500

# 更新的大致流程
# try... except 錯誤處理架構
# try 中嘗試
# 利用 id 取得嘗試要更新的數據
# 檢查有沒有這筆(id) 數據
# 如果有