# SC2QA: 星际争霸2领域知识测试基准

[English README](./README_en.md)  

## 项目简介  
SC2QA 是一个针对《星际争霸2》领域知识的问答基准测试数据集，包含 **1,700+ 道 4选1选择题**。覆盖游戏机制、战术策略、背景故事、赛事历史等内容，旨在评估和训练 AI 系统对星际争霸2领域的专业知识理解能力。适用于：  
- 学术研究（如游戏 AI、知识图谱、自然语言处理）  
- 玩家知识测评工具开发  
- 星际争霸社区教育与内容创作

## 数据格式  
```json
{
    "document": "# SCV (Legacy of the Void)\n\nSCVUnit Information\nType:Ground Unit\nDescription:Basic worker unit. Can gather resources, build Terran structures, and repair.Built From:Command Center\nCost: Minerals: 50  Vespene Gas: 0  Build Time: 12  Supply: 1\nAttack 1: Fusion Cutter\nTargets:Ground\nDamage:5\nDPS:4.67\nCooldown:1.07\nRange:0.2\nUnit stats\nDefense: Hit Points: 45  Armor: 0 (+1)\nAttributes:Biological, Light, Mechanical\nSight:8\nSpeed:3.94\nCargo size:1",
    "question": "What is the primary function of the SCV unit in StarCraft II?",
    "options": [
        "To serve as a combat unit",
        "To gather resources and build Terran structures",
        "To act as a scout unit",
        "To provide long-range support"
    ],
    "answer": "To gather resources and build Terran structures"
}
```

## 大语言模型评估

```bash
python test_llm.py --model_name Qwen2.5-7B-Instruct
```

## 贡献指南  
- **提交新问题**：通过 Pull Request 或 Issue 提交 JSON 格式的问题条目。  
- **修正错误**：发现答案或描述错误时，请在 Issues 中说明。  
- **分类建议**：可提议新增知识点分类（如“经济管理”或“多人对战模式”）。  