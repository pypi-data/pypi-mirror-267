#coding=utf-8

import json
import time

try:
	from urllib import quote
	import urllib2 as import_urllib
except ImportError:
	from urllib.parse import quote
	import urllib.request as import_urllib

class BmobObject:
	"""Bmob的基础对象类
	"""	
	def __init__(self, type):
		"""初始化

		Args:
			type (_type_): Bmob数据的类型，包括指针类、文件类、日期类、地理位置类
		"""		
		self.__dict__["__type"] = type
	
class BmobPointer(BmobObject):
	"""Bmob的指针类

	Args:
		BmobObject (BmobObject): 
	"""	
	def __init__(self, className, objectId):
		"""初始化指针类

		Args:
			className (string): 数据表的名称
			objectId (string): 对应数据的objectId
		"""		
		BmobObject.__init__(self, "Pointer")
		self.__dict__["className"] = className
		self.__dict__["objectId"] = objectId

class BmobFile(BmobObject):
	"""Bmob的文件类

	Args:
		BmobObject (BmobObject): 
	"""	
	def __init__(self, url, filename = ""):
		"""初始化文件类

		Args:
			url (string): 文件路径
			filename (str, optional): 文件名. Defaults to "".
		"""		
		BmobObject.__init__(self, "File")
		self.__dict__["url"] = url
		self.__dict__["filename"] = filename
		
class BmobDate(BmobObject):
	"""Bmob的日期类

	Args:
		BmobObject (BmobObject): 
	"""	
	def __init__(self, timestamp):
		"""初始化日期类

		Args:
			timestamp (int): 时间戳
		"""		
		BmobObject.__init__(self, "Date")
		if type(timestamp) == float or type(timestamp) == int:
			timestamp = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(timestamp / 1000))
		self.__dict__["iso"] = timestamp
		
class BmobGeoPoint(BmobObject):
	"""Bmob的地理位置类

	Args:
		BmobObject (BmobObject): 
	"""	
	def __init__(self, latitude, longitude):
		"""初始化

		Args:
			latitude (float): 纬度
			longitude (float): 经度
		"""		
		BmobObject.__init__(self, "GeoPoint")
		self.__dict__["latitude"] = latitude
		self.__dict__["longitude"] = longitude

def def_marshal(obj):
	return obj.__dict__

class BmobUpdate:
	@staticmethod
	def add(key, value, data = None):
		"""_summary_

		Args:
			key (_type_): _description_
			value (_type_): _description_
			data (_type_, optional): _description_. Defaults to None.

		Returns:
			_type_: _description_
		"""		
		if data == None:
			data = {}
		data[key] = value
		return data
	
	@staticmethod
	def ensuerArray(self, value):
		if isinstance(value, BmobObject):
			value = [value.__dict__]
		elif isinstance(value, dict):
			value = [value]
		elif isinstance(value, list) or isinstance(value, tuple):
			objs = []
			for i in range(0, len(value)):
				obj = value[i]
				if isinstance(obj, BmobObject):
					obj = obj.__dict__
				objs.append(obj)
			value = objs
		else:
			value = [value]
		return value
	
	@staticmethod
	def increment(key, number, data = None):
		return BmobUpdate.add(key, {"__op": "Increment", "amount": number}, data)
	
	@staticmethod
	def arrayAdd(key, value, data = None):
		return BmobUpdate.add(key, {"__op": "Add", "objects": BmobUpdate.ensuerArray(value)}, data)
	
	@staticmethod
	def arrayAddUnique(key, value, data = None):
		return BmobUpdate.add(key, {"__op": "AddUnique", "objects": BmobUpdate.ensuerArray(value)}, data)
	
	@staticmethod
	def arrayRemove(key, value, data = None):
		return BmobUpdate.add(key, {"__op": "Remove", "objects": BmobUpdate.ensuerArray(value)}, data)
	
	@staticmethod
	def addRelations(key, value, data = None):
		return BmobUpdate.add(key, {"__op": "AddRelation", "objects": BmobUpdate.ensuerArray(value)}, data)
	
	@staticmethod
	def removeRelations(key, value, data = None):
		return BmobUpdate.add(key, {"__op": "RemoveRelation", "objects": BmobUpdate.ensuerArray(value)}, data)

class BmobQuery:
	def __init__(self):
		self.filter = {}
	# 基础
	def putWhereFilter(self, key, value = None, oper = None):
		if key == None or len(key) == 0 or value == None:
			return self
		if isinstance(value, BmobObject):
			value = value.__dict__
		if oper == None:
			self.filter[key] = value
		else:
			self.filter[key] = {oper: value}
		return self
	def addWhereEqualTo(self, key, value = None):
		if value == None:
			return self.addWhereNotExists(key)
		else:
			return self.putWhereFilter(key, value)
	def addWhereNotEqualTo(self, key, value = None):
		if value == None:
			return self.addWhereExists(key)
		else:
			return self.putWhereFilter(key, value, "$ne")
	# 比较
	def addWhereGreaterThan(self, key, value):
		return self.putWhereFilter(key, value, "$gt")
	def addWhereGreaterThanOrEqualTo(self, key, value):
		return self.putWhereFilter(key, value, "$gte")
	def addWhereLessThan(self, key, value):
		return self.putWhereFilter(key, value, "$lt")
	def addWhereLessThanOrEqualTo(self, key, value):
		return self.putWhereFilter(key, value, "$lte")
	# 关联
	def addWhereRelatedTo(self, table, objectId, key):
		return self.putWhereFilter(key, {"key": key, "object": {"__type": "Pointer", "className": table, "objectId": objectId}}, "$relatedTo")
	# 存在
	def addWhereExists(self, key, exists = True):
		return self.putWhereFilter(key, exists, "$exists")
	def addWhereNotExists(self, key):
		return self.addWhereExists(key, False)
	# 地理位置
	def addWhereNear(self, key, bmobGeoPointer, maxMiles = None, maxKM = None, maxRadians = None):
		near = {"$nearSphere": bmobGeoPointer.__dict__}
		if maxMiles != None:
			near["$maxDistanceInMiles"] = maxMiles
		if maxKM != None:
			near["$maxDistanceInKilometers"] = maxKM
		if maxRadians != None:
			near["$maxDistanceInRadians"] = maxRadians
		return self.putWhereFilter(key, near)
	def addWhereWithinGeoBox(self, southwest, northeast):
		return self.putWhereFilter(key, {"$box": [southwest.__dict__, northeast.__dict__]}, "$within")
	# 列表
	def addWhereContainedIn(self, key, value, isIn = True):
		if isIn:
			isIn = "$in"
		else:
			isIn = "$nin"
		return self.putWhereFilter(key, value, isIn)
	def addWhereNotContainedIn(self, key, value):
		return self.addWhereContainedIn(key, value, False)
	def addWhereContainsAll(self, key, value):
		return self.putWhereFilter(key, value, "$all")
	# 模糊查询
	def addWhereStrContains(self, key, value):
		return self.putWhereFilter(key, value, "$regex")
	# 子查询
	def addWhereMatchesSelect(self, key, innerQuery, innerKey, innerTable = None, isMatch = True):
		if isMatch:
			isMatch = "$select"
		else:
			isMatch = "$dontSelect"
		if isinstance(innerQuery, BmobQuery):
			innerQuery = {"className": innerTable, "where": innerQuery.filter}
		return self.putWhereFilter(key, {"key": innerKey, "query": innerQuery}, isMatch)
	def addWhereInQuery(self, key, value, className = None, isIn = True):
		if isIn:
			isIn = "$inQuery"
		else:
			isIn = "$notInQuery"
		if isinstance(value, BmobQuery):
			innerQuery = {"className": className, "where": value.filter}
		return self.putWhereFilter(key, value, isIn)

class BmobResult:
	def __init__(self, data):     
		if data == None:
			data = '{}'

		data = data.decode('utf-8')   
		self.stringData = data
		self.queryResults = None
		self._statCount = 0
		self.jsonData = {}
		self._error = None

		try:
			self.jsonData = json.loads(data)
			if 'error' in self.jsonData:
				self._error = self.jsonData['error']
				self._code = self.jsonData['code']
			elif 'results' in self.jsonData:
				self.queryResults = self.jsonData["results"]
			elif 'count' in self.jsonData:
				self._statCount = self.jsonData["count"]

		except:
			self.jsonData = {}
	
	def getError(self):
		return {'error':self._error,'code':self._code}
  
	def __iter__(self):
		if self.queryResults is None:
			self.queryResults = {}
		return iter(self.queryResults)
	
	def __len__(self):
		if self._error is None:
			if self.queryResults is not None:
				return len(self.queryResults)
			elif self._statCount!=0:
				return 0
			else:
				return 1 
		return 0

	def __getattr__(self, name):
		return self.jsonData[name] if name in self.jsonData else None

def BmobRequest(url, method = 'GET', headers = None, body = None, timeout = 10):
	"""发起HTTP请求

	Args:
		url (string): 请求地址
		method (str, optional): 请求方法，默认为GET请求. 
		headers (dict, optional): 请求头，默认为None.
		body (dict, optional): 请求体，默认为None. 
		timeout (int, optional): 超时时间，默认10秒.

	Returns:
		BmobResult: Http请求返回结果
	"""	
	if headers == None:
		headers = {}
	if body != None:
		body = body.encode("utf-8")
	req = import_urllib.Request(url=url, data=body, headers=headers)
	if method != None:
		req.get_method = lambda: method

		try:
			res = import_urllib.urlopen(req, timeout = timeout)
			return BmobResult(res.read())
		except import_urllib.URLError as e:
			try:
				return BmobResult(e.read())
			except Exception as e:
				return BmobResult({'error':f'Exception: {e}','code':'-1'})
	else:
		errMsg = "Unknown Error"
		return BmobResult({'error':errMsg,'code':'-1'})

class Bmob:
	def __init__(self, application_id, rest_api_key):
		"""初始化Bmob

		Args:
			application_id (string): 进入Bmob控制台，具体应用 -> 设置 -> 应用密钥 -> Application ID
			rest_api_key (string): 进入Bmob控制台，具体应用 -> 设置 -> 应用密钥 -> REST API Key
		"""		
		self.domain = 'http://api.codenow.cn'
		self.headers = {"X-Bmob-Application-Id": application_id, "X-Bmob-REST-API-Key": rest_api_key, "Content-Type": "application/json"}
		self.appid = application_id
		self.restkey = rest_api_key

	def resetDomain(self, domain):
		"""重置域名

		Args:
			domain (string): 正式上线之后，建议在初始化Bmob之后，调用这个方法，将你的备案域名替换为正式域名
		"""		
		self.domain = domain
	
	def setUserSession(self, sessionToken):
		"""设置用户的登录sessionToken信息

		Args:
			sessionToken (string): 用户登录的sessionToken

		Returns:
			Bmob: self
		"""		
		self.headers["X-Bmob-Session-Token"] = sessionToken
		return self
	
	def setMasterKey(self, masterKey):
		"""设置masterKey

		Args:
			masterKey (string): 在 控制台 -> 设置 -> 应用密钥 -> Master Key

		Returns:
			Bmob: self
		"""		
		self.headers["X-Bmob-Master-Key"] = masterKey
		return self

	def signUp(self, userInfo):
		"""用户注册

		Args:
			userInfo (dict): 用户的注册数据信息，封装为dict类型

		Returns:
			BmobResult: 数据的查询结果
		"""		
		return BmobRequest(url = self.domain + '/1/users', method = 'POST', headers = self.headers, body = json.dumps(userInfo, default=def_marshal))
	
	def login(self, username, password):
		"""用户登录（账号+密码）

		Args:
			username (string): _description_
			password (string): _description_

		Returns:
			BmobResult: 数据的查询结果
		"""		
		return BmobRequest(url = self.domain + '/1/login?username=' + quote(username) + '&password=' + quote(password), method = 'GET', headers = self.headers)
	
	def loginBySMSCode(self, mobile, smsCode, userInfo):
		"""用户登录（手机号+验证码）

		Args:
			mobile (string): 手机号码
			smsCode (string): 短信验证码
			userInfo (dict): 用户的注册数据信息，封装为dict类型

		Returns:
			BmobResult: 数据的查询结果
		"""		
		userInfo["mobilePhoneNumber"] = mobile
		userInfo["smsCode"] = smsCode
		return self.userSignUp(userInfo)
	
	def resetPasswordByEmail(self, email):
		"""邮件重置密码

		Args:
			email (string): 邮箱

		Returns:
			BmobResult: 数据的查询结果
		"""		
		return BmobRequest(url = self.domain + '/1/requestPasswordReset', method = 'POST', headers = self.headers, body = json.dumps({"email": email}))
	
	def resetPasswordBySMSCode(self, smsCode, password):
		"""重置密码（短信验证码的方式重置）

		Args:
			smsCode (string): 短信验证码
			password (string): 密码

		Returns:
			BmobResult: 数据的查询结果
		"""		
		return BmobRequest(url = self.domain + '/1/resetPasswordBySmsCode/' + smsCode, method = 'PUT', headers = self.headers, body = json.dumps({"password": password}))
	
	def updatePassword(self, userId, oldPassword, newPassword):
		"""重置密码（旧密码方式安全修改用户密码）

		Args:
			userId (string): 要修改密码的用户的objectId
			oldPassword (string): 旧密码
			newPassword (string): 新密码

		Returns:
			BmobResult: 数据的查询结果
		"""		
		return BmobRequest(url = self.domain + '/1/updateUserPassword/' + userId, method = 'PUT', headers = self.headers, body = json.dumps({"oldPassword": oldPassword, "newPassword": newPassword}))
	
	def requestSMSCode(self, mobile, template):
		"""请求发送短信验证码

		Args:
			mobile (string): 要接收验证码的手机号码
			template (string): 验证码的模板（你要先在控制台 -> 短信 -> 自定义模板 中创建你的短信验证码模板，待审核通过之后使用）

		Returns:
			BmobResult: 数据的查询结果
		"""		
		return BmobRequest(url = self.domain + '/1/requestSmsCode', method = 'POST', headers = self.headers, body = json.dumps({'mobilePhoneNumber': mobile, 'template': template}))
	
	def verifySmsCode(self, mobile, smsCode):
		"""检验验证码是否正确

		Args:
			mobile (string): 手机号码
			smsCode (string): 待检验的验证码（6位）

		Returns:
			BmobResult: 数据的查询结果
		"""		
		return BmobRequest(url = self.domain + '/1/verifySmsCode/' + smsCode, method = 'POST', headers = self.headers, body = json.dumps({'mobilePhoneNumber': mobile}))
	
	def functions(self, funcName, body = None):
		"""调用云函数代码

		Args:
			funcName (string): 云函数名称
			body (dict, optional): 请求体. Defaults to None.

		Returns:
			BmobResult: 数据的查询结果
		"""		
		if body == None:
			body = {}
		return BmobRequest(url = self.domain + '/1/functions/' + funcName, method = 'POST', headers = self.headers, body = json.dumps(body, default=def_marshal))
	
	def getServerTime(self):
		"""获取服务器时间戳

		Returns:
			BmobResult: 数据的查询结果
		"""		
		return BmobRequest(url = self.domain + '/1/timestamp/', method = 'GET', headers = self.headers)
	
	def doBatch(self, requests):
		"""批量数据操作

		Args:
			requests (json): requests的数据格式参考文档：https://doc.bmobapp.com/data/restful/develop_doc/#_22

		Returns:
			BmobResult: 数据的查询结果
		"""		
		return BmobRequest(url = self.domain + '/1/batch', method = 'POST', headers = self.headers, body = json.dumps(requests, default=def_marshal))
	
	def save(self, className, data):
		"""新增一条记录

		Args:
			className (string): 数据表的名称
			data (dict): 要新增的数据内容

		Returns:
			BmobResult: 数据的查询结果
		"""		
		if isinstance(data, dict):
			for k, v in data.items():
				if(isinstance(v, BmobObject)):
					data[k] = v.__dict__
		return BmobRequest(url = self.domain + '/1/classes/' + className, method = 'POST', headers = self.headers, body = json.dumps(data, default=def_marshal))
	
	def update(self, className, objectId, data):
		"""更新数据

		Args:
			className (string): 数据表的名称
			objectId (string): 要更新的数据的objectId
			data (dict): 要更新的数据内容

		Returns:
			BmobResult: 数据的更新结果
		"""		
		if isinstance(data, dict):
			for k, v in data.items():
				if(isinstance(v, BmobObject)):
					data[k] = v.__dict__
		return BmobRequest(url = self.domain + '/1/classes/' + className + '/' + objectId, method = 'PUT', headers = self.headers, body = json.dumps(data, default=def_marshal))
	
	def delete(self, className, objectId):
		"""删除单条数据

		Args:
			className (string): 数据表的名称
			objectId (string): 要删除的数据的objectId

		Returns:
			BmobResult: 数据的查询结果
		"""		
		return BmobRequest(url = self.domain + '/1/classes/' + className + '/' + objectId, method = 'DELETE', headers = self.headers)
	
	def findObjects(self, className, where = None, limit = None, skip = None, order = None, include = None, keys = None, count = None, groupby = None, groupcount = None, min = None, max = None, sum = None, average = None, having = None):
		"""多条数据的条件查询

		Args:
			className (string): 数据表名称
			where (json, optional): 查询条件. Defaults to None.
			limit (int, optional): 获取的最大记录数. Defaults to None.
			skip (int, optional): 跳过前面的多少条记录. Defaults to None.
			order (_type_, optional): 按什么进行排序. Defaults to None.
			include (_type_, optional): _description_. Defaults to None.
			keys (_type_, optional): _description_. Defaults to None.
			count (_type_, optional): _description_. Defaults to None.
			groupby (_type_, optional): _description_. Defaults to None.
			groupcount (_type_, optional): _description_. Defaults to None.
			min (string, optional): 需要计算最小值的字段名称. Defaults to None.
			max (string, optional): 需要计算最大值的字段名称. Defaults to None.
			sum (string, optional): 需要求和的字段名称. Defaults to None.
			average (string, optional): 需要计算平均值的字段名称. Defaults to None.
			having (dict, optional): 分组中的过滤条件. Defaults to None.

		Returns:
			BmobResult: 数据的查询结果
		"""		
		try:
			url = self.domain + '/1/classes/' + className

			params = ''
			if limit != None:
				params += '&limit=' + str(limit)
			if skip != None:
				params += '&skip=' + str(skip)
			if count != None:
				params += '&count=' + str(count)
			if groupby != None:
				params += '&groupby=' + quote(groupby)
			if groupcount != None and (groupcount == True or groupcount == 1):
				params += '&groupcount=true'
			if sum != None:
				params += '&sum=' + quote(sum)
			if average != None:
				params += '&average=' + str(average)
			if max != None:
				params += '&max=' + str(max)
			if min != None:
				params += '&min=' + str(min)
			if having != None:
				params += '&having=' + str(having)
			if order != None:
				params += '&order=' + str(order)
			if keys != None:
				params += '&keys=' + str(keys)
			if include != None:
				params += '&include=' + str(include)
			if where != None:
				if isinstance(where, BmobQuery):
					where = where.filter
				params += '&where=' + quote(json.dumps(where, default=def_marshal))
			if len(params) != 0:
				url += '?' + params[1:]
			return BmobRequest(url = url, method = 'GET', headers = self.headers)
		except Exception as e:
			msg = '请求语法错误，请检查查询条件，错误信息：' + str(e)
			print(e)
			return BmobResult({'results':msg})

	def getObject(self, className, objectId):
		"""查询一条记录

		Args:
			className (string): 数据表名称
			objectId (string): 这条记录的objectId

		Returns:
			BmobResult: 数据的查询结果
		"""		
		return BmobRequest(url = self.domain + '/1/classes/' + className + '/' + objectId, method = 'GET', headers = self.headers)

