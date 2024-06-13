from flask import Flask, render_template, request, redirect, url_for, abort
app = Flask(__name__)

# Placeholder for in-memory storage
discussions = {}

@app.route('/')
def index():
    tag_filter = request.args.get('tag')
    search_query = request.args.get('search')
    
    filtered_discussions = discussions
    if tag_filter:
        filtered_discussions = {id: disc for id, disc in filtered_discussions.items() if tag_filter in disc['tags']}
    if search_query:
        filtered_discussions = {id: disc for id, disc in filtered_discussions.items() if search_query.lower() in disc['title'].lower() or any(search_query.lower() in comment['comment'].lower() for comment in disc['comments']) or search_query.lower() in disc['username'].lower()}
        
    return render_template('index.html', discussions=filtered_discussions, all_tags=get_all_tags())

@app.route('/discussion/<int:discussion_id>')
def discussion(discussion_id):
    discussion = discussions.get(discussion_id)
    if discussion is None:
        abort(404)
    return render_template('discussion.html', discussion=discussion, discussion_id=discussion_id)

@app.route('/discussion/new', methods=['GET', 'POST'])
def new_discussion():
    if request.method == 'POST':
        title = request.form['title']
        username = request.form['username']
        tags = request.form['tags'].split(',')
        discussion_id = len(discussions) + 1
        discussions[discussion_id] = {
            'title': title,
            'username': username,
            'comments': [],
            'tags': [tag.strip() for tag in tags]
        }
        return redirect(url_for('discussion', discussion_id=discussion_id))
    return render_template('new_discussion.html')

@app.route('/discussion/<int:discussion_id>/comment', methods=['POST'])
def add_comment(discussion_id):
    discussion = discussions.get(discussion_id)
    if discussion is None:
        abort(404)
        username = request.form['username']
        comment_text = request.form['comment']
        new_comment = {'username': username, 'comment': comment_text}
        discussion['comments'].append(new_comment)
    return redirect(url_for('discussion', discussion_id=discussion_id))

@app.route('/edit_comment/<int:discussion_id>/<int:comment_id>', methods=['GET', 'POST'])
def edit_comment(discussion_id, comment_id):
    if request.method == 'POST':
        new_comment = request.form.get('comment')
        print(f"Received new comment: {new_comment}")
        if new_comment:
            discussions[discussion_id]['comments'][comment_id]['comment'] = new_comment
            print(f"Updated comment: {discussions[discussion_id]['comments'][comment_id]['comment']}")
            return redirect(url_for('edit_comment', discussion_id=discussion_id, comment_id=comment_id))
        else:
            return 'No comment provided', 400

    return render_template('edit_comment.html', discussion_id=discussion_id, comment_id=comment_id, discussions=discussions)

def get_all_tags():
    tags = set()
    for discussion in discussions.values():
        tags.update(discussion['tags'])
    return tags
#if __name__ == '__main__':
#    app.run(debug=True)
