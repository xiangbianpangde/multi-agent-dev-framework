#!/bin/bash
# 快速启动脚本

set -e

echo "======================================"
echo "  多Agent项目开发工具集"
echo "======================================"
echo ""

# 检查Python
if ! command -v python3 &> /dev/null; then
    echo "错误: 需要安装Python 3"
    exit 1
fi

# 显示帮助
show_help() {
    echo "用法: ./run.sh [命令]"
    echo ""
    echo "命令:"
    echo "  project <name>     创建新项目"
    echo "  agent <id> <name> <role>  创建Agent"
    echo "  skill <name> <desc>       创建Skill"
    echo "  list               列出可用资源"
    echo "  help               显示帮助"
    echo ""
    echo "示例:"
    echo "  ./run.sh project my-project"
    echo "  ./run.sh agent my_agent '我的Agent' execution"
    echo "  ./run.sh skill code_review '代码审查'"
}

case "$1" in
    project)
        if [ -z "$2" ]; then
            echo "错误: 请提供项目名称"
            exit 1
        fi
        python3 cli.py project --name "$2" --init-git
        ;;
    agent)
        if [ -z "$2" ] || [ -z "$3" ] || [ -z "$4" ]; then
            echo "错误: 用法: ./run.sh agent <id> <name> <role>"
            exit 1
        fi
        python3 cli.py agent --id "$2" --name "$3" --role "$4"
        ;;
    skill)
        if [ -z "$2" ] || [ -z "$3" ]; then
            echo "错误: 用法: ./run.sh skill <name> <description>"
            exit 1
        fi
        python3 cli.py skill --name "$2" --description "$3"
        ;;
    list)
        python3 cli.py list
        ;;
    help|--help|-h|"")
        show_help
        ;;
    *)
        echo "未知命令: $1"
        show_help
        exit 1
        ;;
esac