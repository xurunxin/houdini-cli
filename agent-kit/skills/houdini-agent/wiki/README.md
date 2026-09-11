# Houdini Agent Wiki

32 个领域入口 · 40 个任务配方 · 81 条来源 · 2026-09-11

先读 [快速上手](quickstart.md)、[CLI 契约](02-cli-contract.md) 和 [已核对工具候选](tool-map.md)。这里只按需阅读，不要求 Agent 预载全库。

## 覆盖等级
`guide`：原理、输入、操作策略与验收；`discovery`：复杂/新领域的路由与继续阅读入口；`recipe-design-not-runtime-tested`：有任务步骤，尚无目标 Houdini 运行证据。示例通过离线检查不等于效果运行通过。

## 领域目录
| 领域 | Skill | 等级 |
| --- | --- | --- |
| [上下文、数据与任务选路](01-mental-model.md) | `houdini-agent` | guide |
| [houdini-cli 会话、工具与安全契约](02-cli-contract.md) | `houdini-agent` | guide |
| [HOM 反射、节点版本与参数发现](03-runtime-discovery.md) | `houdini-agent` | guide |
| [属性、组与几何数据契约](04-attributes.md) | `houdini-sop` | guide |
| [程序化建模、曲线、拓扑与 UV](05-modeling.md) | `houdini-sop` | guide |
| [散布、复制、朝向与打包实例](06-instancing.md) | `houdini-sop` | guide |
| [VEX / VOP：小数据契约到批量计算](07-vex.md) | `houdini-vex` | guide |
| [Volume / VDB / SDF 数据与运算](08-volumes.md) | `houdini-volumes` | guide |
| [时间、反馈、模拟选择与重算](09-time-state.md) | `houdini-simulation` | guide |
| [POP 粒子、属性生命周期与轨迹](10-particles.md) | `houdini-particles` | guide |
| [RBD / Bullet：碎裂、约束、代理与回传](11-rbd.md) | `houdini-rbd` | guide |
| [Vellum：布料、绳索、软体与颗粒](12-vellum.md) | `houdini-vellum` | guide |
| [Pyro：源、字段、模拟与烟火外观](13-pyro.md) | `houdini-pyro` | guide |
| [FLIP、海洋、白水与液体网格](14-flip.md) | `houdini-flip` | guide |
| [MPM、颗粒与其他材料求解器选择](15-mpm.md) | `houdini-mpm` | guide |
| [地形、侵蚀、遮罩与散布](16-terrain.md) | `houdini-terrain` | guide |
| [KineFX：骨架、重定向与变形数据](17-kinefx.md) | `houdini-character` | guide |
| [APEX：角色图与动画系统入口](18-apex.md) | `houdini-character` | discovery |
| [Crowds：Agent、状态与动作混合](19-crowds.md) | `houdini-character` | discovery |
| [毛发、羽毛与肌肉工作流导航](20-groom.md) | `houdini-character` | discovery |
| [Solaris / USD：场景组装、层与绑定](21-solaris.md) | `houdini-solaris` | guide |
| [MaterialX、纹理、颜色空间与Lookdev](22-materials.md) | `houdini-render` | guide |
| [Karma / ROP 渲染与镜头级验收](23-render.md) | `houdini-render` | guide |
| [Copernicus 与旧 COPs：图像和纹理](24-copernicus.md) | `houdini-copernicus` | guide |
| [CHOP：动画通道、信号和音频驱动](25-chops.md) | `houdini-chops` | guide |
| [PDG / TOPs：批量任务、变体与依赖](26-pdg.md) | `houdini-pdg` | guide |
| [缓存、导入导出、路径与交付](27-cache-io.md) | `houdini-pdg` | guide |
| [HDA、Labs 与 Houdini Engine / Unreal](28-hda-engine.md) | `houdini-hda` | guide |
| [诊断、性能与最小复现](29-debug-performance.md) | `houdini-debug` | guide |
| [ML、Gaussian Splats 与新功能检索](30-ml-emerging.md) | `houdini-agent` | discovery |
| [技术、时间与视觉三层验收](31-acceptance.md) | `houdini-debug` | guide |
| [来源、版本适配与知识更新机制](32-maintenance.md) | `houdini-agent` | guide |

## 具体任务配方
每个配方说明最小网络意图、需要现场查询的参数、执行和验收；不是硬编码的可执行节点清单。

- [在独立任务空间验证创建、连线与 cook](recipes/sop-smoke.md)
- [节点参数设置部分失败后的恢复](recipes/parameter-failure.md)
- [沿曲线生成稳定的管线或线缆](recipes/tube.md)
- [在表面散布具有稳定方向和大小的实例](recipes/scatter.md)
- [把参考曲面的颜色传给目标点](recipes/surface-sample.md)
- [可重复的 rest 空间噪声形变](recipes/rest-noise.md)
- [用 SDF 合成壳体或融合形状](recipes/sdf-shell.md)
- [构造可检查的 curl 速度场](recipes/point-advection.md)
- [按稳定 id 生成粒子轨迹](recipes/particle-trail.md)
- [刚体碰撞与约束破裂的最小测试](recipes/rbd-impact.md)
- [将代理刚体模拟回传到高模](recipes/rbd-transfer.md)
- [诊断布料穿透而不盲目增大刚度](recipes/cloth-penetration.md)
- [绳索/枝条的柔性运动](recipes/rope.md)
- [约束驱动的充气或软壳原型](recipes/cloth-inflate.md)
- [烟雾不可见的分层排查](recipes/smoke-invisible.md)
- [受控的短时爆发烟火原型](recipes/pyro-burst.md)
- [液体漏水或流失的诊断](recipes/flip-leak.md)
- [FLIP 粒子到时间稳定表面](recipes/fluid-surface.md)
- [雪沙材料的小体积 MPM 测试](recipes/mpm-material.md)
- [用坡度/地貌遮罩控制植被](recipes/terrain-mask.md)
- [选择 SOP 或 Copernicus 地形路径](recipes/terrain-cop-route.md)
- [角色导入后的骨架与 rest 验收](recipes/kinefx-import.md)
- [重定向与根运动排错](recipes/retarget.md)
- [SOP 资产进入 Solaris 的边界验证](recipes/usd-import.md)
- [USD 材质绑定不生效的排查](recipes/usd-binding.md)
- [用非破坏 USD 变体组织资产](recipes/usd-variants.md)
- [MaterialX 法线贴图与颜色语义验证](recipes/materialx-normal.md)
- [在全序列前执行可比的单帧预览](recipes/render-one-frame.md)
- [渲染动画闪烁的分层定位](recipes/render-flicker.md)
- [Copernicus 程序贴图的导出验收](recipes/texture-output.md)
- [音频或信号驱动几何参数](recipes/audio-drive.md)
- [参数 Wedge 的安全批量产出](recipes/wedge.md)
- [检查缓存序列完整性并读回](recipes/cache-readback.md)
- [将已验证网络封装为可维护 HDA](recipes/hda-package.md)
- [Houdini Engine / Unreal 交付前检查](recipes/unreal-delivery.md)
- [CLI 超时后的不重放恢复流程](recipes/timeout-recovery.md)
- [植物/根系的可控生长可视化原型](recipes/growth-visual.md)
- [科技数据流与网络路径动画](recipes/data-lines.md)
- [反射/折射光路线的学习与原型入口](recipes/procedural-laser.md)
- [Agent 输出交付前的证据审查](recipes/review-delivery.md)

## 其他入口
[源码示例与前提](../examples/README.md) · [现场测试矩阵](target-smoke.md) · [来源目录](sources.md) · [验收模板](../templates/acceptance.json)
