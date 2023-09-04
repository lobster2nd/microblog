class Twit:
    def __init__(self, uid: str, body: str, author, comments: list):
        self.uid = uid
        self.body = body
        self.author = author
        self.comments = comments
