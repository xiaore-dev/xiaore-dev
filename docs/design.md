# 设计手记 · 七层云版画

## 从主页里能读到什么

改版前，同名仓库只有一份默认 README。访客只能看到一句问候，其余内容都在模板注释里。从账户的公开仓库中选出四个项目，整理成首页目录。账号拼写给了封面一个独有的图形线索，项目本身则回答访客接下来可以看什么。[公开仓库列表](https://github.com/x1975544-cloud?tab=repositories)

项目名、链接与功能说明以各仓库的公开内容为依据。介绍的范围限于项目功能，个人履历留给账户主人日后补充。[react-agent](https://github.com/x1975544-cloud/react-agent) · [pix-agent](https://github.com/x1975544-cloud/pix-agent) · [ai-coding](https://github.com/x1975544-cloud/ai-coding) · [SpecFlow](https://github.com/x1975544-cloud/SpecFlow)

## 三个案例带来的取舍

- **Simon Willison 的出版索引。** 发布记录、博客与学习笔记各有独立入口，标题和日期就能说明点开后会看到什么。并列呈现许多长标题需要较宽的阅读空间。这次保留索引的直接性，四个项目逐项向下阅读。[主页源码与效果](https://github.com/simonw/simonw#readme)
- **Tim Burgan 的社区棋盘。** 一盘等待落子的国际象棋给人明确的视觉记忆，点选一步会打开预填的议题，再由工作流更新棋局。这个玩法值得单独占据首屏，也需要持续维护状态。这里让版画承担视觉焦点，把访问项目的动作留给普通链接。[主页源码与玩法](https://github.com/timburgan/timburgan#readme)
- **Kautuk Kundan 的字符画。** 等宽字符拼成的人物让开篇有了自己的语气，随后自然过渡到作品文字。字符之间的相对位置依赖固定列宽，窄屏容易出现横向滚动。独立矢量插画可以保留完整构图，正文仍能自由换行。[主页源码与效果](https://github.com/kautukkundan/kautukkundan#readme)

## 三条设计路线

| 方案 | 视觉表现 | 原创性 | 实用性 | 兼容性 | 维护成本 |
| --- | --- | --- | --- | --- | --- |
| 七层云版画 | 七层轮廓叠成整幅云景，版面有明确重心 | 从账号的七位数字取形，图案随账号而定 | 封面下直接进入四个项目 | 封面等比缩放，文字独立换行 | 低，增删项目只改目录 |
| 项目线路图 | 每个仓库成为一个站点，浏览顺序一目了然 | 路线可根据项目间的真实联系绘制 | 适合讲解有明确依赖或次序的项目 | 窄屏会压缩站名和路线间距 | 中，新增项目时要重排站点 |
| 作品接触印样 | 每个项目配一格缩略图，如同观看一张摄影接触印样 | 可从各项目自己的界面或输出取材 | 适合直接比较图像或界面效果 | 图片可缩放，小尺寸截图容易丢失细节 | 高，界面迭代后需重新制作图版 |

选定**七层云版画**。四个项目各有入口，一张线路图容易暗示它们之间存在固定次序。接触印样更依赖每个项目都有可辨认的截图。版画只取材于名称，在项目目录增减时仍然成立。

## 画面与阅读顺序

封面将账号中的 `cloud` 读作云，将 `1975544` 的七个数字逐一用于七层云廓的形态。米白像未着墨的纸，墨色压住轮廓，青绿铺开层次，少量朱红牵引视线。画面采用静帧，云层的起伏与疏密已经足以表达流动感。

下方目录使用 GitHub 原生文字，每个项目的名称本身就是入口。封面带有自己的纸色与墨色，在深浅背景上都能保留套色关系。正文颜色与字号跟随 GitHub 主题，仓库内的图片可使用相对路径引用。[GitHub 图片与替代文字](https://docs.github.com/en/get-started/writing-on-github/getting-started-with-writing-and-formatting-on-github/basic-writing-and-formatting-syntax#images)

GitHub 会在符合条件的同名公开仓库中读取根目录的非空 README。案例只用于研究构图、信息组织和交互方式，封面图形在本仓库独立绘制。[GitHub 个人主页 README 说明](https://docs.github.com/en/account-and-profile/how-tos/profile-customization/managing-your-profile-readme#prerequisites)

## 实现与预览

桌面封面为 1120 × 440。手机封面为 500 × 475，保留字号层次，把云版移到标题下方。README 通过 `<picture>` 在视口宽度不超过 600 px 时选择手机构图，内层 `<img>` 提供横版后备图。米白纸张在两种主题中使用同一套油墨，正文、链接和标题分隔线跟随 GitHub 主题。[GitHub 的 picture 示例](https://docs.github.com/en/get-started/writing-on-github/getting-started-with-writing-and-formatting-on-github/quickstart-for-writing-on-github#adding-an-image-to-suit-your-visitors)

在 VS Code 中打开根目录的 [README](../README.md)，运行「Markdown: Open Preview to the Side」。把预览面板收窄到 600 px 以下可查看手机排版，切换编辑器的深浅主题可检查正文对比。也可直接用浏览器打开[横版封面](../assets/cloud-press.svg)或[手机版封面](../assets/cloud-press-mobile.svg)，放大查看刻纹。本地编辑器和 GitHub 的文字间距、链接样式可能略有不同。

## 后续维护

| 要修改的内容 | 位置与做法 |
| --- | --- |
| 项目名称、排序或介绍 | 编辑根目录的 `README.md`。每项包含一个仓库链接和一句可从该仓库核实的说明。 |
| 项目图标 | 编辑 `assets/projects/` 下对应的 SVG。画布为 54 × 48，名称已在相邻链接中，图标使用空替代文本。 |
| 云版轮廓、颜色或布局 | 编辑 [print_cloud.py](../scripts/print_cloud.py)。`CLOUD` 定义共用版形，`DIGITS` 为七位制版参数，文件顶部是主色常量。 |
| 重新出图 | 在仓库根目录运行 `python3 scripts/print_cloud.py`，同时更新两张封面。直接修改生成的 SVG 会在下次出图时被覆盖。 |

四枚图标和封面的路径均在本仓库内绘制，字体由设备本地的衬线和等宽字体提供。生成器只用 Python 标准库；访问主页只需加载选中的封面和四枚图标。日常更新项目目录无须运行脚本或配置 GitHub Actions。
