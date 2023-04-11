from flask import Flask, request, jsonify, render_template
import cs50
from fuzzywuzzy import fuzz

db = cs50.SQL("sqlite:///appledb.db")

app = Flask(__name__)

@app.route('/', methods = ['GET', 'POST'])
def basic():
    return render_template('video.html')


@app.route('/video', methods=['GET'])
def get_video():
    title = request.args.get('title')
    
    video = db.execute("SELECT * FROM videos WHERE title LIKE '%' || ? || '%' OR description LIKE '%' || ? || '%'", title, title)
    print(video)
    
    fuzzyvideo = []
    
    for i in range(len(video)):
        tempdict = {
            "videoinfo": video[i],
            "fuzzyscore": fuzz.ratio(title, video[i]['title'])
        }
        fuzzyvideo.append(tempdict)
        
    fuzzyvideo.sort(key=lambda x: x['fuzzyscore'], reverse=True)
    print(fuzzyvideo)
    
    return render_template('video.html', responses=fuzzyvideo)

if __name__ == '__main__':
    app.run(debug=True)
