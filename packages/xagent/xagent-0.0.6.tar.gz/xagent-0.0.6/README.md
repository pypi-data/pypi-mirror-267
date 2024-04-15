# XAgents

XAgents项目为在大模型服务基础上的中间件，为了避免各个业务线重复开发，提供统一的程序接口，快速支持各种业务的需求

## 主要能力

- 接入各种模型服务，包括zhipu sdk, 本地LLM，embedding模型，rerank模型，NLU模型等
- 知识库的管理
- RAG的能力
- 工具调用的能力

具体设计参考[文档](https://zhipu-ai.feishu.cn/docx/Y78IdJZSmoESK0x0HZpc7vrWnde)

## 接入方式

### python SDK（python程序快速接入）

#### install

基于python3.10以上版本
  `pip install -U xagent`

#### 本地知识库

参考 tutorial/local_kb.py

#### 服务端知识库

参考 tutorial/remote_kb.py

#### http Service

测试环境&内部生产环境: 117.50.174.44:8001

测试代码
  ```shell
curl -X 'POST' \
  'http://localhost:8001/kb/list' \
  -H 'accept: application/json' \
  -H 'Authorization: Basic emhpcHU6emhpcHU=' \
  -d ''
```

具体接口文档参考 http://117.50.174.44:8001/docs
鉴权的用户名和密码都是zhipu


## Release Note

### 20240325

version: 0.0.4

- 创建了工程项目以及[README文档](https://dev.aminer.cn/solution-center-algorithm/XAgents)、[DEVELOP文档](https://dev.aminer.cn/solution-center-algorithm/XAgents/-/blob/main/DEVELOP.md?ref_type=heads)
- 提供知识库的增删改查、搜索、索引接口
- 提供了知识库文件的增删改查、更新、切片接口
- 提供http接口文档:http://117.50.174.44:8001/docs
- 提供python sdk以及调用[教程](https://dev.aminer.cn/solution-center-algorithm/XAgents/-/tree/main/tutorial?ref_type=heads)

### 20240401

version: 0.0.5

#### BUG FIX
- [修复上传知识库文件时，接口出错的问题](https://dev.aminer.cn/solution-center-algorithm/XAgents/-/issues/9)

#### FEATURE
- [支持在构建索引的时候，临时指定请求embedding模型的并发度](https://dev.aminer.cn/solution-center-algorithm/XAgents/-/issues/8)
- [支持调用部署在本地的embedding服务](https://dev.aminer.cn/solution-center-algorithm/XAgents/-/issues/4)
- [支持调用部署在本地的LLM服务（三代模型）](https://dev.aminer.cn/solution-center-algorithm/XAgents/-/issues/3)
- [解析PDF的时候支持多列PDF的解析以及带图片的PDF的解析](https://dev.aminer.cn/solution-center-algorithm/XAgents/-/issues/2)

#### OTHER
- [在api接口文档中补充了参数说明和example。补充了开发流程规范](https://dev.aminer.cn/solution-center-algorithm/XAgents/-/issues/7)

### 20240408

version: 0.0.6

#### BUG FIX
- [搜索时，传入rerank参数，会报错](https://dev.aminer.cn/solution-center-algorithm/XAgents/-/issues/15)

#### FEATURE
- [开放Agent问答接口](https://dev.aminer.cn/solution-center-algorithm/XAgents/-/issues/5)
- [识别文档中的表格](https://dev.aminer.cn/solution-center-algorithm/XAgents/-/issues/12)

#### OTHER
- [使用镜像部署功能，方便控制版本以及去客户环境部署](https://dev.aminer.cn/solution-center-algorithm/XAgents/-/issues/1)


### 20240415

version: 0.0.7

#### BUG FIX
- [Agent没有知识库配置时，use_kb会导致prompt模板format出错](https://dev.aminer.cn/solution-center-algorithm/XAgents/-/issues/19)

#### FEATURE
- [支持doc/docx文件读取](https://dev.aminer.cn/solution-center-algorithm/XAgents/-/issues/22)
- [Agent问答支持流式接口](https://dev.aminer.cn/solution-center-algorithm/XAgents/-/issues/21)

#### OTHER
- [完善单元测试](https://dev.aminer.cn/solution-center-algorithm/XAgents/-/issues/6)
- [补充一些重要参数的示例]()