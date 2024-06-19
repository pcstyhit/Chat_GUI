# Changelog

All notable changes to this project will be documented in this file.

The official format can refer to [Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

那下面的内容就按照个人习惯写了

- 🎨 优化了 axios 调用接口的方法, 然后给 SERVER 端的 API 代码进行了整理和添加注释 [#63b065f](https://github.com/pcstyhit/Chat_GUI/commit/63b065f32c479265d85d52166e92180ac7d4688b)

- ✨ 语音播报: 用 WEB 传文本 SERVER, 然后 SERVER 调用 OpenAI 的 tts 模型生成语音 mp3 文件,返回给 WEB, **TODO: 这个需要改掉这个方式** [#da9f0e5](https://github.com/pcstyhit/Chat_GUI/commit/da9f0e5758a0ff73866d32517f6d7f43325e1160)

- ✨ **幽灵对话的功能 幽灵对话的目的是不记录上下文来完成特定的任务**, 节省 API. [#994ad26](https://github.com/pcstyhit/Chat_GUI/commit/994ad26aae005a79790eb2f3d5eeb89f5bf074cf)

- ✨ 上传和下载对话历史的功能, 并且 在去掉新建对话的 WEB 界面增加了这个新的 UI, 并且**设计了新建特殊 prompt 类型的对话的流程** [#ae5d284](https://github.com/pcstyhit/Chat_GUI/commit/ae5d284f21a5c71bee0b0de6efa1f7e860ed3187)

- ♻ 重构项目的全局参数的管理文件,目的是为了适配 OpenAI 的 api 和 Azure 的 api [#c3f29cf](https://github.com/pcstyhit/Chat_GUI/commit/c3f29cf61a71b224f58d2d38e6809dc31dca13d2)

- 🚀 去掉了新建的对话是用全局 overlay 的方式, 也重新设计了 stroe 和整个 chat 项目的 onMounted 的流程 [#8623702](https://github.com/pcstyhit/Chat_GUI/commit/862370229c15ba3739bb79fe7ece4429c5ee4567#diff-49c049b44916ff559c87045fde590e61a2c39574b6b42406b38bce0c9ae2e60c)

- 修复了 tokens 和响应时间在 WEB 上更新的不对的问题 [#4610433](https://github.com/pcstyhit/Chat_GUI/commit/4610433b88f4990276697e8da0e9ff172cc4c2bc)

- 修复了 WEB 的代理没有配置成功的小 BUG [#1e5ece6](https://github.com/pcstyhit/Chat_GUI/commit/1e5ece6c0ce01ec50f9273d4c74ba865b80a35b5)

- ✨ 可以重新发送对话的功能, 需要操作数据库删除旧的信息 [#cd35a8f](https://github.com/pcstyhit/Chat_GUI/commit/cd35a8f6a0ad5a3be1fefde7f170f214850326e3)

- 修复了重命名对话没有生效的问题, 这个还要继续开发, TODO: 重命名对话的功能不该只从 WEB 的配置界面才能修改 [#ff46cfa](https://github.com/pcstyhit/Chat_GUI/commit/ff46cfa3bdc2c75faad801256287df4da3d90692)

- 修复了编辑对话没有生效的问题 [#a6284df](https://github.com/pcstyhit/Chat_GUI/commit/a6284df97522bcf4e98f48f59eac527eeb01bcef)

- ⚡ 对流更新 markdown 的渲染,调整了 v-for 的逻辑, 减少渲染的压力, 其实也就是渲染的工作不要交给 v-for 来，v-for 只做数据内容的比对更新 [#1f81437](https://github.com/pcstyhit/Chat_GUI/commit/1f814370f5737376f6d54b02524dc7c6612337cb)

- 🔥 用 JS 原生的 eventSource 来和 SERVER 端做流对话的更新,去掉了 WebSocket 的方式 [#edb8eb8](https://github.com/pcstyhit/Chat_GUI/commit/edb8eb8fd269110dcfcbe16a5231b0b78e720958)
