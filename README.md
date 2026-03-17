# OpenClaw Auto Session Tree Skill

✨ 全自动会话树 | 向量 ID 配对 | 对话前检索解读 | 信息树延展 | 自动压缩

## 功能特性

- ✅ 对话前自动向量检索
- ✅ 自动构建父子会话树
- ✅ Token 阈值自动压缩
- ✅ 结构化信息树自动延展
- ✅ 全链路决策可回溯

## 一键安装

### 从 GitHub 安装
```bash
# 替换为你的 GitHub 用户名
openclaw skill install github:king/openclaw-auto-session-tree
```

### 启用 Skill
```bash
openclaw skill enable auto-session-tree
```

### 初始化
```bash
openclaw run skill auto-session-tree skill:init
```

### 重启网关
```bash
openclaw gateway restart
```

### 创建会话
```bash
/new --system auto-session-tree/prompts/system_infotree.txt
```

## 内置命令

| 命令 | 描述 |
|------|------|
| `session:tree` | 查看会话树 |
| `session:trace <id>` | 回溯会话逻辑链 |
| `info:search <kw>` | 搜索信息树关键词 |
| `vector:rebuild` | 重建向量索引 |
| `skill:init` | 初始化目录结构 |

## 升级 & 卸载

### 升级
```bash
openclaw skill update github:king/openclaw-auto-session-tree
```

### 卸载
```bash
openclaw skill uninstall auto-session-tree
```

## 安全说明

- 本技能已修复命令注入风险（使用 `subprocess.run()` 替代 `os.popen()`）
- 增加输入长度限制与权限校验
- 建议在沙箱环境中运行

## License

MIT License
