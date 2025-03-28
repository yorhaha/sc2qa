# SC2QA: StarCraft II Domain Knowledge Benchmark

[中文 README](./README.md)  

## Project Overview  
SC2QA is a large-scale QA dataset (**1,700+ 4-choice questions**) designed to evaluate AI systems' expertise in *StarCraft II*. It covers game mechanics, strategies, lore, and competitive history, catering to researchers, developers, and enthusiasts.

## Data Format  
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

## Evaluation for LLMs

```bash
python test_llm.py --model_name Qwen2.5-7B-Instruct
```

## Contribution Guidelines  
- **Add Questions**: Submit new entries via Pull Requests or Issues (JSON format preferred).  
- **Report Errors**: Open an Issue if you find inaccuracies.  
- **Suggest Categories**: Propose new tags like "Economy Management" or "Co-op Missions". 