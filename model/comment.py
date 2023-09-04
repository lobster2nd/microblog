class Comment:
    def __init__(self, uid: str, author, message: str, twit_id: str):
        self.uid = uid
        self.author = author
        self.twit_id = twit_id
        self.message = message
