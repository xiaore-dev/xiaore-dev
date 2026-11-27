# XIAORE / AGENT LAB · 第三期

[离线动态预览](../preview.html) · [桌面截图](screenshots/desktop.png) · [手机截图](screenshots/mobile.png) · [芯片时序实测](screenshots/loop-sequence.png) · [V2 与 V3 封面对照](screenshots/covers.png)

## 从 V2 到 V3

切割 X 字标、蓝青折带和浅底构图延续第二期。第三期把重心放在运动的因果关系上。访客可以在封面看到粒子绕到带面背后，在芯片上跟随同一个输入直到反馈返回，在雷达上看到扫描前缘经过某个方向后发生的回响。

| 部位 | 本期调整 |
| --- | --- |
| Phase Loom | 为折带计算两个完整的三维形态，经透视投影后连续插值。相邻面片共享顶点，开口和截面随曲率一起变化。内外两条轨道把粒子分在带面之前、之后绘制，粒子的大小随深度改变。 |
| 01 · Intelligence Loop | 输入接线、片内三级电路、晶核、输出和反馈首尾相接。左侧阶段名随同一张时序表推进，完成的电路暂时保留亮度，便于回看信号走过的路径。它是一项概念研究。 |
| 02 · Technology Radar | 保留倾斜三层观测面，为扫描前缘加入渐弱的扇形尾迹。节点在对应角度收到扫描时产生外圈回响，随后向下层传递。七个方向位于同一模型半径。 |
| 导航与编排 | 简介压成一句对研究兴趣的说明。三个可点击的索引签分别通往 Loop、Radar 和博客。开发环境及其导航、图形和生成逻辑已移除。Garden 接续为第 03 章。 |
| 03 · Digital Garden 与页脚 | 继续使用折叶电路插画和 **Build. Learn. Iterate.**。花园的分叉传输与页脚的色块回响改用 12 秒周期。桌面主要起笔线约在图宽的 1/28 处。 |

### 运动的层次

12 秒承担一次信号传播，24 秒承担折带形变和雷达扫描，36 秒承担外轨进动和低频字面错位。雷达下层的伴星沿反向轨道用 48 秒走完一周。各 SVG 可独立加载；需要严格衔接的芯片阶段都在同一张图内计时。

| 芯片周期 | 画面事件 |
| --- | --- |
| 0–2.2 秒 | Perceive 接收输入，信号进入芯片的第一个触点。 |
| 2.2–4.4 秒 | Reason 点亮第一段片内电路。 |
| 4.4–6.4 秒 | Act 接续第二段电路。 |
| 6.4–8.4 秒 | Observe 经第三段将信号送到晶核。 |
| 8.4–9.5 秒 | 三段走线保持充能，晶核释放一次向外扩散的脉冲。 |
| 9.5–12 秒 | 输出先沿片内支路到达边缘，10.4 秒后进入外围反馈线，回到同一感知端口。 |

## 预览与验收

用浏览器直接打开根目录的 `preview.html`。收窄窗口到 640 px 或以下可切换手机构图。**Theme** 切换阅读背景，**Still frames** 切换静帧。启用系统「减少动态效果」时会自动选用静态图版。

| 检查 | 本次结果 |
| --- | --- |
| 正文布局和交互 | Chrome 158 下，1280、375 和 320 px 视口均无横向溢出。两个索引签能定位到对应章节，Garden 签和博客插画均可打开博客地址。 |
| 真实图片播放 | 六个动态组件以外链 `<img>` 形式加载，浏览器取帧比较均有像素变化。启用系统减少动态效果后，六张静帧在相同检查中均为零变化。三个导航签本身为静态 SVG。计入导航，单一屏宽选用的常规图形合计约 136 KB，静帧约 91 KB，均按未压缩文件大小计算。 |
| 封面形变 | 折带一个顶点的横坐标在 0、6、12、24 秒分别约为 155.9、148.6、141.3、155.9，完整周期后回到起点。 |
| 芯片时序 | 以 0.5 秒间距检查周期，并额外定位关键时刻。1.25、3.25、5.25、7.25 秒分别只有输入或对应片内支路在传播。8.75 秒各段传输暂停，晶核波前可见。9.75 和 11.25 秒分别进入输出和反馈。六段路径相邻端点的投影接缝误差均为 0 CSS px。 |
| 雷达相位 | 按七个节点的实际方位逐一定位扫描前缘，交会时对应节点均产生回响，信号沿层间路径传播，约 1.2 秒后到达下层。 |

[四个关键时刻的局部截图](screenshots/loop-sequence.png)来自浏览器实际渲染，图上秒数是动画周期内的取样时刻。

### GitHub 兼容性

README 使用原生链接、具名锚点、`<picture>` 和后备 `<img>`。索引签的点击区域由外层链接提供，SVG 只负责绘制；图片各有说明目的地的替代文字。所有运行所需的图形、字体回退和动画样式均可在本地解析。无法插值 SVG 路径的客户端仍可绘制元素自带的静态轮廓。[GitHub 响应式图片示例](https://docs.github.com/en/get-started/writing-on-github/getting-started-with-writing-and-formatting-on-github/quickstart-for-writing-on-github#example-of-a-responsive-image) · [GitHub 自定义锚点](https://docs.github.com/en/get-started/writing-on-github/getting-started-with-writing-and-formatting-on-github/basic-writing-and-formatting-syntax#custom-anchors) · [SVG 图片模式](https://developer.mozilla.org/en-US/docs/Web/SVG/Guides/SVG_as_an_image)

已核对 GitHub 当前公开 V2 的实际 HTML。站点保留窄屏和减少动态效果条件、相对路径后备图、章节锚点与包裹图片的博客链接。V3 沿用这些结构。此次截图和动画测量来自本地浏览器，V3 上线后的站点样式和图片代理效果仍待发布后确认。[公开仓库](https://github.com/xiaore-dev/xiaore-dev)

## 恢复 V2

[V2 恢复包](archive/xiaore-agent-lab-v2.zip)来自改动前已有的提交 `bddd411f1690e0a70ae0c9374952fd0eeac7e4dd`。解压到一个空目录，打开其中的 `preview.html` 即可使用完整 V2。包内含该版 README、全部运行图版、静帧、生成脚本、设计说明和原截图。归档中 32 个文件已与原提交逐一校验，并已在独立目录重建，输出逐字节一致。

## 文件与维护

| 位置 | 用途 |
| --- | --- |
| `README.md`、`assets/lab/nav/` | 个人简介、索引签、跳转地址及图版替代文字 |
| `scripts/draw_hero.py` | 三维带面、轨道、遮挡顺序及桌面和手机构图 |
| `scripts/draw_diagrams.py` | 芯片时序、片内电路、雷达投影及节点响应 |
| `assets/lab/`、`assets/lab/still/` | 主图版与无动画副本。花园、分割线和页脚直接编辑各自的动态 SVG |
| `scripts/build_preview.py`、`preview.html` | 从图形属性生成静帧，用同一份 README 正文生成离线预览 |
| `docs/screenshots/`、`docs/archive/` | 审阅图与独立恢复包，浏览主页时无需下载 |

在仓库根目录重新出图只需要 Python 3 标准库。只改 README 或手绘图形时，运行最后一条命令即可。截图与时序记录对应本次验收版本。

```sh
python3 scripts/draw_hero.py
python3 scripts/draw_diagrams.py
python3 scripts/build_preview.py
```
