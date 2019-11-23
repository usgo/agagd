import requests

class RatingsTopRequest:
    def __init__(self, ratings_files_url):
        self.ratings_files_url = ratings_files_url
    def getRatingsTopActive(self):
        topActiveRequest = requests.get("{}{}".format(self.ratings_files_url, '/topActive.php'))
        return topActiveRequest.content
    def getRatingsTopDanKyu(self):
        topDanKyuRequest = requests.get("{}{}".format(self.ratings_files_url, '/topDanKyu.php'))
        return topDanKyuRequest.content
