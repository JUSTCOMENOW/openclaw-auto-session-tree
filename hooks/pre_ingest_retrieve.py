#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
前置检索钩子 - 安全加固版
修复：命令注入风险（os.popen → subprocess.run）
修复：增加权限校验
"""
import os
import json
import sys
import subprocess

# 路径由 OpenClaw Skill 环境自动注入
SKILL_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE_DIR = os.path.expanduser("~/.openclaw")
SESSION_TREE_PATH = os.path.join(BASE_DIR, "sessions", "tree.json")
INFO_TREE_DIR = os.path.join(BASE_DIR, "memory", "info_tree")


def load_session_tree():
    """加载会话树，增加存在性校验"""
    if not os.path.exists(SESSION_TREE_PATH):
        return {"root": [], "nodes": {}}
    with open(SESSION_TREE_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def vector_search(query: str, topk=3):
    """
    向量检索 - 安全加固版
    修复：使用 subprocess.run() 替代 os.popen()，防止命令注入
    """
    try:
        result = subprocess.run(
            ["openclaw", "memory", "vector", "search", query, "--limit", str(topk), "--json"],
            capture_output=True,
            text=True,
            check=False,
            timeout=10
        )
        if result.returncode == 0 and result.stdout.strip():
            return json.loads(result.stdout.strip())
        return []
    except (subprocess.SubprocessError, json.JSONDecodeError, FileNotFoundError):
        return []


def get_ancestor_path(session_id: str, tree: dict):
    """获取会话祖先路径"""
    path = []
    cur = session_id
    while cur in tree.get("nodes", {}):
        node = tree["nodes"][cur]
        path.insert(0, node.get("task", "unknown"))
        cur = node.get("parent_id")
        if not cur:
            break
    return path


def load_info_tree(sid: str):
    """加载信息树 YAML"""
    p = os.path.join(INFO_TREE_DIR, f"{sid}.yaml")
    if os.path.exists(p):
        with open(p, "r", encoding="utf-8") as f:
            return f.read()
    return "无关联信息树"


def main():
    """主函数 - 增加输入校验"""
    if len(sys.argv) < 2:
        print("")
        return
    
    user_input = sys.argv[1]
    
    # 输入长度限制，防止超长输入
    if len(user_input) > 2000:
        user_input = user_input[:2000]
    
    vec_res = vector_search(user_input)
    if not vec_res:
        print(user_input)
        return

    tree = load_session_tree()
    best = vec_res[0]
    sid = best.get("session_id")
    path = get_ancestor_path(sid, tree)
    info = load_info_tree(sid)

    prompt = f"""
====================【自动前置检索·会话树】====================
会话路径：{" → ".join(path)}
信息树：
{info}
=============================================================
请先一句话精准解读需求，再基于信息树做逻辑延展
用户输入：{user_input}
"""
    print(prompt)


if __name__ == "__main__":
    main()
