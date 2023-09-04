class Comment:
    def __init__(self, id: str, author, message: str, twit_id: str):
        self.id = id
        self.author = author
        self.twit_id = twit_id
        self.message = message
