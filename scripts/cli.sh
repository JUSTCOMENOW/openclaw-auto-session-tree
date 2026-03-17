#!/bin/bash
# OpenClaw Auto Session Tree CLI
set -e

BASE_DIR=~/.openclaw
TREE_FILE="$BASE_DIR/sessions/tree.json"
INFO_DIR="$BASE_DIR/memory/info_tree"

init() {
    mkdir -p "$BASE_DIR"/{sessions,memory/info_tree}
    echo '{"root":[],"nodes":{}}' > "$TREE_FILE"
    chmod +x "$(dirname "$0")/../hooks/pre_ingest_retrieve.py"
    echo "✅ auto-session-tree 初始化完成"
}

cmd_tree() {
    if [ ! -f "$TREE_FILE" ]; then
        echo "❌ 会话树不存在，请先执行 skill:init"
        exit 1
    fi
    cat "$TREE_FILE" | jq .
}

cmd_trace() {
    if [ -z "$2" ]; then
        echo "用法：session:trace <会话 ID>"
        exit 1
    fi
    if [ ! -f "$TREE_FILE" ]; then
        echo "❌ 会话树不存在"
        exit 1
    fi
    grep -A 20 "\"$2\"" "$TREE_FILE" || echo "未找到会话 ID: $2"
    if [ -f "$INFO_DIR/$2.yaml" ]; then
        echo "--- 信息树 ---"
        cat "$INFO_DIR/$2.yaml"
    fi
}

cmd_info() {
    if [ -z "$2" ]; then
        echo "用法：info:search <关键词>"
        exit 1
    fi
    if [ ! -d "$INFO_DIR" ]; then
        echo "❌ 信息树目录不存在"
        exit 1
    fi
    grep -r "$2" "$INFO_DIR"/ || echo "未找到匹配项"
}

cmd_rebuild() {
    echo "🔄 重建向量索引..."
    openclaw memory vector index rebuild
    echo "✅ 向量索引重建完成"
}

show_help() {
    echo "OpenClaw Auto Session Tree CLI"
    echo ""
    echo "命令:"
    echo "  skill:init          初始化目录结构"
    echo "  session:tree        查看会话树"
    echo "  session:trace <id>  回溯会话逻辑链"
    echo "  info:search <kw>    搜索信息树关键词"
    echo "  vector:rebuild      重建向量索引"
}

case "$1" in
    init)
        init
        ;;
    tree)
        cmd_tree
        ;;
    trace)
        cmd_trace "$@"
        ;;
    info)
        cmd_info "$@"
        ;;
    rebuild)
        cmd_rebuild
        ;;
    *)
        show_help
        ;;
esac
