from bmob import *
import datetime

b = Bmob("a49b83c0314118e5e2fe115699ba00c7", "b24648781f5bd927784dcacdf39a5a70")  # 有效
# b = Bmob("ca79e5ac860f0ccf6729c3d366ee959e", "61e06ffe2e09df6c8e2bb1996a3aa013")  # 到期
# from bmob import *
# b = Bmob('application_id','rest_api_key')

# 获取一条记录
# r = b.getObject("Ppt", "15fd040e43")
# print(r)

# 删除一条记录
# isoK = b.delete('ai_log','93a9b6847f')
# print(isoK)

# 更新一条记录
# isOK = b.update('ai_log','93a9b6847f',data={
#     'messages':'mytest'
# })
# print(isOK)

# 保存一条记录
# isOK = b.save('ai_log',data={
#     'messages':'这是新的内容'
# })
# print(isOK)

# Bmob日期类的使用
# isOK = b.save('tests',data={
#     'date':BmobDate(datetime.datetime.now().timestamp()*1000)
# })
# print(isOK)

# 查询数据
# rs = b.findObjects('Ppt',limit=10,skip=10,order='-createdAt')
# for r in rs:
#     print(r.title)

# 获取服务器时间
# rs = b.getServerTime()
# print(rs,rs.timestamp,rs.datetime)

# 调用云函数
# rs = b.functions('good',{'name':'yeah'})
# print(rs)

# 请求发送短信验证码
# rs = b.requestSMSCode('13512707963')
# print(rs)

# 检查验证码是否正确
# rs = b.verifySmsCode('13512707963','785871')
# print(rs)

# 账号密码登录
# rs = b.login('13512707963','123456')
# print(rs)

# 短信验证码重置密码
# rs = b.resetPasswordBySMSCode('340443','123456')
# print(rs)

# 旧密码方式安全修改用户密码
# rs = b.updatePassword('340b4f1e65', '123', '123')
# print(rs)

# 邮件重置密码
# rs = b.resetPasswordByEmail('support1@bmobapp.com')
# print(rs)

# 注册用户
# rs = b.signUp('13800138002','123456', userInfo={
#     'sex':True,
#     'age':100
# })
# print(rs)

# 文件上传和数据表的结合使用
# bmobFile = b.upload('d:/武汉虫洞智能科技有限公司2024A11L4018766.pdf')
# print(bmobFile.url)
# print(bmobFile.filename)

# isOK = b.save('tests',data={
#     'myfile':bmobFile
# })
# print(isOK)

# 删除文件（这里有一个BUG，控制台->素材 里面的数据文件看上去并没有真正删除掉）
# rs = b.delFile('https://bmob-cdn-31082.bmobpay.com/2024/04/13/9d6307b540bfcfdc8000aaec0e197c0f.pdf')
# print(rs)

# 指针类的使用
# isOK = b.save('tests',data={
#     'name':'Bmob',
#     'my':BmobPointer('Ppt','ce05c4cbff')
# })
# print(isOK)

# 数组的保存
isOK = b.save('tests',data={
    'name':'我的数组',
    'mylist':['good','yes','不是']
})
print(isOK)

# 地理位置类的使用
# isOK = b.save('tests',data={
#     'name':'Bmob',
#     'address':BmobGeoPoint(50,100)
# })
# print(isOK)

# 复杂查询

# 查询
# query = BmobQuery().addWhereEqualTo('isShow',False).addWhereContainedIn('objectId',['a5030db1e1','2e3f4acfa6','fc9659a3c5'])
# rs = b.findObjects('Ppt',where=query,limit=2,order='objectId',skip=0,keys=['title','type'],include=['type'])
# print('查询结果是',rs)
# for r in rs:
#     print(r)

# 获取指针对应的数据
# rs = b.findObjects('tests',where=None,include=['my','you'])
# # print('查询结果是',rs)
# for r in rs:
#     print(r)
#     print('')

# 求和
# query = BmobQuery().addWhereEqualTo('isFree',False)  #.addWhereContainedIn('objectId',['a5030db1e1','2e3f4acfa6','fc9659a3c5'])
# rs = b.sum('Ppt', ['count','isShow'], where=None)
# print('求和是',rs)

# 计数
# query = BmobQuery().addWhereEqualTo('isShow',False).addWhereContainedIn('objectId',['ddddd'])
# rs = b.count('Ppt', where=None)
# print('总行数是',rs)

# 最大值
# query = BmobQuery().addWhereEqualTo('isShow',False).addWhereContainedIn('objectId',['ddddd'])
# rs = b.max('PptType', 'weight', where=None)
# print('最大值是',rs)

# 最小值
# query = BmobQuery().addWhereEqualTo('isShow',False).addWhereContainedIn('objectId',['ddddd'])
# rs = b.min('PptType', ['weight'], where=None)
# print('最小值是',rs)

# 平均值
# query = BmobQuery().addWhereEqualTo('isShow',False).addWhereContainedIn('objectId',['ddddd'])
# rs = b.mean('PptType', ['weight'], where=None)
# print('平均值是',rs)

# 数组的查询
query = BmobQuery().addWhereContainedIn('mylist',['真好','yes'])
rs = b.findObjects('tests',where=query,keys=['mylist'])
for r in rs:
    print(r)
