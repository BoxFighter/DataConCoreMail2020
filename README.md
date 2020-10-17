# DataCon. 2020 Coremail邮件安全竞赛 赛题一
DataCon 2020 Coremail邮件安全竞赛-赛题一满分方法源码

可能是运气好碰巧找到了所有过滤规则，请各位大佬不要笑我这个菜鸡，哈哈哈

# 基于规则过滤“发件人伪造”攻击

## 1 赛题描述
了解常见的邮件安全协议，熟悉常见的邮件数据头部字段。在此基础上，自行设计检测算法，识别数据集中所有包含“发件人伪造（Sender Spoofing）”攻击行为的邮件。

数据为5000封左右的邮件信息，经过主办方的匿名化处理，仅保留邮件的头部字段信息。每封邮件均有唯一的ID编号，其中仅有100封左右的邮件含有发件人伪造攻击。

## 2 最终排名
本次比赛我们“菜鸡也要试一下”战队第一题得到了满分100，我们基于规则过滤找到了数据集中包含的所有“发件人伪造”攻击的所有100个样本。
![在这里插入图片描述](https://img-blog.csdnimg.cn/20201017090353643.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3FxXzMyNTA1MjA3,size_16,color_FFFFFF,t_70#pic_center)
## 3 关键知识

### 3.1 SMTP
SMTP邮件服务商互相发送邮件是不需要认证的问题，“发件人伪造”攻击是利用这个问题来实现伪造任意发件人。
 ![在这里插入图片描述](https://img-blog.csdnimg.cn/20201017090715335.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3FxXzMyNTA1MjA3,size_16,color_FFFFFF,t_70#pic_center)

SMTP（Simple Mail Transfer Protocol）协议，即简单邮件传输协议，是定义邮件传输的协议，它是基于TCP服务的应用层协议，用户通过SMTP协议所指定的服务器就可以把邮件发送到收件人的服务器上。
由于SMTP传输数据的阶段是可以人为可控的，所以可能会出现攻击者人为编造传输数据中发件人实现“发件人伪造”攻击。SMTP协议数据传输过程主要是通过以下五个主要命令实现的。
- 	Helo ：表示与服务器内处理邮件的进程开始通话"介绍自己"
- 	Mail from：邮件信息的来源地址，也就是要伪造的地址
- 	Rcpt to：邮件接收者/受害者
- 	Data：邮件的具体内容/可以添加附件等
- 	Quit：退出邮件
攻击者可以利用以上命令进行“发件人伪造”攻击。
目前，为了防范这些问题，有人提出了一些防范技术，如SPF、DKIM、DMARC等。

### 3.2 SPF

SPF（Sender Policy Framework）发件人策略框架，SPF 是为了防范伪造发件人地址发送垃圾邮件而提出的一种开放式标准，是一种以 IP 地址认证电子邮件发件人身份的技术。域名所有者通过在 DNS 中发布 SPF 记录来授权合法使用该域名发送邮件的 IP 地址。
当在 DNS 中定义了域名的 SPF 记录后，为了确认邮件声称发件人不是伪造的，邮件接收方首先检查邮件域名的 SPF 记录，来确定发件人的 IP 地址是否被包含在 SPF 记录中，若包含，则认为是一封正确的邮件，否则认为是一封伪造的邮件并退回，或将其标记为垃圾 / 仿冒邮件。
设置正确的 SPF 记录可以提高邮件系统发送外域邮件的成功率，也可以一定程度上防止被假冒域名发送邮件。
常见SPF记录验证可能返回的结果如下图所示。
 ![在这里插入图片描述](https://img-blog.csdnimg.cn/20201017090649963.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3FxXzMyNTA1MjA3,size_16,color_FFFFFF,t_70#pic_center)


### 3.3 DKIM

DKIM（DomainKeys Identified Mail）域密钥识别邮件，DKIM 是一种防范电子邮件欺诈的验证技术，通过消息加密认证的方式对邮件发送域名进行验证。
邮件发送方发送邮件时，利用本域私钥加密邮件生成 DKIM 签名，将 DKIM 签名及其相关信息插入邮件头。邮件接收方接收邮件时，通过 DNS 查询获得公钥，验证邮件 DKIM 签名的有效性。从而确认在邮件发送的过程中，防止邮件被恶意篡改，保证邮件内容的完整性。
DKIM 标准的模糊性，缺乏安全默认值，以及 MIME 标准的实现的复杂性，灵活性都可以产生改变邮件的主要信息，比如主题，甚至改变整个邮件的内容。包括添加新的恶意附件，从而可以实现利用现有邮件创造欺诈邮件。DKIM字段含义如下图所示。
 ![在这里插入图片描述](https://img-blog.csdnimg.cn/20201017090627929.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3FxXzMyNTA1MjA3,size_16,color_FFFFFF,t_70#pic_center)


### 3.4 DMARC

DMARC（Domain-based Message Authentication, Reporting & Conformance）基于域的消息认证，报告和一致性。
DMARC 是一种基于现有的 SPF 和 DKIM 协议的可扩展电子邮件认证协议，在邮件收发双方建立了邮件反馈机制，便于邮件发送方和邮件接收方共同对域名的管理进行完善和监督。
DMARC 要求域名所有者在 DNS 记录中设置 SPF 记录和 DKIM 记录，并明确声明对验证失败邮件的处理策略。邮件接收方接收邮件时，首先通过 DNS 获取 DMARC 记录，再对邮件来源进行 SPF 验证和 DKIM 验证，对验证失败的邮件根据 DMARC 记录进行处理，并将处理结果反馈给发送方。
DMARC记录标签解释如下所示。
 ![在这里插入图片描述](https://img-blog.csdnimg.cn/20201017090553387.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3FxXzMyNTA1MjA3,size_16,color_FFFFFF,t_70#pic_center)
## 4 解决方法
**基于规则过滤“发件人伪造”攻击样本**
经过阅读分析邮件协议头字段的含义和提交答案尝试验证，我们决定使用规则对比赛数据进行过滤，从而找出数据中的“发件人伪造”攻击样本。

1)	规则1: smtp.mail和From
如果Authentication-Results字段里的smtp.mail和From字段里最后那个发件人的地址不一样，就认为是攻击样本。示例如下：
![在这里插入图片描述](https://img-blog.csdnimg.cn/20201017090903986.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3FxXzMyNTA1MjA3,size_16,color_FFFFFF,t_70#pic_center)

2)	规则2: SPF记录结果不为pass
如果Authentication-Results字段里的spf=后面结果不是pass，就认为是攻击样本。示例如下：
![在这里插入图片描述](https://img-blog.csdnimg.cn/20201017090951501.png#pic_center)
![在这里插入图片描述](https://img-blog.csdnimg.cn/2020101709102297.png#pic_center)
![在这里插入图片描述](https://img-blog.csdnimg.cn/20201017091048789.png#pic_center)
3)	规则3:多个From字段
如果邮件协议头里有多个From，就认为是攻击样本。示例如下：
![在这里插入图片描述](https://img-blog.csdnimg.cn/20201017091116766.png#pic_center)

4)	规则4: Sender和From不一样
如果邮件协议头里Sender和From不一样，就认为是攻击样本。示例如下：
 ![在这里插入图片描述](https://img-blog.csdnimg.cn/20201017091140594.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3FxXzMyNTA1MjA3,size_16,color_FFFFFF,t_70#pic_center)

5)	规则5: From里有特殊字符
如果From邮件地址里有这些特殊符号['~','!','#','$','%','^','&','*',':',';','[',']','--']，就认为是攻击样本。示例如下：
 ![在这里插入图片描述](https://img-blog.csdnimg.cn/20201017091204880.png#pic_center)

6)	规则6: dkim.d和From不一致
如果DKIM-Signature字段里的d=和From不一致，就认为是攻击样本。示例如下：
 ![在这里插入图片描述](https://img-blog.csdnimg.cn/20201017091225273.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3FxXzMyNTA1MjA3,size_16,color_FFFFFF,t_70#pic_center)

7)	规则7: Authentication-Results字段里的header.i和stmp.mail域名不一致
如果Authentication-Results字段里的header.i和stmp.mail域名不一致，就认为是攻击样本。示例如下：
 ![在这里插入图片描述](https://img-blog.csdnimg.cn/20201017091244265.png#pic_center)

8)	规则8: Return-Path和From不一样
如果Return-Path和From不一样，就认为是攻击样本。示例如下：
![在这里插入图片描述](https://img-blog.csdnimg.cn/20201017091301495.png#pic_center)

9)	规则9: X-Return-Path和From不一样
如果X-Return-Path和From不一样，就认为是攻击样本。示例如下：
![在这里插入图片描述](https://img-blog.csdnimg.cn/20201017091317824.png#pic_center)

最后，将所有规则过滤出的结果copy到一个list转set去重即可得到最后的结果。

## 5 参考文献
1.	https://zhuanlan.zhihu.com/p/49443988
2.	http://tools.ietf.org/html/rfc7208
3.	http://www.openspf.org/Introduction
4.	https://docs.microsoft.com/en-us/microsoft-365/security/office-365-security/email-validation-and-authentication?view=o365-worldwide
5.	https://service.mail.qq.com/cgi-bin/help?subtype=1&no=1001505&id=16
6.	https://blog.csdn.net/qq_34101364/article/details/108062913

