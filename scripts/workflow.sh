#!/bin/bash
# workflow.sh — AI 全栈开发工作流 v6
# 用法: source workflow.sh <stage>
# 依赖: CC Switch 管理模型供应商
# 模型: DeepSeek V4 Pro（主力）+ MiMo V2.5 Pro（前端/长上下文/交叉审查）

case "$1" in
  # ── 规划层 → DeepSeek ──
  "-1"|"inspire")   echo "🔵 CC Switch 切到 DeepSeek V4 Pro" ;;
  "0"|"require")    echo "🔵 CC Switch 切到 DeepSeek V4 Pro" ;;
  "1"|"spec")       echo "🔵 CC Switch 切到 DeepSeek V4 Pro" ;;
  "2"|"tech")       echo "🔵 CC Switch 切到 DeepSeek V4 Pro" ;;
  "3"|"api")        echo "🔵 CC Switch 切到 DeepSeek V4 Pro" ;;

  # ── 执行层 ──
  "4"|"backend")    echo "🔵 CC Switch 切到 DeepSeek V4 Pro" ;;
  "6"|"e2e"|"test"|"verify") echo "🔵 CC Switch 切到 DeepSeek V4 Pro" ;;
  "8"|"deploy")     echo "🔵 CC Switch 切到 DeepSeek V4 Pro" ;;
	  "9"|"retro")      echo "🔵 CC Switch 切到 DeepSeek V4 Pro | 复盘" ;;
  "infra")          echo "🔵 CC Switch 切到 DeepSeek V4 Pro" ;;

  # ── 前端/视觉 → MiMo（Agent 全球开源第1 + 1M上下文） ──
  "5"|"frontend")   echo "🟣 CC Switch 切到 MiMo V2.5 Pro | 前端生成" ;;
  "7"|"visual")     echo "🟣 CC Switch 切到 MiMo V2.5 Pro | 视觉打磨" ;;

  # ── 横切 ──
  "review")         echo "🟣 CC Switch 切到 MiMo V2.5 Pro | 交叉审查（DS写→MiMo审）" ;;
  "rescue")         echo "🔵 CC Switch 切到 DeepSeek V4 Pro" ;;

  # ── 轻量 → DeepSeek V4 Flash（如果有）或 MiMo 标准版 ──
  "quick")          echo "⚪ CC Switch 切到 DeepSeek V4 Flash（或 MiMo 标准版 ¥2/M）" ;;

  *)
    echo "═══════════════════════════════════"
    echo "  workflow.sh v6 — 双模型分工"
    echo "═══════════════════════════════════"
    echo ""
    echo "  DeepSeek V4 Pro（主力）:"
    echo "    规划/需求/Spec/API/后端/验证/部署/复盘"
    echo ""
    echo "  MiMo V2.5 Pro（前端+审查）:"
    echo "    前端生成/视觉打磨/交叉审查"
    echo "    优势: Agent全球开源第1 + 1M上下文"
    echo ""
    echo "  轻量: DeepSeek Flash / MiMo 标准版"
    echo ""
    echo "  用法: source workflow.sh <stage>"
    ;;
esac
