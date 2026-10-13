import requests

get_endpoints = [
  "/",
  "/ads/create",
  "/ads/1",
  "/login",
  "/register",
  "/auth/github",
  "/auth/github/callback",
  "/users",
  "/up",
  "/api/health",
  "/api/feed",
  "/api/docs",
  "/api/redoc",
  "/api/openapi.json"
]
post_endpoints = [
  ("/ads", {
        "_token": "1qKDMtYzYvFCzsLgzNDv2JGwUK99qs2ofDHi18Uo",
        "title": "sfd",
        "description": "sdf",
        "price": "500",
        "category_id": "",
    }),
    ("/ads/1/comments", {
        "_token": "1qKDMtYzYvFCzsLgzNDv2JGwUK99qs2ofDHi18Uo",
        "body": "asd"
    }),
    ("/login", {
            "_token":	"Nlor7zr7XSsfFjEod4D6yGCC57pR359D2Ll83ZuX",
            "email":	"V4n1sh@gmail.com",
            "password":	"Ks54060208#"
            }),
    ("/register", {
        "_token":	"q20xNrMurv6uh5esFC7h3Ht7itTCEhBi5ebnk1Xy",
        "name":	"lev",
        "email": "V4n2sh@gmail.com",
        "password":	"Ks54060208#"
    }),
    ("/logout", {
        "_token": "28IeWLsJuLor9hXQ2UgXfQHglAFngmFZUHDvgDRm"
    }),
]

for endpoint in get_endpoints:
    url = f"http://localhost:8080{endpoint}"
    print(url)
    r = requests.get(url)
    with open(f"get_res/endpoint_{get_endpoints.index(endpoint)}.json", "w", encoding="utf-8") as f:
        f.write(r.text)

session = requests.Session()

for path, data in post_endpoints:
    url = f"http://localhost:8080{path}"
    print(f"POST {url}")
    print(f"status: {r.status_code}")
    print(f"final url: {r.url}")
    print(f"content-type: {r.headers.get('Content-Type')}")
    body = r.text
    with open(f"post_res/endpoint_{path.split('/')[-1]}.json", "w", encoding="utf-8") as f:
            f.write(r.text)