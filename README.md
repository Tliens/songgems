# SongGems — Free CC Music Player & Discovery

免费在线音乐播放器：全部曲目来自 [Jamendo](https://www.jamendo.com/) 官方公开 API，
由独立音乐人以 Creative Commons 授权发布——搜索、播放队列、收藏与歌单（本地存储），
逐曲展示授权徽标与署名链接；默认过滤 NC（非商业）曲目，未来商业化也安全。

单文件 `index.html`，零外部 JS 依赖、零构建。线上：<https://songgems.kuige.me/>

## 接入自己的 API key

整站通过 Jamendo 官方 API 流式播放（不转存任何音频文件）：

1. 在 <https://developer.jamendo.com/v3.0/apps> 免费注册一个应用，拿到 `client_id`
2. 二选一：
   - 写进 `index.html` 顶部的 `JAMENDO_CLIENT_ID` 常量（对所有访客生效，推荐）
   - 或访客在页面 ⚙ 设置里自己粘贴（只存浏览器 localStorage）

## 本地预览 / 测试

```bash
python3 -m http.server 8979
# http://localhost:8979/?mock=1  ← 内置示例曲目，无需 key 即可体验完整 UI 与播放
```

## 技术要点

- 署名内建：`license_ccurl` 解析为 CC BY / BY-SA / CC0 / NC 徽标并链接授权全文
- NC 过滤：请求带 `ccnc=false` + 客户端按 license URL 二次校验（纵深防御）
- 亮暗主题（auto/light/dark）、中英双语（`?lang=` 深链）、Media Session 锁屏控制
- 无限滚动分页（IntersectionObserver + scroll 兜底）、骨架屏加载
- 点艺术家名直达搜索；分享当前曲目（Web Share API → 剪贴板兜底）
- 会话恢复：回到站点接着上次听（不自动播放、进度还原）；footer 常驻反馈/下架入口
- `?mock=1` 示例模式：内置 80 首演示曲目（SoundHelix 测试音频），用于无 key 冒烟测试

Part of [kuige.me](https://kuige.me/)
