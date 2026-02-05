from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

POSTS = [
    {"id": 1, "title": "First Post", "content": "This is the first post."},
    {"id": 2, "title": "Second Post", "content": "This is the second post."},
]


def generate_new_id():
    if not POSTS:
        return 1
    return max(post['id'] for post in POSTS) + 1


# --- ENDPUNKTE ---

# 1. Pfad für die Liste (GET) und das Hinzufügen (POST)
@app.route('/api/posts', methods=['GET', 'POST'])
def handle_posts():
    if request.method == 'POST':
        data = request.get_json()
        if not data or 'title' not in data or 'content' not in data:
            return jsonify({"error": "Title and content are required"}), 400

        new_post = {
            "id": generate_new_id(),
            "title": data['title'],
            "content": data['content']
        }
        POSTS.append(new_post)
        return jsonify(new_post), 201

    # GET Logik (mit Sortierung aus Schritt 6)
    sort_field = request.args.get('sort')
    direction = request.args.get('direction', 'asc')
    result = list(POSTS)

    if sort_field:
        if sort_field not in ['title', 'content'] or direction not in ['asc', 'desc']:
            return jsonify({"error": "Invalid sort parameters"}), 400
        reverse = (direction == 'desc')
        result.sort(key=lambda x: x[sort_field].lower(), reverse=reverse)
    return jsonify(result)


# 2. Pfad für einzelne Posts (ID) - DELETE und PUT
@app.route('/api/posts/<int:post_id>', methods=['DELETE', 'PUT'])
def handle_single_post(post_id):
    post = next((p for p in POSTS if p['id'] == post_id), None)

    if post is None:
        return jsonify({"error": "Post not found"}), 404

    if request.method == 'DELETE':
        POSTS.remove(post)
        return jsonify({"message": f"Post with id {post_id} deleted."}), 200

    if request.method == 'PUT':
        data = request.get_json()
        post['title'] = data.get('title', post['title'])
        post['content'] = data.get('content', post['content'])
        return jsonify(post), 200


# 3. Pfad für die Suche (Schritt 5)
@app.route('/api/posts/search', methods=['GET'])
def search_posts():
    title_query = request.args.get('title', '').lower()
    content_query = request.args.get('content', '').lower()

    filtered_posts = [
        post for post in POSTS
        if title_query in post['title'].lower() and content_query in post['content'].lower()
    ]
    return jsonify(filtered_posts)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002, debug=True)
