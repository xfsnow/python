# Azure Active Directory B2C 的一些实践
## 海外 Azure B2C 租户跳转到中国 Azure B2C 租户验证

## 通过IEF策略控制 MFA 认证时的邮件验证码有效期
AAD B2C 的 MFA 认证方式有两种，一种是通过手机短信发送验证码，另一种是通过邮件发送验证码。默认情况下，邮件验证码的有效期为 10 分钟。我们可以通过 IEF 策略来控制邮件验证码的有效期。

### 准备数据
AAD B2C 的租户名字记下来，可以在控制台左上角找到，形如 *contosoftb2c*.onmicrosoft.com 这样的 URL。
AAD B2C 中注册一个新的应用程序，这个应用的 Overview 页面上会目录（租户） ID。
点击 Policies > User flows 下创建的 user flow 名字记下，形如 B2C_1A_signup_signin 的格式。

### 准备密钥
点击进入 Policies > Identity Experience Framework，再展开 Manage 点击 Policy keys，创建 2 个新的密钥，命名分别为TokenSigningKeyContainer 和 TokenEncryptionKeyContainer。具体操作参考 [官方文档](https://docs.azure.cn/zh-cn/active-directory-b2c/tutorial-create-user-flows?pivots=b2c-custom-policy#create-the-encryption-key)

### 准备策略
1. 打开 MFA_Email_Base.xml 文件，做以下修改：

```xml
<TrustFrameworkPolicy xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
xmlns:xsd="http://www.w3.org/2001/XMLSchema"
xmlns="http://schemas.microsoft.com/online/cpim/schemas/2013/06"
PolicySchemaVersion="0.3.0.0"
TenantId="spkorg.onmicrosoft.com"
PolicyId="MFA_Email_Base"
PublicPolicyUri="http://spkorg.onmicrosoft.com/MFA_Email_Base"
TenantObjectId="7a41c675-c64d-4283-8203-c81dfeba3e88">
```
所有 spkorg.onmicrosoft.com 域名都替换成刚才形如 *contosoftb2c*.onmicrosoft.com 的租户名字。 TenantObjectId 替换成刚才在应用程序 Overview 页面上找到的目录（租户） ID。 PublicPolicyUri 替换成形如 http://*contosoftb2c*.onmicrosoft.com/B2C_1A_B2C_1_email 的格式。

`PolicyId="MFA_Email_Base"` 这里是策略的 ID，取一个有意义的名字，比如 `MFA_Email_Base`。
`PublicPolicyUri="http://spkorg.onmicrosoft.com/MFA_Email_Base"` 这里是策略的 URI，形如 `http://*contosoftb2c*.onmicrosoft.com/<PolicyId>` 的格式。

2. 在 Azure 控制台的 Identity Experience Framework 页面上，点击 Upload policy，上传刚才修改好的 `MFA_Email_Base.xml` 文件。
如果有错误提示，请及时截图，因为这个提示显示几秒后就消失了。
上传成功后，由于 Identity Experience Framework 页面默认显示 Getting started 的内容，所以需要向下滚动页面找到 Custom policies 部分，就可以看到刚才上传的策略了。Azure 可能会给策略加上前缀如 `B2C_1A_`，所以我们上传的 `MFA_Email_Base.xml` 策略在 Azure 控制台上显示为 `B2C_1A_MFA_Email_Base`。这是正常的，记下这个 Policy id，后面会用到。

3. 打开 MFA_Email_Extension.xml 文件，做以下修改：

```xml
<TrustFrameworkPolicy xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
xmlns:xsd="http://www.w3.org/2001/XMLSchema"
xmlns="http://schemas.microsoft.com/online/cpim/schemas/2013/06"
PolicySchemaVersion="0.3.0.0"
TenantId="spkorg.onmicrosoft.com"
PolicyId="MFA_Email_Extension"
PublicPolicyUri="http://spkorg.onmicrosoft.com/MFA_Email_Extension"
TenantObjectId="568ceb16-6d05-4e1a-bf15-c05b27c087eb">
  <BasePolicy>
    <TenantId>spkorg.onmicrosoft.com</TenantId>
    <PolicyId>MFA_Email_Base</PolicyId>
  </BasePolicy>
```
所有 spkorg.onmicrosoft.com 域名都替换成刚才形如 *contosoftb2c*.onmicrosoft.com 的租户名字。 TenantObjectId 替换成刚才在应用程序 Overview 页面上找到的目录（租户） ID。

`PolicyId="MFA_Email_Extension"` 这里是策略的 ID，取一个有意义的名字，比如 `MFA_Email_Extension`，注意不能和前面的基础策略重名。
`PublicPolicyUri="http://spkorg.onmicrosoft.com/MFA_Email_Extension"` 这里是策略的 URI，替换成形如 `http://*contosoftb2c*.onmicrosoft.com/<PolicyId>` 的格式。

`<PolicyId>B2C_1A_MFA_EMAIL_BASE</PolicyId>` 这里是基础策略的 ID，替换成刚才上传成功后控制台显示的 Policy id，比如 `B2C_1A_MFA_Email_Base`。

```xml
<Metadata>
   <Item Key="ContentDefinitionReferenceId">api.selfasserted</Item>
   <Item Key="language.intro">Please verify your email address</Item>
   <Item Key="VerificationCodeExpiryInSeconds">3600</Item> <!-- 1 hour -->
   </Metadata>
```
`<Item Key="VerificationCodeExpiryInSeconds">3600</Item>` 这里是邮件验证码的有效期，单位是秒，默认是 600 秒（10 分钟），可以修改成 3600 秒（1 小时）或者更长的时间。
4. 在 Azure 控制台的 Identity Experience Framework 页面上，点击 Upload policy，上传刚才修改好的 `MFA_Email_Extension.xml` 文件。
全部成功后，2个策略都会显示在 Custom policies 部分。