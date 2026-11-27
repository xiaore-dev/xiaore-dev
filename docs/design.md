# XIAORE / AGENT LAB · 第二期

[完整动态预览](../preview.html) · [桌面截图](screenshots/desktop.png) · [手机截图](screenshots/mobile.png) · [两代封面对照](screenshots/covers.png)

## 封面选型

先把三个候选装置画成同尺度的动态小样，观察它们如何起伏、聚合，以及运动停止后是否仍然容易辨认。[三个动态构图小样](core-studies.svg)

| 构图 | 运动方式 | 小尺寸下的取舍 |
| --- | --- | --- |
| A · Phase Loom，相位织机 | 蓝青折带绕同一孔隙交错，前后两层各有相位 | 四个伸出的带端形成 Xiaore 的首字母 X。选用此案，静帧也能承担个人标记的作用 |
| B · Axial Stack，悬浮晶片 | 五层薄片沿竖轴分开、合拢，透出中央晶孔 | 层间空隙容易读懂，收拢后外形接近常见芯片 |
| C · Branch Field，分叉粒子场 | 两簇粒子沿枝状路径从中心发散，再向中心收束 | 聚散时的节奏鲜明，窄屏下外围细枝容易合成一团 |

## V1 → V2

| 部位 | V1 | V2 |
| --- | --- | --- |
| 封面 | 蓝色经纬球与飞行轨迹 | 两条带面围住一枚晶核。按深度绘制明暗面和切面，独立轨道、碎粒与脉冲参与同一构图 |
| 字标 | 整行粗体文字叠加瞬时错位 | 单独绘制首字母 X，在交点嵌入一小段蓝色。低频色偏只经过狭窄的字面切片 |
| 阅读顺序 | 五组标题、说明和插图 | 作者短介和可点击的页内目录。章节号进入图版本身，控制面和观察面交替左右排布 |
| 01 · Intelligence Loop | 五枚并列的流程图标 | 五个有序模块与立体控制核交换脉冲，回传线路闭合。「Concept study」标明其概念性质 |
| 02 · Technology Radar | 俯视圆盘与外部引线 | 三层倾斜的观测面共享投影，扫描扇面到达节点后触发跨层传输。A–G 对应七项研究方向 |
| 03 · Development Environment | 四个独立图标单元 | Python、TypeScript、Pydantic 和 Playwright 排成两条紧凑的母线，分别标出语言和工具 |
| 04 · Digital Garden | 两个独立光点经过蓝色折叶 | 同一波信号依次到达三个分叉，分向五片叶子。整幅图和目录中的域名都可进入博客 |

持续使用冷白、科技蓝和科技青。大字与实体色块提供第一层轮廓，投影和局部拓扑交代前后关系，细线承担轨迹与索引。标题色偏只占很小面积。雷达七个方向位于相同的模型半径，透视造成的屏幕距离差不承载技术评分。页尾沿用 **Build. Learn. Iterate.**。

## 预览与维护

在浏览器打开根目录的 `preview.html` 即可离线播放。本地正文外框最大宽度为 900 px。将窗口收窄到 640 px 或以下会选用手机版核心、控制面、雷达和技术矩阵。选择 **Dark** 可检查深色背景，勾选 **Still frames** 或启用系统「减少动态效果」可查看静帧。

| 位置 | 用途 |
| --- | --- |
| `README.md` | 作者介绍、章节目录、图片选择、替代文字和博客链接 |
| `scripts/draw_hero.py` | X 形装置的投影、着色、遮挡、运动与两版封面排印 |
| `scripts/draw_diagrams.py` | 运行循环、研究方向和开发环境的布局与动画 |
| `assets/lab/` | 动态图版。分割线、花园和页脚直接在各自的 SVG 内编辑 |
| `assets/lab/still/` | 由同一套几何与文字生成的无动画图版 |
| `scripts/build_preview.py` | 生成静帧，再将 README 正文嵌入本地预览 |
| `docs/core-studies.svg`、`docs/screenshots/` | 三个构图小样与供审阅的 PNG，访客打开个人主页时无需下载 |

在仓库根目录依次运行以下命令即可重建。只改 README 或手绘 SVG 时，运行最后一条即可。截图记录的是本次审阅版本，修改版面后需重新截图。

```sh
python3 scripts/draw_hero.py
python3 scripts/draw_diagrams.py
python3 scripts/build_preview.py
```

脚本只需要 Python 标准库。静帧保留图形元素的底色、位置、轮廓和文字，移除动画与标有 `data-motion-only="true"` 的图层。这样可以单独检查暗色环境中的浅色图版、移动端排版和无动态构图。

## GitHub 渲染边界

正文使用 GitHub 支持的 HTML、仓库相对路径和图片替代文字。图版通过 `<picture>` 和后备 `<img>` 选择。SVG 在图片上下文中播放，动画、路径与样式均在文件内部。页内链接和博客入口由 README 的原生链接承担。只有本地预览外壳使用脚本来切换主题、静帧。[GitHub 响应式图片示例](https://docs.github.com/en/get-started/writing-on-github/getting-started-with-writing-and-formatting-on-github/quickstart-for-writing-on-github#example-of-a-responsive-image) · [GitHub 自定义锚点](https://docs.github.com/en/get-started/writing-on-github/getting-started-with-writing-and-formatting-on-github/basic-writing-and-formatting-syntax#custom-anchors) · [浏览器的 SVG 图片模式](https://developer.mozilla.org/en-US/docs/Web/SVG/Guides/SVG_as_an_image)

截图取自本地 Chrome 中的 README 正文。GitHub 站点的样式、图片代理缓存以及不同客户端的动画支持仍以发布后的实际页面为准。

已读取 GitHub 当前发布的同名仓库 HTML。站点保留了 640 px 窄屏条件、减少动态效果条件、两者的组合条件和后备图片，并将相对路径重写为仓库的 raw URL。正文链接和包裹插画的博客链接也都得到保留。V2 沿用这一图片结构。[当前公开仓库](https://github.com/xiaore-dev/xiaore-dev)

## 本次验收

- 在 Chrome 158 的图片上下文中，对七个可见组件分别取帧比较。常规模式下七个组件均有可测的帧间变化，模拟系统减少动态效果后，七个组件都选中静帧，取样期间像素保持一致。
- 已检查 1280、375 和 320 px 视口的滚动宽度、图片加载、章节定位与博客入口。四组窄屏图版正确切换。预览中的深浅主题和手动静帧均可恢复到原设置。
- 七个动态组件合计约 126.5 KB，静帧合计约 114 KB，均按源文件字节数计算。已解析 22 张组件 SVG 及构图小样，检查所有内部引用与 README 图片路径。连续重建得到相同的输出。
