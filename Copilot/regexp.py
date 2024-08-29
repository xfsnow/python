import random
import re
# 示例文本
text = """
Starter Unit 1
good /gud/ adj. 好的
morning /'mɔ:niŋ/ n. 早晨；上午
Good morning! 早上好！
hi /hai/ interj. (用于打招呼)嗨；喂
hello /hə'ləu/ interj. 你好；喂
afternoon /,a:ftə'nu:n/ n. 下午
Good afternoon! 下午好！
evening /'i:vniŋ/ n. 晚上；傍晚
Good evening! 晚上好！
how /hau/ adv. 怎样；如何
are /a:/ v. 是
you /ju:/ pron. 你；你们
How are you? 你好吗？
I /ai/ pron. 我
am /æm/ v. 是
fine /fain/ adj. 健康的；美好的
thanks /θæŋks/ interj.&n. 感谢；谢谢
OK /əu'kei/ interj.& adv. 好；可以

Starter Unit 2
what /wɔt/ pron.&adj. 什么
is /iz/ v. 是
this /ðis/ pron. 这；这个
in /in/ prep. (表示使用语言、材料等)用；以
English /'iŋgliʃ/ n. 英语adj. 英格兰的；英语的
in English 用英语
map /mæp/ n. 地图
cup /kʌp/ n. 杯子
ruler /'ru:lə/ n. 尺；直尺
pen /pen/ n. 笔；钢笔
orange /'ɔrindʒ/ n. 橙子
jacket /'dʒækit/ n. 夹克衫；短上衣
key /ki:/ n. 钥匙
quilt /kwilt/ n. 被子；床罩
it /it/ pron. 它
a /ə/ art. (用于单数可数名词前)一(人、事、物)
that /ðæt/ pron. 那；那个
spell /spel/ v. 用字母拼；拼写
please /pli:z/ interj. (用于客气地请求或吩咐)请

Starter Unit 3
color /'kʌlə/ n. (=colour) 颜色
red /red/ adj.& n. 红色（的）
yellow /'jeləu/ adj.& n. 黄色（的）
green /gri:n/ adj.& n. 绿色（的）
blue /blu:/ adj.& n. 蓝色（的）
black /blæk/ adj.& n. 黑色（的）
white /wait/ adj.& n. 白色（的）
purple /'pə:pl/ adj.& n. 紫色（的）
brown /braun/ adj.& n. 棕色（的）；褐色（的）
the /ði; ðə/ art. 指已提到或易领会到的人或事
now /nau/ adv. 现在；目前
see /si:/ v. 理解；明白
can /kæn/ modal v. 能；会
say /sei/ v. 说；讲
my /mai/ pron. 我的

Unit 1
name /neim/ n. 名字；名称
nice /nais/ adj. 令人愉快的；宜人的
to /tu:/ 常用于原形动词之前，该动词为不定式
meet /mi:t/ v. 遇见；相逢
too /tu:/ adv. 也；又；太
your /jɔ:/ pron. 你的；你们的
Ms. /miz/ (于女子的姓名前，不指明婚否)女士
his /hiz/ pron. 他的
and /ænd/ conj. 和；又；而
her /hə:/ pron, 她的
yes /jes/ interj. 是的；可以
she /ʃi:/ pron. 她
he /hi:/ pron. 他
no /nəu/ interj. 不；没有；不是
not /nɔt/ adv. 不；没有
zero /'ziərəu/ num. 零
one /wʌn/ num. 一
two /tu:/ num. 二
three /θri:/ num. 三
four /fɔ:/ num. 四
five /faiv/ num. 五
six /siks/ num. 六
seven /'sevn/ num. 七
eight /eit/ num. 八
nine /nain/ num. 九
telephone /'telifəun/ n. 电话；电话机
number /'nʌmbə/ n. 号码；数字
phone /fəun/ n. 电话；电话机
telephone/phone number 电话号码
first /fə:st/ adj. 第一
first name 名字
last /la:st/ adj. 最后的；末尾的
last name 姓
friend /frend/ n. 朋友
China /'tʃainə/ 中国
middle /'midl/ adj. 中间的；中间
school /sku:l/ n. 学校
middle school 中学；初中

Unit 2
sister /'sistə/ n. 姐；妹
mother /'mʌðə/ n. 母亲；妈妈
father /'fa:ðə/ n. 父亲；爸爸
parent /'peərənt/ n. 父（母）亲
brother /'brʌðə/ n. 兄；弟
grandmother /'grænmʌðə/ n.（外）
grandfather /'grænfa:ðə/ n. (外)祖父；爷爷； 
grandparent/'grænpeərənt/ n.祖父（母）；
family /'fæməli/ n. 家；家庭
those /ðəuz/ pron. 那些
who /hu:/ pron. 谁；什么人
oh /əu/ interj. 哦；啊
these /ði:z/ pron. 这些
they /ðei/ pron. 他（她、它）们
well /wel/ interj. 嗯；好吧
have /hæv/ v. 经受；经历
Have a good day! (表示祝愿)过得愉快！
bye /bai/ interj. (=goodbye)再见
son /sʌn/ n. 儿子
cousin /'kʌzn/ n. 堂兄（弟、姐、妹）；表兄
grandpa /'grænpa:/ n. （外）祖父；爷爷；外公mom /mɔm/, /ma:m/ n. (=mum)妈妈
aunt /a:nt/ n. 姑母；姨母；伯母；婶母；舅母
grandma /'grænma:/ n.（外）祖母；奶奶；外婆；
dad /dæd/ n. 爸爸
uncle /'ʌŋkl/ n. 舅父；叔父；伯父；姑父；舅父
daughter /'dɔ:tə/ n. 女儿
here /hiə/ adv. (用以介绍人或物)这就是；在这里
photo /'fəutəu/ n. 照片
of /ɔv, əv/ prep. 属于(人或物)；关于(人或物)
next /nekst/ adj.&n. 下一个（的）；接下来（的）
picture /'piktʃə/ n. 照片；图画
girl /gə:l/ n. 女孩
dog /dɔg/ n. 狗

Unit 3
pencil /'pensl/ n. 铅笔
book /buk/ n. 书
eraser /i'reizə/ n. 橡皮
box /bɒks/ n. 箱；盒
pencil box 铅笔盒；文具盒
schoolbag /'sku:lbæg/ n. 书包
dictionary /'dikʃənəri/ n. 词典；字典
his /hiz/ pron. 他的
mine /main/ pron. 我的
hers /hə:z/ pron. 她的
excuse /ik'skju:z/ v. 原谅；宽恕
me /mi:/ pron. (I的宾格)我
excuse me 劳驾；请原谅
thank /θæŋk/ v. 感谢；谢谢
teacher /'ti:tʃə/ n. 老师；教师
about //ə'baut/ prep. 关于
What about...?(询问消息或提出建议..怎么样？
yours /jɔ:z/ pron. 你的；你们的
for /fɔ:/ prep. 为了；给；对
thank you for... 为......而感谢
help /help/ v.&n. 帮助；援助
welcome /'welkəm/ adj. 受欢迎的
You're welcome. 别客气。
baseball /'beisbɔ:l/ n. 棒球
watch /wɒtʃ/ n. 表；手表
computer /kəm'pju:tə/ n. 计算机；电脑
game /geim/ n. 游戏；运动；比赛
card /kɑ:d/ n. 卡片
ID card 学生卡；身份证
notebook /'nəutbuk/ n. 笔记本
ring /riŋ/ n. 戒指
bag /bæg/ n. 袋；包
in /in/ prep. 在......里
library /'laibrəri/ n. 图书馆
ask /ɑ:sk/ v. 请求；要求；询问
ask... for... 请求；恳求(给予)
find /faind/ v. (过去分词 found)找到；发现
some /sʌm/ adj. 一些；某些
classroom /'klɑ:sru:m/ n. 教室
e-mail /'emeil/ n. (=email)电子邮件
at /æt/ prep. 按照；根据；在(某处、某时间时刻)
call /kɔ:l/ v. (给......)打电话
lost /lɒst/ v. (动词lose的过去式)遗失；丢失
must /mʌst/ modal v. 必须
set /set/ n. 一套；一副；一组
a set of 一套；一副；一组

Unit 4
where /weə/ adv. 在哪里；到哪里
table /'teibl/ n. 桌子
bed /bed/ n. 床
bookcase /'bukkeis/ n. 书架；书柜
sofa /'səufə/ n. 沙发
chair /tʃeə/ n. 椅子
on /ɔn/ prep. 在.......上
under /'ʌndə/ prep. 在.......下
come /kʌm/ v. 来；来到
come on 快点儿
desk /desk/ n. 书桌
think /θiŋk/ n. 认为；想；思考
room /ru:m/ n. 房间
their /ðeə/ pron. 他（她、它）们的
hat /hæt/ n. 帽子
head /hed/ n. 头
yeah /jeə/ interj. 是的；对
know /nəu/ v. 知道；了解
radio /'reidiəu/ n. 收音机；无线电广播
clock /klɔk/ n. 时钟
tape /teip/ n. 磁带；录音带；录像带
player /pleiə/ n.播放机
tape player 录音机
model /'mɔdl/ n. 模型
plane /plein/ n. 飞机
model plane 飞机模型
tidy /'taidi/ adj. 整洁的；井井有条的
but /bʌt/ conj. 但是
our /'auə/ pron. 我们的
everywhere /'evriweə/ adv. 处处；到处；各地
always /'ɔ:lweiz/ adv. 总是

Unit 5
do /du:/ aux v. &v. 用于否定句疑问句；做；干
have /hæv/ v. 有
tennis /'tenis/ n. 网球
ball /bɔ:l/ n. 球
ping-pong /'piŋpɔŋ/ n. 乒乓球
bat /bæt/ n. 球棒；球拍
soccer /'sɔkə/ n. （英式）足球
soccer ball (英式)足球
volleyball /'vɔlibɔ:l/ n. 排球
basketball /'ba:skitbɔ:l/ n. 篮球
hey /hei/ interj. 嘿；喂
let /let/ v. 允许；让
us /ʌs/ pron. (we的宾格)我们
let's = let us 让我们（一起）
go /gəu/ v. 去；走
we /wi:/ pron. 我们
late /leit/ adj. 迟到
has /hæz/ v. (have的第三人称单数形式)有
get /get/ v. 去取（或带来）；得到
great /greit/ adj. 美妙的；伟大的
play /plei/ v. 参加（比赛或运动）；玩耍
sound /saund/ v. 听起来好像
interesting /'intrəstiŋ/ adj. 有趣的
boring /'bɔ:riŋ/ adj. 没趣的；令人厌倦的
fun /fʌn/ adj. 有趣的；使人快乐的n.乐趣；快乐
difficult /'difikəlt/ adj. 困难的
relaxing /ri'læksiŋ/ adj. 轻松的；令人放松的
watch /wɔtʃ/ v. 注视；观看
TV /ti:'vi:/ n. (=television) 电视；电视机
watch TV 看电视
same /seim/ adj. 相同的
love /lʌv/ v.&n. 爱；喜爱
with /wið/ prep. 和......在一起；带有；使用
sport /spɔ:t/ n. 体育运动
them /ðem/ pron. (they的宾格)他(她、它)们
only /'əunli/ adv. 只；仅
like /laik/ v. 喜欢；喜爱
easy /'i:zi/ adj. 容易的；不费力的
after /'a:ftə/ prep. 在......以后
class /kla:s/ n. 班级；课
classmate /'kla:smeit/ n. 同班同学

Unit 6
banana /bə'na:nə/ n. 香蕉
hamburger /'hæmbə:gə/ n. 汉堡包
tomato /tə'ma:təu/ n. 西红柿
ice-cream /ais'kri:m/ n. 冰激凌
salad /'sæləd/ n. 沙拉
strawberry /'strɔ:bəri/ n. 草莓
pear /peə/ n. 梨
milk /milk/ n. 牛奶
bread /bred/ n. 面包
birthday /'bə:θdai/ n. 生日
dinner /'dinə/ n. (中午或晚上吃的)正餐
week /wi:k/ n. 周；星期
think about 思考；思索
food /fu:d/ n. 食物
sure /ʃuə/ adv. 当然；肯定；一定
How about...? (提出建议)......怎么样？
burger /'bə:gə/ n. (=hamburger)汉堡包
vegetable /'vedʒtəbl/ n. 蔬菜
fruit /fru:t/ n. 水果
right /rait/ adj. 正确的；适当的
apple /'æpl/ n. 苹果
then /ðen/ adv. 那么
egg /eg/ n. 蛋；鸡蛋
carrot /'kærət/ n. 胡萝卜
rice /rais/ n. 大米；米饭
chicken /'tʃikin/ n. 鸡肉
so /səu/ conj. (引出评论或问题)那么
breakfast /'brekfəst/ n. 早餐；早饭
lunch /lʌntʃ/ n. 午餐
star /sta:/ n. 明星；星星
eat /i:t/ v. 吃
well /wel/ adv. 好；令人满意地
habit /'hæbit/ n. 习惯
healthy /'helθi/ adj. 健康的
really /'ri:əli/ adv. 真正地
question /'kwestʃən/ n. 问题
want /wɔnt/ v. 需要；想要
be /bi:/ v. 变成
fat /fæt/ adj. 肥的；肥胖的

Unit 7
much /mʌtʃ/ pron.&adj. 许多；大量；多少
How much...? (购物时)......多少钱？
sock /sɔk/ n. 短袜
T-shirt /'ti:ʃə:t/ n. T恤衫
shorts /ʃɔ:ts/ n. (pl.) 短裤
sweater /'swetə/ n. 毛衣
trousers /'trauzəz/ n. (pl.) 裤子
shoe /ʃu:/ n. 鞋
skirt /skə:t/ n. 裙子
dollar /'dɔlə/ n. 元(美国、等国的货币符号为$)
big /big/ adj. 大的；大号的
small /smɔ:l/ adj. 小的；小号的
short /ʃɔ:t/ adj. 短的；矮的
long /lɔ:ŋ/ adj. 长的
woman /'wumən/ n. 女子
Can I help you? 我能帮您吗？
need /ni:d/ v. 需要
look /luk/ v. 看；看上去
pair /peə/ n. 一双；一对
take /teik/ v. 买下；拿；取
Here you are. 给你。
ten /ten/ num. 十
eleven /i'levən/ num. 十一
twelve /twelv/ num. 十二
thirteen /θə:'ti:n/ num. 十三
fifteen /fif'ti:n/ num. 十五
eighteen /ei'ti:n/ num. 十八
twenty /'twenti/ num. 二十
thirty /'θə:ti/ num. 三十
Mr. /'mistə/ 先生
clothes /kləuðz/ n. (pl.) 衣服；服装
store /stɔ:/ n. 商店
buy /bai/ v. 购买；买
sale /seil/ n. 特价销售；出售
sell /sel/ v. 出售；销售；卖
all /ɔ:l/ adj. 所有的；全部的
very /'veri/ adv. 很；非常
price /prais/ n. 价格
boy /bɔi/ n. 男孩
a pair of 一双

Unit 8
when /wen/ adv. (疑问副词)什么时候
month /mʌnθ/ n. 月；月份
January /'dʒænjuəri/ n. 一月
February /'februəri/ n. 二月
March /ma:tʃ/ n. 三月
April /'eiprəl/ n. 四月
May /mei/ n. 五月
June /dʒu:n/ n. 六月
July /dʒu'lai/ n. 七月
August /'ɔ:gəst/ n. 八月
September /sep'tembə/ n. 九月
October /ɔk'təubə/ n. 十月
November /nəu'vembə/ n. 十一月
December /di'sembə/ n. 十二月
happy /'hæpi/ adj. 愉快的；高兴的
Happy birthday! 生日快乐！
old /əuld/ adj. 年老的；旧的
How old...? ....多大年纪？..几岁了？
party /'pa:ti/ n. 聚会；晚会
See you! 再见！
first /fə:st/ num. 第一
second /'sekənd/ num. 第二
third /θə:d/ num. 第三
fifth /fifθ/ num. 第五
eighth /eitθ/ num. 第八
ninth /nainθ/ num. 第九
twelfth /twelfθ/ num. 第十二
twentieth /'twentiəθ/ num. 第二十
test /test/ n. 测验；检查
trip /trip/ n. 旅游；旅行
art /a:t/ n. 艺术；美术
festival /'festivl/ n. (音乐、戏剧等的)节；节日
dear /diə/ adj. 亲爱的
student /'stju:dnt/ n. 学生
thing /θiŋ/ n. 东西；事情
term /tə:m/ n. 学期
busy /'bizi/ adj. 忙碌的；无暇的
time /taim/ n. 时间
Have a good time! (表示祝愿) 过得愉快！
there /ðeə/ adv. (在)那里

Unit 9
favorite /'feivərit/ adj.&n.特别喜爱的(人或事物)
subject /'sʌbdʒekt/ n. 学科；科目
science /'saiəns/ n. 科学
P.E. /pi: 'i:/ n. (=physical education)体育
music /'mju:zik/ n. 音乐；乐曲
math /mæθ/ n. 数学
Chinese /tʃai'ni:z/ n. 语文；汉语中国的
geography /dʒi'ɔgrəfi/ n. 地理(学)
history /'histri/ n. 历史
why /wai/ adv. 为什么
because /bi'kɔz/ conj. 因为
Monday /'mʌndei/ n. 星期一
Friday /'fraidei/ n. 星期五
Saturday /'sætədei/ n. 星期六
for sure 无疑；肯定
free /fri:/ adj. 空闲的
cool /ku:l/ adj. 妙极的；酷的
Tuesday /'tju:zdei/ n. 星期二
Wednesday /'wenzdei/ n. 星期三
Thursday /'θəzdei/ n. 星期四
Sunday /'sʌndei/ n. 星期日
A.M. /ei 'em/ (=a.m.)上午
P.M. /pi: 'em/ (=p.m.) 下午；午后
useful /'ju:sfl/ adj. 有用的；有益的
from /frɔm/ prep (表示开始的时间)从......开始
from... to... 从......到......
Mrs. /'misiz/ (女子的姓氏或姓名前)太太；夫人
finish /'finiʃ/ v. 完成；做好
lesson /'lesn/ n. 课；一节课
hour /'auə/ n. 小时
"""

# # 分割文本为行
# lines = text.strip().split('\n')

# # 定义正则表达式匹配每行开头的英文单词
# pattern = re.compile(r'^\w+')

# # 提取每行开头的英文单词
# extracted_words = [pattern.match(line).group() for line in lines if pattern.match(line)]

# # 将结果合并为字符串
# result = '\n'.join(extracted_words)

# # 输出结果
# print(result)


# 分割文本为行
lines = text.strip().split('\n')

# 定义正则表达式匹配 / 和 / 之间的内容
pattern = re.compile(r'(/.*?/)')

# 提取 / 和 / 之间的内容
extracted_content = [pattern.search(line).group(1) for line in lines if pattern.search(line)]

# 提取出的结果随机排列

random.shuffle(extracted_content)

# 将结果合并为字符串
result = '\n'.join(extracted_content)

# 输出结果
print(result)