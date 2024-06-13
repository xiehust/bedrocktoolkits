<p>Skip to Main Content</p>
<p>单击此处以返回 Amazon Web Services 主页</p>
<p>联系我们</p>
<p>支持</p>
<p>中文（简体）</p>
<p>我的账户</p>
<p>登录</p>
<p>创建 AWS 账户</p>
<p>re:Invent</p>
<p>产品</p>
<p>解决方案</p>
<p>定价</p>
<p>文档</p>
<p>了解</p>
<p>合作伙伴网络</p>
<p>AWS Marketplace</p>
<p>客户支持</p>
<p>活动</p>
<p>探索更多信息</p>
<p>关闭</p>
<p>عربي</p>
<p>Bahasa Indonesia</p>
<p>Deutsch</p>
<p>English</p>
<p>Español</p>
<p>Français</p>
<p>Italiano</p>
<p>Português</p>
<p>Tiếng Việt</p>
<p>Türkçe</p>
<p>Ρусский</p>
<p>ไทย</p>
<p>日本語</p>
<p>한국어</p>
<p>中文 (简体)</p>
<p>中文 (繁體)</p>
<p>关闭</p>
<p>我的配置文件</p>
<p>注销 AWS Builder ID</p>
<p>AWS 管理控制台</p>
<p>账户设置</p>
<p>账单与成本管理</p>
<p>安全证书</p>
<p>AWS Personal Health Dashboard</p>
<p>关闭</p>
<p>支持中心</p>
<p>专家帮助</p>
<p>知识中心</p>
<p>AWS Support 概述</p>
<p>AWS re:Post</p>
<p>单击此处以返回 Amazon Web Services 主页</p>
<p>免费试用</p>
<p>联系我们</p>
<p>re:Invent</p>
<p>产品</p>
<p>解决方案</p>
<p>定价</p>
<p>AWS 简介</p>
<p>入门</p>
<p>文档</p>
<p>培训和认证</p>
<p>开发人员中心</p>
<p>客户成功案例</p>
<p>合作伙伴网络</p>
<p>AWS Marketplace</p>
<p>支持</p>
<p>AWS re:Post</p>
<p>登录控制台</p>
<p>下载移动应用</p>
<p>博客主页</p>
<p>版本</p>
<p>关闭</p>
<p>中国版</p>
<p>日本版</p>
<p>한국 에디션</p>
<p>기술 블로그</p>
<p>Edisi Bahasa Indonesia</p>
<p>AWS 泰语博客</p>
<p>Édition Française</p>
<p>Deutsche Edition</p>
<p>Edição em Português</p>
<p>Edición en Español</p>
<p>Версия на русском</p>
<p>Türkçe Sürüm</p>
<p>亚马逊AWS官方博客</p>
<p>妙语连珠，文采飞扬——使用 AWS 自研芯片，快速构建 LLama 3 等大语言模型应用</p>
<p>by</p>
<p>AWS Team</p>
<p>| on</p>
<p>20 5月 2024</p>
<p>| in</p>
<p>Architecture</p>
<p>|</p>
<p>Permalink</p>
<p>|</p>
<p>Share</p>
<p>背景</p>
<p>随着 AIGC/GenAI 的生成式人工智能模型的兴起，LLM/SD 等模型越来越多的深入文本/图像/视频生成与多模态/复杂推理等场景。相对于传统的机器学习模型相比，生成式人工智能模型要大得多，也复杂得多。然而，这种模型增加了复杂性，也带来了高昂的推理成本，以及对强大计算资源日益增长的需求。对于资源有限的企业和研究人员来说，生成式人工智能模型的高推理成本可能会成为进入市场的障碍，因此需要更高效、更具成本效益的解决方案。此外，大多数生成式人工智能使用案例都涉及人机交互或真实世界场景，因此需要能提供低延迟性能的硬件。同时，大语言模型的发布日趋频繁，如何快速构建测试环境对模型功能进行评测也成为企业业务人员和研究人员面临的挑战。</p>
<p>在本文中，我们将介绍如何采用 AWS Inf2 实例，在 AWS 自研芯片上一键部署多个业界领先的大语言模型，方便企业业务人员进行测试，同时开放出 API 接口，方便进行性能基准测试以及下游的应用程序的调用。</p>
<p>AWS Inferentia2</p>
<p>AWS 一直在利用专用芯片进行创新，以满足对功能强大、高效且经济实惠的计算硬件的日益增长的需求。</p>
<p>Amazon Inferentia2 是 AWS 自研的第二代推理芯片，专为 transformer 的语言及其 CV 类的模型而构建，基于 XLA 和 HLO 架构，为动态输入大小和用 C++ 编写的自定义运算符添加了硬件优化。它还支持随机舍入，与传统舍入模式相比可实现高性能和更高的精度，以及其他并行计算，内存计算的针对性的优化。</p>
<p>Amazon Inf2 实例可以大规模部署日益复杂的模型，例如大型语言模型（LLM）和潜在扩散模型。Inf2 实例可帮助您在部署超大型模型时实现可持续发展目标，可通过加速器之间的超高速连接支持横向扩展分布式推理。您可以使用 Inf2实例来运行推理应用程序，以实现文本摘要、代码生成、视频和图像生成、语音识别、个性化、欺诈检测等等。</p>
<p>与同类基于 Nvidia GPU 的 EC2 实例相比 ，Inf2 实例的吞吐量可提高多达 2.3 倍，每次推理的成本可降低多达 70%，实例可实现高达 50% 的性能功耗比提升。包括 Leonardo.ai、德国电信和 Qualtrics 在内许多客户已在其深度学习和生成式人工智能应用程序中采用了 Inf2 实例。</p>
<p>模型介绍</p>
<p>我们选取了最近 3 个比较主流的语言模型 Meta-Llama-3-8B、Mistral-7B-Instruct-v0.2 和 CodeLlama-7b-Instruct-hf，方便用户进行体验。</p>
<p>模型名称</p>
<p>发布公司</p>
<p>参数数量</p>
<p>发布时间</p>
<p>模型能力</p>
<p>Meta-Llama-3-8B</p>
<p>Meta</p>
<p>80 亿</p>
<p>2024 年 4月</p>
<p>语言理解、翻译、代码生成、推理、聊天</p>
<p>Mistral-7B-Instruct-v0.2</p>
<p>Mistral AI</p>
<p>73 亿</p>
<p>2024 年 3月</p>
<p>语言理解、翻译、代码生成、推理、聊天</p>
<p>CodeLlama-7b-Instruct-hf</p>
<p>Meta</p>
<p>70 亿</p>
<p>2023 年 8月</p>
<p>代码生成，代码补全、聊天</p>
<p>AWS Inferentia 2 的加速器显存大小为 32GB，在推理中比较常用的数据类型是 BF16/FP16，通常我们通过模型参数数量 * 2 估算所需的显存大小（比如 7B 到模型，所需显存大约为 7 * 2 = 14GB）。在模型推理的过程中通常会引入缓存机制（KV cache）， 这种缓存机制随着序列长度（Sequence length）和批量大小（Batch Size）线性增加内存分配。理论上对于 16B 以下的模型，单张 AWS Inferentia 2 芯片完全能够胜任。</p>
<p>Meta-Llama-3-8B</p>
<p>是 Llama 大语言模型家族最新、最先进的成员，由 Meta AI 于 2024 年 4 月发布。 Llama 3 模型具有改进的预训练、即时理解、输出生成、编码、推理和数学技能。 Meta AI 团队表示，Llama 3 有潜力成为人工智能新一波创新浪潮的启动者。Llama 3 模型有 8B 和 70B 两个公开发布的版本。 Llama 400B 模型尚未发布，与另两个模型相比，它使用更多数据进行训练，并且具有更多参数。</p>
<p>Mistral-7B-Instruct-v0.2</p>
<p>是 Mistral AI 公司于 2024 年 3 月发布，它标志着开源语言模型发展的一个重要里程碑。 凭借其令人印象深刻的性能、高效的架构和广泛的功能，Mistral 7B v0.2 为易于使用且功能强大的 AI 工具树立了新标准。 该模型能够在从自然语言处理到编码的各种任务中表现出色，这使其成为研究人员、开发人员和企业的宝贵资源。</p>
<p>CodeLlama-7b-Instruct-hf</p>
<p>是 Meta AI 发布的一系列的模型集合，参数规模从 70 亿到 700 亿不等。它是一个通过使用文本提示生成代码的大型语言模型（LLM）。 Code Llama 是针对代码任务，使开发人员的工作流程更快、更高效，并降低编码人员的学习门槛。Code Llama 有潜力用作生产力和教育工具，帮助程序员编写更强大、文档更齐全的软件。</p>
<p>方案架构</p>
<p>方案采用 Client-Server 的架构，客户端使用了 HuggingFace Chat UI，提供了一个 PC 或者移动设备都能访问的聊天页面。服务端的模型推理使用了 Text Generation Inference，一个高效的大语言模型推理框架，它在 docker 容器中运行。我们预先使用 Optimum Neuron 对模型进行了编译，并将编译结果上传到了 HF Hub 中。我们还在 HuggingFace Chat UI 中加入了模型切换机制，通过一个调度器（Scheduler）控制 Text Generation Inference 容器加载不同的模型。</p>
<p>方案特点</p>
<p>所有的组件部署在一台 AWS Inf2 单卡实例（inf2.xl 或者 inf2.8xl）上，用户能够在一台实例上体验多种模型的效果；</p>
<p>采用 Client-Server 的架构，用户可根据自身的实际需要替换对客户的或者服务器端进行裁剪和替换。例如模型可部署在 AWS SageMaker 中，前端 Chat UI 可部署在 Node 服务器。为演示方便，我们把前后端都部署在了同一台 Inf2 服务器上；</p>
<p>采用开源框架，用户可根据自身需要对前端页面或者模型进行定制；</p>
<p>提供 Text Generation Inference 的 API 接口，方便使用 API 的用户快速接入；</p>
<p>使用 AWS Cloudformation 一键部署，适合于企业内部各类业务及开发人员。</p>
<p>主要组件</p>
<p>AWS Neuron SDK</p>
<p>AWS Neuron 是 Amazon Inferentia 实例上的 SDK。Neuron 由编译器、运行时和分析工具组成，并预先集成到流行的机器学习框架中，包括 TensorFlow、Pytorch 和 MXNet。AWS Neuron SDK 可以帮助开发人员在不同机型和多卡的 AWS Inferentia 加速器上部署各种参数规模的模型，并且兼容模型分片（sharding），流水线并行，张量平行，量化压缩等业界成熟的模型推理功能，因此可以在 pytorch/Tensorflow 各种业界流行的 DL 框架和流程中进行 LLM 模型的推理。</p>
<p>AWS Neuron SDK 设计为与 PyTorch 和 TensorFlow 等框架原生集成，使得客户可以继续使用现有的工作流程和应用程序框架，并且最大程度地减少代码更改以及与特定于推理框架（如：llamacc）的绑定，使用同样的 Huggingface pipeline/Tokenizer 等代码逻辑实现自然语言处理（NLP）/理解、语言翻译、文本摘要、视频和图像生成、语音识别、个性化、欺诈检测等业务场景。</p>
<p>Optimum Neuron</p>
<p>Optimum Neuron 是 HuggingFace Transformers 库和 AWS 加速芯片（AWS Trainium、AWS Inferentia）Neuron SDK 之间的接口。 它提供了一组工具，可以轻松地对不同下游任务的单加速器和多加速器设置进行模型加载、训练和推理。在本文中，我们主要用到了 Optimum Neuron 的 export 接口。要在 Neuron 设备上部署 HuggingFace Transformers 模型，需要编译模型并将其导出为序列化格式，然后再进行推理。 export 接口通过使用 Neuron 编译器（ Neuronx-cc 或 Neuron-cc ）进行提前（AOT）编译，模型将转换为序列化和优化的 TorchScript 模块。</p>
<p>在编译过程中，我们引入了张量并行性机制，在2个 NeuronCore 之间分割权重、数据和计算。更多的编译参数可以参考</p>
<p>链接</p>
<p>。</p>
<p>Text Generation Inference（TGI）</p>
<p>Text Generation Inference（TGI）是一个用 Rust 和 Python 编写的框架，用于部署和服务大型语言模型。 是一个用于部署和服务大型语言模型（LLM）的工具包。 TGI 为最流行的开源 LLM 提供高性能文本生成服务。它的主要功能如下：</p>
<p>简单的启动器，可为众多 LLM 提供推理服务</p>
<p>支持 generate 和 stream 两种接口</p>
<p>使用服务器发送事件（SSE）的令牌流</p>
<p>支持 Nvidia、AWS Inferentia、Trainium 等多种加速器</p>
<p>HuggingFace Chat UI</p>
<p>HuggingFace Chat UI 是一个开源聊天工具，由 SvelteKit 构建，可以很容易地部署到 Cloudflare、Netlify、Node 等环境中。主要具有以下功能：</p>
<p>页面可定制</p>
<p>可存储对话记录，聊天记录存储在 MongoDB 中</p>
<p>支持在 PC 端以及手机端运行</p>
<p>后端可对接 Text Generation Inference，同时支持 Anthropic、Amazon SageMaker、Cohere 等 API 接口</p>
<p>可对接多种开源模型（Llama 系列，Mistral/Mixtral 系列，Falcon 等）</p>
<p>得益于 Hugging Chat UI 的页面定制能力，我们在其中加入了模型切换的功能，使得在同一台 EC2 Inf2 服务器上，用户就可以在不同的模型之间进行切换。</p>
<p>方案部署</p>
<ol>
<li>在部署解决方案前，请确保您在 us-east-1（弗吉尼亚）或者 us-west-2（俄勒冈）区域具有 inf2.xl 或者 inf2.8xl 的使用配额，配额申请方式见</li>
</ol>
<p>参考链接</p>
<p>。</p>
<ol>
<li>
<p>登录控制台，在控制台页面右上角切换区域至 us-east-1（弗吉尼亚）或者 us-west-2（俄勒冈）。</p>
</li>
<li>
<p>在 Service 搜索框中输入 Cloudformation，点击进入，然后点击”Create stack”，依次选择”Choose an existing template”，”Amazon S3 URL”。</p>
</li>
<li>
<p>如果您计划使用已有 VPC 进行部署，请使用 4.1 的步骤；如果您计划创建新的 VPC 进行部署，请使用 4.2 的步骤。</p>
</li>
</ol>
<p>4.1. 使用已有 VPC</p>
<p>在 Amazon S3 URL 中输入</p>
<p>https://zz-common.s3.amazonaws.com/tmp/tgiui/20240501/launch_server_default_vpc_ubuntu22.04.yaml</p>
<p>Stack name，填写堆栈名称；</p>
<p>InstanceType，选择 inf2.xl 或者 inf2.8xl；</p>
<p>KeyPairName（可选项），如果要登陆到 Inf2 实例，填写 KeyPairName 名称；</p>
<p>VpcId，选择 VPC；</p>
<p>PublicSubnetId，选择公有子网；</p>
<p>VolumeSize，输入 EC2 实例 EBS 存储卷的大小，最小 80G；</p>
<p>连续点击两次“Next”，点击“Submit”。</p>
<p>4.2 新建 VPC</p>
<p>在 Amazon S3 URL 中输入</p>
<p>https://zz-common.s3.amazonaws.com/tmp/tgiui/20240501/launch_server_new_vpc_ubuntu22.04.yaml</p>
<p>Stack name，填写堆栈名称；</p>
<p>InstanceType，选择 inf2.xl 或者 inf2.8xl；</p>
<p>KeyPairName（可选项），如果要登陆到 Inf2 实例，填写 KeyPairName 名称；</p>
<p>VpcId，保持 New 不变；</p>
<p>PublicSubnetId，保持 New 不变；</p>
<p>VolumeSize，输入 EC2 实例 EBS 存储卷的大小，最小 80G；</p>
<p>连续点击两次“Next”，点击“Submit”。</p>
<ol>
<li>创建堆栈后等待资源创建和启动（约 15 分钟），待堆栈状态显示为“CREATE_COMPLETE”后，点击“Outputs”。点击“键”为“Public endpoint for the web server”相应的“值”位置的 URL（请关闭所有 VPN 连接和防火墙程序）。</li>
</ol>
<p>用户交互界面</p>
<p>部署完成后，用户可以在 PC 端或者手机上访问上述 URL，在页面中，默认会加载 Llama3-8B 模型，用户可以在菜单 Settings 中进行模型切换，在模型列表中选择要激活的模型名称，点击”Activate”按钮，就能够实现切换模型。切换模型需要把新模型重新加载到 Inferentia 2 加速器内存中，这个过程需要 1 分钟左右。在此过程中，用户可以通过点击”Retrieve model status”按钮查看新模型的加载状态，如果状态为”Available”，那么表明新模型已加载成功。</p>
<p>不同模型的效果如下图所示：</p>
<p>在 PC 端的浏览器中运行：</p>
<p>API 接口以及性能测试</p>
<p>方案中使用了 Text Generation Inference 推理服务器，它支持/generate 和/generate_stream 两种接口，默认使用 8080 端口。将下文中的替换为上文部署的 IP 地址就能够进行 API 调用。</p>
<p>/generate 接口用于在服务端生成所有令牌（token）后，一次性返回所有响应到客户端。</p>
<p>curl <IP>:8080/generate \
    -X POST \
    -d '{"inputs":"计算一下北京到上海的距离"}' \
    -H 'Content-Type: application/json'</p>
<p>/generate_stream 通常用于模型输出长度比较大时，通过逐个令牌（token）接收的方式，降低等待延时，增强用户体验。</p>
<p>curl <IP>:8080/generate_stream \
    -X POST \
    -d '{"inputs":"写一篇小学生心理健康的作文，不超过300字。"}' \
    -H 'Content-Type: application/json'</p>
<p>同样，您可以对 API 端点进行性能测试。以 Llama 3 为例，我们在 Inf2.2xlarge 机型上进行了测试，测试工具使用了</p>
<p>Locust</p>
<p>。</p>
<p>测试参数为</p>
<p>input tokens</p>
<p>:</p>
<p>104</p>
<p>max output tokens: 500</p>
<p>并发用户数： 10</p>
<p>持续测试时间：15 分钟</p>
<p>对应的 Prompt 输入为：</p>
<p>"</p>
<p>你是一名小说家，热衷于创意写作和编写故事。</p>
<p>请帮我编写一个故事，对象是 10-12 岁的小学生</p>
<p>故事背景：</p>
<p>讲述一位名叫莉拉的年轻女子发现自己有控制天气的能力。她住在一个小镇上，每个人都互相认识。</p>
<p>其他要求：</p>
<p>-避免暴力，色情，粗俗的语言</p>
<p>-长度要求不少于 500 字</p>
<p>请开始：</p>
<p>"</p>
<p>以下是测试结果，</p>
<p>Average latency：32 s</p>
<p>p50 latency: 33s</p>
<p>p90 latency: 34s</p>
<p>RPM = 0.3 * 60 = 18</p>
<p>TPM = 0.3<em>60</em>(104+500) = 10872</p>
<p>按照美东一（us-east-1）的价格 0.7582$/小时，TPM 为 10872，那么生成 1,000,000 个 token 需要花费 1.16$。计算方法如下：</p>
<p>1,000,000 / 10872 / 60 * 0.7582 = 1.16 $</p>
<p>总结</p>
<p>在本文中，我们介绍了在 AWS 自研芯片上部署流行的大语言模型的方法和示例，使用户不用花费太多精力就能快速体验大语言模型带来的生产效率的提升。Inf2 机型已在多个用户以及场景中得到验证，展现出了强大的性能和广泛的适用性。AWS 也在不断扩展其应用场景和功能，为用户提供高效、经济的计算能力。同时，作为一款自研芯片，并不是所有的模型都能够在 Inf2 机型上运行，用户可以参考</p>
<p>链接</p>
<p>查看在 Inferentia 2 芯片上支持模型的种类以及列表，也欢迎读者联系我们反馈大语言模型的需求或问题。</p>
<p>参考资料</p>
<p>https://aws.amazon.com/ec2/instance-types/inf2/</p>
<p>https://huggingface.co/docs/optimum-neuron/en/index</p>
<p>https://github.com/huggingface/optimum-neuron</p>
<p>https://huggingface.co/docs/text-generation-inference/en/index</p>
<p>https://github.com/huggingface/chat-ui</p>
<p>https://ai.meta.com/blog/meta-llama-3/</p>
<p>https://huggingface.co/NousResearch/Meta-Llama-3-8B</p>
<p>https://huggingface.co/mistralai/Mistral-7B-Instruct-v0.2</p>
<p>https://huggingface.co/codellama/CodeLlama-7b-Instruct-hf</p>
<p>https://huggingface.co/cszhzleo</p>
<p>https://docs.aws.amazon.com/zh_cn/general/latest/gr/aws_service_limits.html</p>
<p>https://locust.io/</p>
<p>本篇作者</p>
<p>张铮</p>
<p>亚马逊云科技机器学习产品技术专家，负责基于亚马逊云科技加速计算和 GPU 实例的咨询和设计工作。专注于机器学习大规模模型训练和推理加速等领域，参与实施了国内多个机器学习项目的咨询与设计工作。</p>
<p>谢川</p>
<p>亚马逊云科技 GenAI 高级解决方案架构师，负责基于亚马逊云的生成式人工智能解决方案的设计，实施和优化。曾在通信，电商，互联网等行业有多年的产研经验，在数据科学，推荐系统，LLM RAG 等方面有丰富的实践经验，并且拥有多个 AI 相关产品技术发明专利。</p>
<p>唐清原</p>
<p>亚马逊云科技高级解决方案架构师，负责 Data Analytic &amp; AIML 产品服务架构设计以及解决方案。10+数据领域研发及架构设计经验，历任 IBM 咨询顾问，Oracle 高级咨询顾问，澳新银行数据部领域架构师职务。在大数据 BI，数据湖，推荐系统，MLOps 等平台项目有丰富实战经验。</p>
<p>史天</p>
<p>亚马逊云科技资深解决方案架构师。拥有丰富的云计算、数据分析和机器学习经验，目前致力于数据科学、机器学习、无服务器等领域的研究和实践。译有《机器学习即服务》《基于 Kubernetes 的 DevOps 实践》《Kubernetes 微服务实战》《Prometheus 监控实战》《云原生时代的 CoreDNS 学习指南》等。</p>
<p>'"`</p>
<p>登录控制台</p>
<p>了解有关 AWS 的信息</p>
<p>什么是 AWS？</p>
<p>什么是云计算？</p>
<p>AWS 包容性、多样性和公平性</p>
<p>什么是 DevOps？</p>
<p>什么是容器？</p>
<p>什么是数据湖？</p>
<p>AWS 云安全性</p>
<p>最新资讯</p>
<p>博客</p>
<p>新闻稿</p>
<p>AWS 资源</p>
<p>入门</p>
<p>培训和认证</p>
<p>AWS 解决方案库</p>
<p>架构中心</p>
<p>产品和技术常见问题</p>
<p>分析报告</p>
<p>AWS 合作伙伴</p>
<p>AWS 上的开发人员</p>
<p>开发人员中心</p>
<p>软件开发工具包与工具</p>
<p>运行于 AWS 上的 .NET</p>
<p>运行于 AWS 上的 Python</p>
<p>运行于 AWS 上的 Java</p>
<p>运行于 AWS 上的 PHP</p>
<p>运行于 AWS 上的 JavaScript</p>
<p>帮助</p>
<p>联系我们</p>
<p>获取专家帮助</p>
<p>提交支持工单</p>
<p>AWS re:Post</p>
<p>Knowledge Center</p>
<p>AWS Support 概览</p>
<p>法律人员</p>
<p>亚马逊云科技诚聘英才</p>
<p>创建账户</p>
<p>Amazon 是一个倡导机会均等的雇主：</p>
<p>反对少数族裔、妇女、残疾人士、退伍军人、性别认同和性取向歧视。</p>
<p>语言</p>
<p>عربي</p>
<p>Bahasa Indonesia</p>
<p>Deutsch</p>
<p>English</p>
<p>Español</p>
<p>Français</p>
<p>Italiano</p>
<p>Português</p>
<p>Tiếng Việt</p>
<p>Türkçe</p>
<p>Ρусский</p>
<p>ไทย</p>
<p>日本語</p>
<p>한국어</p>
<p>中文 (简体)</p>
<p>中文 (繁體)</p>
<p>隐私</p>
<p>|</p>
<p>网站条款</p>
<p>|</p>
<p>Cookie 首选项</p>
<p>|</p>
<p>© 2023, Amazon Web Services, Inc. 或其联属公司。保留所有权利。</p>
<div class="lb-alert lb-alert-info">
    <h4 class="lb-title">功能不可用</h4>

    <p>访问 <a href="#" data-shortbread-modal="true">Cookie 首选项</a>并允许所有 Cookie 以启用此功能。</p>
  </div>