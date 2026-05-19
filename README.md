# wow-agent【🧪 Beta公测版】

【🧪 Beta公测版本提示：教程主体已完成，正在优化细节，欢迎大家提Issue反馈问题或建议。】

本课程由自塾团队与datawhale合作开发并在datawhale社区进行开源。我们想要建立一个适合部署在企业的简易Agent教程和框架指南。wow-agent致力于在代码行数和依赖库数量之间取得均衡的最小值，用最划算的方式帮助您在本地搭建AI Agent，嵌入到您的生产工作环节中。

## 项目受众

想要在企业内部实现Agent自动办公的人。

## 快速开始

> 当前仓库处于 Beta 公测阶段。为了让新学习者更容易跑通示例，建议先按下面的方式创建独立环境，再逐章验证教程。

### 1. 准备 Python 环境

建议使用 Python 3.10 或 Python 3.11，并为本项目创建独立虚拟环境：

```bash
python -m venv .venv
source .venv/bin/activate  # macOS / Linux
# .venv\Scripts\activate  # Windows PowerShell
python -m pip install --upgrade pip
```

### 2. 安装依赖

```bash
pip install -r requirements.txt
```

如果安装或运行过程中遇到依赖冲突，建议先记录当前 Python 版本、操作系统、报错信息和对应章节，再提交 Issue 或 PR。

### 3. 配置模型密钥

多数示例需要访问大模型 API。可以在项目根目录创建 `.env` 文件，并按实际服务商填写：

```bash
OPENAI_API_KEY=your_api_key_here
# OPENAI_BASE_URL=https://your-compatible-endpoint/v1
```

如果使用 OpenAI API 兼容服务，请同时检查教程中的模型名称、base url 和 SDK 初始化方式。

### 4. 跑通最小示例

建议先从 OpenAI 相关基础章节开始验证，再进入 LlamaIndex、Zigent 和 MetaGPT 章节。每完成一章，可以记录：

- Python 版本
- 依赖版本
- 示例命令
- 是否成功运行
- 如失败，记录完整报错和复现步骤

维护者可参考 [`docs/maintenance-checklist.md`](docs/maintenance-checklist.md) 逐章做可运行性巡检。

## 目录

- 第01课-什么是wow-agent

### task01 openai库搭建AI Agent

- 第02课-手搓一个土得掉渣的Agent
- 第03课-OpenAI实现简历信息提取智能体
- 第04课-OpenAI实现阅卷智能体

### task02 Llama-index库搭建AI Agent

- 第05课-用Llama-index创建Agent
- 第06课-数据库对话Agent
- 第07课-RAG接入Agent
- 第08课-搜索引擎Agent

### task03 Zigent库搭建AI Agent

- 第09课-初识Zigent
- 第10课-Zigent实现哲学家多智能体
- 第11课-Zigent实现教程编写智能体
- 第12课-Zigent实现出题智能体

### task04 metaGPT库搭建AI Agent

- 第13课-metaGPT安装和配置
- 第14课-metaGPT快速尝鲜
- 第15课-单动作单智能体
- 第16课-多动作单智能体
- 第17课-技术教程智能体
- 第18课-订阅智能体
- 第19课-调研员智能体
- 第20课-单动作多智能体
- 第21课-带教智能体
- 第22课-辩论智能体
- 第23课-多动作多智能体
- 第24课-狼人杀智能体
- 第25课-虚拟小镇智能体
- 第26课-软件公司智能体

## 维护计划

当前建议按“小步提交、逐章验证”的方式维护：

1. 先补齐环境准备、依赖安装和 API Key 配置说明。
2. 再按 OpenAI、LlamaIndex、Zigent、MetaGPT 四个模块逐章跑通。
3. 每个模块单独提交 PR，避免一次性大改导致 review 成本过高。
4. 对每个失败案例记录复现步骤、错误信息和修复方案。
5. 对 notebooks 做最小可运行性验证，必要时补充运行环境说明。

## 贡献者名单

| 姓名 | 职责 | 简介 |
| :----| :---- | :---- |
| [黎伟](https://github.com/omige) | 项目负责人 | 规划教程整体 |
| [胡琦](https://github.com/hu-qi) | zigent章节 | 塾员 |
| [珞索](https://github.com/galaAella) | metagpt章节 | 塾员 |
| [陈嘉诺](https://github.com/Tangent-90C) | openai-agent SDK章节 | 塾员 |
| [汤耀月](https://github.com/SuTang-vain) | openai-agent SDK章节项目说明 | 塾员         |

## 参与贡献

- 如果你发现了一些问题，可以提Issue进行反馈，如果提完没有人回复你可以联系[胡琦](https://github.com/hu-qi)同学进行反馈跟进~
- 如果你想参与贡献本项目，可以提Pull request，如果提完没有人回复你可以联系[黎伟](https://github.com/omige)同学进行反馈跟进~
- 如果你对 Datawhale 很感兴趣并想要发起一个新的项目，请按照[Datawhale开源项目指南](https://github.com/datawhalechina/DOPMC/blob/main/GUIDE.md)进行操作即可~

## 关注我们

<div align=center>
<p>扫描下方二维码关注公众号：Datawhale</p>
<img src="https://raw.githubusercontent.com/datawhalechina/pumpkin-book/master/res/qrcode.jpeg" width = "180" height = "180">
</div>

## LICENSE

<a rel="license" href="http://creativecommons.org/licenses/by-nc-sa/4.0/"><img alt="知识共享许可协议" style="border-width:0" src="https://img.shields.io/badge/license-CC%20BY--NC--SA%204.0-lightgrey" /></a><br />本作品采用<a rel="license" href="http://creativecommons.org/licenses/by-nc-sa/4.0/">知识共享署名-非商业性使用-相同方式共享 4.0 国际许可协议</a>进行许可。

*注：默认使用CC 4.0协议，也可根据自身项目情况选用其他协议*
