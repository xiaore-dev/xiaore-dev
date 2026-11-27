# Xiaore / Agent Lab 设计与维护

## 从账号到封面

这次改版以 Xiaore、个人博客和技术探索方向为内容来源。此前 README 的入口按仓库组织，本版把入口改为个人介绍、两张概念图、开发环境和博客。旧素材保留在原处，新主页和本地预览只引用 `assets/lab/`。

| 初选构图 | 阅读体验 | 取舍 |
| --- | --- | --- |
| 偏心轨道图册 | 左侧先读 Xiaore，再沿基线读到右侧的旋转球体 | 采用。标题与复杂线框各有空间，手机上可以上下重排 |
| 同心仪表盘 | 球体占中心，名称与方向沿外圈分布 | 环绕构图有空间感，长标题需要转向阅读 |
| 信号剖面 | 倾斜的扫描带穿过标题和球体 | 速度感强，窄屏裁切会削弱姓名的完整轮廓 |

构图按瑞士平面设计约 50%、控制台约 30%、赛博朋克约 20% 把握。大字、非对称平衡和留白控制第一眼的阅读顺序。工程编号、经纬线与扫描定位属于第二层。粉色只在低频的标题错位中短暂出现。

## 颜色与动效

| 用途 | 颜色 |
| --- | --- |
| 纸面与图层 | 冷白 `#F6F8FA`、纯白 `#FFFFFF` |
| 主次文字 | 墨蓝 `#182433`、灰蓝 `#64748B` |
| 结构与反馈 | 科技蓝 `#2457E6`、科技青 `#009F91` |
| 细线与瞬时强调 | 边框 `#D7E0EA`、故障粉 `#E88DAB` |

- **Hero** 由三维经纬线投影出前后半球。球体以 28 秒转一圈，粒子沿 22 秒轨道绕行。网格、扫描线和文字切片分别使用 26、21、13 秒的节奏。角标 FIG. 01 是图版编号。
- **Intelligence Loop** 沿闭合轨道用 10 秒走完感知、推理、行动、观察和返回。信号到达时，相应节点亮起。这是一张原理图。
- **Technology Radar** 用 18 秒扫过七个主题。所有主题处在同一半径上，角度用于区分标签。手机图用字母把点位与下方图例对应起来。
- **Development Environment** 用四枚原创图标区分 Python、TypeScript、Pydantic 和 Playwright。来自账号公开代码中的语言和依赖有据可查。下划线轮流着色，不显示计量值。
- **Digital Garden** 把电路分叉画成折叠的叶片，两束信号从根部走向叶尖。读者可以点击整幅图，也可以直接点击可复制的域名。
- **分割线和页脚** 共用短线和逐段亮起的色块，页尾保留品牌标语。图片拥有固定浅色画布，正文和原生链接跟随 GitHub 的阅读主题。

## 文件与更新

| 位置 | 修改方式 |
| --- | --- |
| `README.md` | 个人资料、段落顺序、博客链接和替代文字的唯一正文来源。仅使用 GitHub 支持的 HTML 标签。 |
| `scripts/draw_hero.py` | 修改球体投影、封面排印和动效参数，同时输出横版和窄屏版。 |
| `scripts/draw_diagrams.py` | 修改运行步骤、雷达方向和开发环境图标，同时生成两种版式。 |
| `assets/lab/` | 各组件的独立动态 SVG。花园、分割线和页脚直接在这里编辑。 |
| `assets/lab/still/` | 无动画的对应 SVG。静态版从同一份几何图形生成。 |
| `scripts/build_preview.py`、`preview.html` | 提取静帧，将 README 正文嵌入本地预览外壳。主题和静帧控件只在本地预览中出现。 |

在仓库根目录运行下列命令可重建所有生成文件，只需要 Python 3 标准库。单独修改 README、分割线、花园或页脚后只需运行最后一条。

```sh
python3 scripts/draw_hero.py
python3 scripts/draw_diagrams.py
python3 scripts/build_preview.py
```

静态版使用 SVG 元素本身的颜色、位置和路径。新增动效时，把初始可读状态写在元素属性上，动画样式放在 SVG 的 `<style>` 或 SMIL 标签里。仅用于传输的粒子组可标记为 `data-motion-only="true"`，出静帧时会移除。

## 预览与兼容性

直接在浏览器打开仓库根目录的 [preview.html](../preview.html)。桌面正文外框上限为 900 px，收窄窗口到 640 px 或以下可切换手机图版。选择 **Dark** 检查深色环境，勾选 **Still frames** 可单独看静态构图。操作系统启用「减少动态效果」时，页面也会自动选择静帧。

README 中只放图片引用、原生文字和链接。动画留在自包含 SVG 内，由图片渲染器播放，字体走本地系统栈。GitHub 文档提供了 picture/source 和后备 img 的写法，浏览器以图片方式加载 SVG 时会限制脚本和外部资源。本设计不需要远程字体、第三方动态图服务、令牌或定时工作流。[GitHub 图片示例](https://docs.github.com/en/get-started/writing-on-github/getting-started-with-writing-and-formatting-on-github/quickstart-for-writing-on-github#adding-an-image-to-suit-your-visitors) · [MDN 对 SVG 图片上下文的说明](https://developer.mozilla.org/en-US/docs/Web/SVG/Guides/SVG_as_an_image)

线上核对时，该账号已有 README 的窄屏 source 条件得到保留，GitHub 将仓库相对路径改写为可访问的原图 URL，公开 SVG 返回 `image/svg+xml`。博客地址返回 HTTP 200。本地预览复用 README 正文与图片，不模拟 GitHub 完整的 HTML 清洗、图片代理或移动客户端。针对通用测试片段的匿名 Markdown API 请求遇到限流。新版实际发布效果要在同名公开仓库的 GitHub 页面上核对。[GitHub 个人主页展示条件](https://docs.github.com/en/account-and-profile/how-tos/profile-customization/managing-your-profile-readme)

### 本次检查

- 在桌面 Chrome 中将七个组件作为 `<img>` 加载，分别截取多帧比较。七个组件均发生变化，其中球体中心的蓝色经纬线也有独立的帧间变化。启用系统级减少动态效果模拟后，七个组件在同一采样区间内的帧间像素差均为零。
- 四组信息量较大的图版各有桌面与手机版。两种屏宽下每次各显示七张图，动态 SVG 合计约 49–51 KB。静态资源含完整几何、文字和替代说明，静帧合计约 35 KB。
- 已检查 22 张 SVG 的 XML、内部引用与本地图片路径，连续重建结果逐字节一致。图中全部字体为系统字体，项目内无需分发字体文件。
- Chrome 整页检查覆盖 1280、375、320 px 三种视口。两个手机宽度的文档均无横向溢出。四个窄版组件全部命中，静帧控件和系统减少动态效果偏好均切换全部七个组件。深色主题下的文字链接和整幅博客入口都保持可访问。
