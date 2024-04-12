from requests import post
from json import loads
from random import randint, choice
class Luis:
	def __init__(self,auth:str='Luis'):
		self.auth = auth
	def req(self,input,name):
		return loads(post(url="https://rubino5.iranlms.ir/",json={"api_version":"0","auth":self.auth,"client":{"app_name":"Main","app_version":"3.6.4","lang_code":"fa","package":"app.rbmain.a","platform":"Android"},"data":input,"method":name}).text)
	def uploadFile(self,file:str):
		with open(file) as f:
			size = f.seek(0, 2)
		id = self.getId()['data']['profiles'][0]["id"]
		input = {"file_name":"m.jpg","file_size":size,"file_type":"Picture","profile_id":id}
		p = self.req(input,'requestUploadFile')
		url = p["data"]['server_url']
		hash = p['data']['hash_file_request']
		file_id = p['data']['file_id']
		byte_file = open(file, 'rb').read()
		headers = {"auth":self.auth,"file-id":file_id,"chunk-size":str(len(byte_file)),"total-part":"1","part-number":"1","hash-file-request":hash}
		m = loads(post(url=url,headers=headers,data=byte_file).text)
		hash_rec = m['data']['hash_file_receive']
		return {"auth":self.auth,"id":file_id,"data":id,"hash_file_receive":hash_rrc}
	def addPost(self,file:str):
		p = self.uploadFile(file)
		rnd = randint(100000, 999999999)
		input = {"caption":"Luis","file_id":p['id'],"hash_file_receive":p['hash_file_receive'],"height":800,"profile_id":p['data'],"post_type":"Picture","rnd":rnd,"tagged_profiles":[],"thumbnail_file_id":p['id'],"thumbnail_hash_file_receive":p["hash_file_receive"],"width":800}
		name = "addPost"
		return self.req(input,name)
	def getId(self):
		return self.req({"equal":False,"limit":10,"sort": "FromMax"},"getProfileList")
	def addText(self,post_id,id,my):
		input = {"content":"Luis","post_id":post_id,"post_profile_id":id,"profile_id":my}
		return self.req(input,"addComment")
	def addLike(self,post_id,id,my):
		input = {"action_type":"Like","post_id":post_id,"post_profile_id":id,"profile_id":my}
		return self.req(input,'likePostAction')
	def addViv(self,post_id,id):
		input = {"post_id":post_id,"post_profile_id":id}
		return self.req(input,"addPostViewCount")
	def isExistUsername(self,name:str):
		input = {"username": name}
		return self.req(input,"isExistUsername")
	def createPage(self,name:str,bio,user):
		input = {"bio": bio,"name": name,"username": user}
		return self.req(input,'createPage')
	def getPost(self,id):
		input = {"limit":10,"sort":"FromMax","target_profile_id":id}
		return self.req(input,"getProfilePosts")
		