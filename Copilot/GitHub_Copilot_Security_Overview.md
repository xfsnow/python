# GitHub Copilot安全概览
## 访问控制
通过 SAML 协议和客户的 Azure Active Directory 集成，再集成到客户的 CAS，在 Azure Active Directory 和 CAS 中都是创建了特定的用户组，仅限有权限的员工才可以登录，并实现和企业员工 SSO，不允许个人账号登录并使用 GitHub Copilot。

## 数据安全
* 用户的源码保存在任何地方都可以，不必放在GitHub上。
* Copilot只在IDE中打开的程序文件中选取上下文，未打开的文件不会读取。
* 有限的上下文被发送到 Copilot，生成建议后立即删除上下文。
* 上下文中的参数信息，不放入到模型训练的数据集中。

## 更多详细内容可参考 GitHub 官网的文档
https://resources.github.com/copilot-trust-center/
### How GitHub Copilot treats code and customer data?
GitHub Copilot for Business does not access the source code in your editor other than to generate a suggestion, and prompts used to generate a suggestion are transmitted to the model securely. Once a suggestion is generated, your prompts are not retained.

Prompts used to generate a suggestion may include various elements of the context, including file content both in the file you are editing, as well as neighboring or related files within a project. Prompts may also include the URLs of repositories or file paths to identify relevant context. The comments and code along with context are then used to synthesize and suggest individual lines and whole functions.

中文参考译文：
GitHub Copilot for Business 除了生成建议之外，不会访问编辑器中的源代码，用于生成建议的提示会被安全地传输到模型中。 生成建议后，不会保留提示。

用于生成建议的提示可能包括上下文的各种元素，包括您正在编辑的文件中的文件内容，以及项目中的相邻或相关文件。 提示还可以包括存储库的 URL 或文件路径，以识别相关上下文。 然后，将注释和代码与上下文一起用于合成和建议单个行和整个函数。

### What is transmitted back and forth:

How much data is transmitted back and forth varies widely and depends on many factors, including: the language the user is using, if there are other open tabs, how long the current file is, whether the code referencing feature is enabled, whether the model generates a single, or multi-line suggestion, whether parts of a prompt are redacted, etc. Therefore, we can't indicate exactly how much is transmitted in number of bytes/characters in a prompt. Further, because responses are non-deterministic we can't know how many characters/bytes will be emitted by the model ahead of time. The same input could yield a different output depending on context.

Copilot for Business does not retain any prompts—including code and other context used for the purposes of providing suggestions—for training its models or any other development of Microsoft or GitHub products. Prompts are discarded once a suggestion is returned.

中文参考译文：
来回传输的数据量差异很大，取决于许多因素，包括：用户使用的语言，是否有其他打开的标签，当前文件的长度，是否启用了代码引用功能，模型是否生成单行或多行建议，提示的部分是否被编辑等。 因此，我们无法准确指出提示中传输的字节数/字符数。 此外，由于响应是非确定性的，因此我们无法提前知道模型将发出多少个字符/字节。 根据上下文，相同的输入可能会产生不同的输出。

Copilot for Business 不会保留任何提示，包括用于提供建议的代码和其他上下文，用于训练其模型或任何其他 Microsoft 或 GitHub 产品的开发。 提示在返回建议后被丢弃。

### GitHub Copilot terms of service
https://github.com/customer-terms/github-copilot-product-specific-terms
GitHub Copilot sends an encrypted Prompt from your code editor to GitHub to provide Suggestions to you. Prompts are transmitted only to generate Suggestions in real-time and are deleted once Suggestions are generated. Prompts are not used for any other purpose, including the training of language models. Prompts are encrypted during transit and are not stored at rest. More detailed information on how data is processed by GitHub Copilot is in the GitHub Privacy Statement available at https://gh.io/privacy

中文参考译文：
GitHub Copilot 将加密的 Prompt 从代码编辑器发送到 GitHub，以向您提供建议。 Prompt 仅用于实时生成建议，并在生成建议后删除。 Prompt 不用于任何其他目的，包括语言模型的训练。 Prompt 在传输过程中进行加密，并且不会在休息时存储。 有关 GitHub Copilot 如何处理数据的更多详细信息，请参见 GitHub 隐私声明，网址为 https://gh.io/privacy

### Code Snippets Data
https://docs.github.com/en/site-policy/privacy-policies/github-copilot-for-business-privacy-statement

GitHub Copilot transmits snippets of your code from your IDE to GitHub to provide Suggestions to you. Code snippets data is only transmitted in real-time to return Suggestions, and is discarded once a Suggestion is returned. Copilot for Business does not retain any Code Snippets Data.

中文参考译文：
GitHub Copilot 将代码片段从 IDE 发送到 GitHub，以向您提供建议。 代码片段数据仅在实时传输以返回建议，并在返回建议后被丢弃。 Copilot for Business 不会保留任何代码片段数据。