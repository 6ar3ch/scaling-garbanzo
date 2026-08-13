from flask import Flask, jsonify, request, Response
import requests

app = Flask(__name__)

@app.get("/config")
def config():
    base = request.host_url.rstrip("/")
    return jsonify({
        "MySource": {
            "name": "我的漫画源",
            "apiUrl": base,
            "detailPath": "/album/<item_id>",
            "photoPath": "/photo/<item_id>/<chapter>",
            "searchPath": "/search/<keyword>/<page>",
            "type": "comic"
        }
    })

@app.get("/search/<keyword>/<int:page>")
def search(keyword, page):
    return jsonify({
        "page": page,
        "has_more": False,
        "results": []
    })

@app.get("/album/<item_id>")
def album(item_id):
    return jsonify({
        "item_id": item_id,
        "name": "示例漫画",
        "cover": "",
        "author": "",
        "description": "",
        "chapters": []
    })

@app.get("/photo/<item_id>/<int:chapter>")
def photo(item_id, chapter):
    return jsonify({
        "item_id": item_id,
        "chapter": chapter,
        "title": f"第{chapter}话",
        "images": []
    })

@app.get("/image/proxy")
def image_proxy():
    img_url = request.args.get("url", "")
    if not img_url:
        return "缺少url参数", 400
    try:
        resp = requests.get(img_url, timeout=10)
        return Response(resp.content, mimetype=resp.headers.get("content-type", "image/jpeg"))
    except Exception as e:
        return f"图片加载失败: {str(e)}", 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3000)
