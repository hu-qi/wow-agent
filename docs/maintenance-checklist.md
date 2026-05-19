# wow-agent 教程可运行性巡检清单

本文档用于记录 wow-agent 教程重新维护过程中的逐章检查结果。目标不是一次性重写全部教程，而是让每一章都能被新学习者按步骤复现。

## 巡检原则

- 优先保证教程可以在干净环境中跑通。
- 优先补充必要的环境说明，再修改示例代码。
- 每次 PR 只处理一个相对独立的模块，方便 review 和回滚。
- 所有失败案例都应记录复现步骤、错误信息和修复结论。
- 涉及大模型 API 的示例，应说明所需环境变量、模型名称和兼容 endpoint 配置方式。

## 推荐记录格式

| 模块 | 章节 | Python | 依赖版本 | 运行结果 | 问题摘要 | 后续动作 |
| --- | --- | --- | --- | --- | --- | --- |
| OpenAI | 第02课 | 3.10 / 3.11 | 待记录 | 待验证 | 待记录 | 待处理 |

## 环境准备检查

- [ ] README 是否说明推荐 Python 版本
- [ ] README 是否说明虚拟环境创建方式
- [ ] README 是否说明 `pip install -r requirements.txt`
- [ ] README 是否说明 `.env` / API Key 配置方式
- [ ] requirements.txt 是否足够支撑基础教程运行
- [ ] 是否需要补充依赖版本边界或 lock 文件

## OpenAI 章节

- [ ] 第02课-手搓一个土得掉渣的Agent
- [ ] 第03课-OpenAI实现简历信息提取智能体
- [ ] 第04课-OpenAI实现阅卷智能体
- [ ] 第03章-openai-agents/01-安装与配置
- [ ] 第03章-openai-agents/02-初步尝鲜
- [ ] 第03章-openai-agents/05-运行
- [ ] 第03章-openai-agents/09-追踪

重点检查：

- SDK 初始化方式是否仍然有效
- 模型名称是否可用
- API Key / base url 是否说明清楚
- 示例输出是否与当前 SDK 行为一致

## LlamaIndex 章节

- [ ] 第05课-用Llama-index创建Agent
- [ ] 第06课-数据库对话Agent
- [ ] 第07课-RAG接入Agent
- [ ] 第08课-搜索引擎Agent

重点检查：

- 包名是否仍然正确
- Agent / RAG 相关 API 是否变更
- 向量库依赖是否需要额外安装说明
- 示例数据路径是否正确

## Zigent 章节

- [ ] 第09课-初识Zigent
- [ ] 第10课-Zigent实现哲学家多智能体
- [ ] 第11课-Zigent实现教程编写智能体
- [ ] 第12课-Zigent实现出题智能体

重点检查：

- 本地包导入路径是否正确
- LLM 配置是否说明清楚
- 示例是否依赖外部服务或本地文件

## MetaGPT 章节

- [ ] 第13课-metaGPT安装和配置
- [ ] 第14课-metaGPT快速尝鲜
- [ ] 第15课-单动作单智能体
- [ ] 第16课-多动作单智能体
- [ ] 第17课-技术教程智能体
- [ ] 第18课-订阅智能体
- [ ] 第19课-调研员智能体
- [ ] 第20课-单动作多智能体
- [ ] 第21课-带教智能体
- [ ] 第22课-辩论智能体
- [ ] 第23课-多动作多智能体
- [ ] 第24课-狼人杀智能体
- [ ] 第25课-虚拟小镇智能体
- [ ] 第26课-软件公司智能体

重点检查：

- 安装方式是否仍然可用
- 配置文件路径是否正确
- 示例运行成本和耗时是否需要提醒
- 复杂案例是否需要拆成最小可运行示例

## notebooks 检查

- [ ] notebooks 是否能在干净环境中打开
- [ ] 是否有硬编码路径或密钥
- [ ] 是否需要清理历史输出
- [ ] 是否需要补充运行顺序说明
- [ ] 是否需要拆分过长 notebook

## PR 拆分建议

1. `docs: add quick start and maintenance checklist`
2. `docs: refresh OpenAI tutorial setup`
3. `docs: refresh LlamaIndex tutorial setup`
4. `docs: refresh Zigent tutorial setup`
5. `docs: refresh MetaGPT tutorial setup`
6. `fix: make notebooks reproducible`
