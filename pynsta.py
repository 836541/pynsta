import requests
import pyfiglet
import optparse

def error(returncode):
    returncode = str(returncode)

    if returncode[0] in ["4","5"]:
       print(f"Error: {returncode}")
       input("")
       quit()
    
    return 

def readLines(file, threshhold):
    with open(file, "r") as readfile:
        content = readfile.read().splitlines()
    
    if len(content) != threshhold:
        print("Input only facebook page ID (first line) and access token (second line) in the data file.")

    return content 



def arguments():
    parser = optparse.OptionParser()

    parser.add_option("-d","--data", dest="data", help="Line 1 = Facebook Page ID, Line 2 = Access Token")
    (inputs, args) = parser.parse_args()
    
    if not inputs.data:
        parser.error("[x] Please input a file with your tokens and IDs")

    return inputs.data

class Instagram:
    def __init__(self, data):
        self.access_token = readLines(data,2)[1]
        self.page_id = readLines(data,2)[0]
        request = requests.get(f"https://graph.facebook.com/v14.0/{self.page_id}?fields=instagram_business_account&access_token={self.access_token}")
        error(request.status_code)
        self.ig_id = request.json()["instagram_business_account"]["id"]
        self.userdata = dict()
        self.caption = str()
        self.postlink = str()

    def httpGET(self):   
        request = requests.get(f"https://graph.facebook.com/v14.0/{self.ig_id}?fields=media%2Cfollowers_count%2Cfollows_count%2Cusername%2Cname&access_token={self.access_token}")
        error(request.status_code)
        rq = request.json()
        
        self.userdata["following"], self.userdata["followers"] = rq["followers_count"], rq["follows_count"]
        self.userdata["name"], self.userdata["username"] = rq["name"], rq["username"]
        
    
    def httpPOST(self):
        while True:
           try:
              self.postlink = str(input("Image URL>>> "))
              self.caption = str(input("Caption>>> "))
        
              request = requests.post(f"https://graph.facebook.com/v14.0/{self.ig_id}/media?image_url={self.postlink}&caption={self.caption}&access_token={self.access_token}")
              print(request.json())
              imageid = request.json()["id"]
              error(request.status_code)
              request2 = requests.post(f"https://graph.facebook.com/v14.0/{self.ig_id}/media_publish?creation_id={imageid}&access_token={self.access_token}")
              error(request2.status_code)
              print("[*] Success!")
              break
           except:
                
                continue
    
    def followMetric(self):
        print("Following:", (self.userdata["following"]))
        print("Followers:", (self.userdata["followers"]))


    def options(self):
        print("[0] Refresh Menu\n[1] Check Follow Metrics\n[2] Post an Image\n[3] Delete a Post\n[4] Change a Post\n[5] Quit")

    def printHeader(self):
        ascii_header = pyfiglet.figlet_format("PYNSTA")
        print(ascii_header)
        print("__"*38)
        print("Starting the application for account: @", self.userdata["username"], "(",self.userdata["name"],")")
        print("__"*38)
        print("[$$] Welcome to a Basic Instagram GRAPH API (Business API) implementation !")
        self.options()
    
    def terminal(self):
        option = 6
        while option not in range(0,6):
            try:
               option = int(input(">>> "))
            except:
                continue

            if option == 0:
                self.options()
            if option == 1:
                self.followMetric()
            if option == 2:
                self.httpPOST()
            if option == 5:
                input("Press a button to quit>>> ")
                quit()

        
        

if __name__ == "__main__":
    txt = arguments()

    ig = Instagram(data= txt)
    ig.httpGET()
    ig.printHeader()
    while True:
       ig.terminal()

        

    

