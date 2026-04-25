from flask import Flask, request, render_template_string
import requests

app = Flask(__name__)

# Replace with your real OMDb API key
API_KEY = "412bf6da"

html = """
<!DOCTYPE html>
<html>
<head>
<title>AI Movie Recommendation System</title>

<style>
body{
    margin:0;
    font-family:Arial, sans-serif;
    background-image:url('https://images.unsplash.com/photo-1489599849927-2ee91cede3ba');
    background-size:cover;
    background-position:center;
    background-attachment:fixed;
    min-height:100vh;
}

.overlay{
    background:rgba(0,0,0,0.72);
    min-height:100vh;
    padding:30px;
}

h1{
    text-align:center;
    color:white;
    font-size:58px;
    margin-bottom:10px;
}

.subtitle{
    text-align:center;
    color:#f1f1f1;
    font-size:22px;
    margin-bottom:35px;
}

form{
    text-align:center;
    margin-bottom:40px;
}

input{
    width:420px;
    max-width:90%;
    padding:16px;
    font-size:18px;
    border:none;
    border-radius:12px;
    outline:none;
}

button{
    padding:16px 26px;
    font-size:18px;
    border:none;
    border-radius:12px;
    background:#e50914;
    color:white;
    cursor:pointer;
    margin-left:10px;
    transition:0.3s;
}

button:hover{
    background:#b20710;
}

.grid{
    display:grid;
    grid-template-columns:repeat(auto-fit,minmax(220px,1fr));
    gap:25px;
    margin-top:20px;
}

.card{
    background:rgba(255,255,255,0.12);
    backdrop-filter:blur(12px);
    border-radius:18px;
    padding:15px;
    text-align:center;
    color:white;
    transition:0.3s;
    box-shadow:0 8px 20px rgba(0,0,0,0.35);
}

.card:hover{
    transform:scale(1.05);
}

.card img{
    width:100%;
    height:320px;
    object-fit:cover;
    border-radius:12px;
}

.card h3{
    margin-top:12px;
    font-size:19px;
}

.card p{
    color:#ddd;
    margin-top:6px;
}

.message{
    text-align:center;
    color:white;
    font-size:24px;
    margin-top:30px;
}

footer{
    text-align:center;
    color:#ddd;
    margin-top:45px;
    font-size:18px;
}
</style>

</head>
<body>

<div class="overlay">

<h1>🎬 AI Movie Recommendation System</h1>
<p class="subtitle">
Discover movies instantly with real-time posters and smart search.
</p>

<form method="POST">
<input type="text" name="movie" placeholder="Search Avengers, Batman, 3 Idiots..." required>
<button type="submit">Search</button>
</form>

<div class="grid">
{% for m in movies %}
<div class="card">
<img src="{{m.poster}}">
<h3>{{m.title}}</h3>
<p>{{m.year}}</p>
</div>
{% endfor %}
</div>

<div class="message">{{message}}</div>

<footer>
Developed by Siddharth Kharat
</footer>

</div>

</body>
</html>
"""

@app.route("/", methods=["GET", "POST"])
def home():
    movies = []
    message = ""

    if request.method == "POST":
        movie = request.form["movie"]

        url = f"https://www.omdbapi.com/?s={movie}&apikey={API_KEY}"
        data = requests.get(url).json()

        if data.get("Response") == "True":
            for item in data["Search"][:8]:
                poster = item["Poster"]

                if poster == "N/A":
                    poster = "https://via.placeholder.com/300x450?text=No+Poster"

                movies.append({
                    "title": item["Title"],
                    "year": item["Year"],
                    "poster": poster
                })
        else:
            message = data.get("Error", "No movie found")

    return render_template_string(html, movies=movies, message=message)

if __name__ == "__main__":
    app.run(debug=True)
