"""
知识图谱关系定义

定义知识图谱中所有关系类型
"""
from enum import Enum


class RelationType(Enum):
    """关系类型"""
    
    # 项目关系
    HAS_AGENT = "HAS_AGENT"              # Project -> Agent
    USES_SKILL = "USES_SKILL"            # Agent -> Skill
    DEPENDS_ON = "DEPENDS_ON"            # Agent -> Agent
    CALLS = "CALLS"                      # Agent -> Agent
    
    # 决策关系
    MADE_DECISION = "MADE_DECISION"      # Agent -> Decision
    DECISION_AFFECTS = "AFFECTS"         # Decision -> Agent/Project
    BASED_ON = "BASED_ON"                # Decision -> Knowledge
    ALTERNATIVE_TO = "ALTERNATIVE_TO"    # Decision -> Decision
    
    # 模式关系
    APPLIES_PATTERN = "APPLIES_PATTERN"  # Project -> Pattern
    PATTERN_USED_IN = "USED_IN"          # Pattern -> Project
    SOLVES_PROBLEM = "SOLVES"            # Pattern -> Problem
    REQUIRES_SKILL = "REQUIRES"          # Pattern -> Skill
    
    # 学习关系
    LEARNS_FROM = "LEARNS_FROM"          # Agent -> Problem
    IMPROVES_SKILL = "IMPROVES"          # Agent -> Skill
    REFERENCES = "REFERENCES"            # Decision/Knowledge -> Knowledge
    
    # 继承关系
    EXTENDS = "EXTENDS"                  # Agent -> Agent
    INHERITS = "INHERITS"                # Skill -> Skill
    
    # 关联关系
    RELATED_TO = "RELATED_TO"            # Knowledge -> Knowledge
    CAUSED_BY = "CAUSED_BY"              # Problem -> Problem
    FOLLOWS = "FOLLOWS"                  # Decision -> Decision
    
    # 项目流程关系
    PRECEDES = "PRECEDES"                # Task -> Task
    BLOCKS = "BLOCKS"                    # Problem -> Task
    
    # 知识来源关系
    DERIVED_FROM = "DERIVED_FROM"        # Knowledge -> Project/Decision
    APPLIES_TO = "APPLIES_TO"            # Knowledge -> Scenario


# 关系属性模板
RELATION_PROPERTIES = {
    RelationType.HAS_AGENT: {
        "added_at": "datetime",
        "role": "string"  # primary, secondary
    },
    RelationType.USES_SKILL: {
        "proficiency": "float",  # 0-1
        "last_used": "datetime"
    },
    RelationType.DEPENDS_ON: {
        "dependency_type": "string",  # requires, optional
        "description": "string"
    },
    RelationType.MADE_DECISION: {
        "timestamp": "datetime",
        "context": "string"
    },
    RelationType.APPLIES_PATTERN: {
        "applied_at": "datetime",
        "customizations": "string"
    },
    RelationType.SOLVES_PROBLEM: {
        "effectiveness": "float",  # 0-1
        "notes": "string"
    },
    RelationType.REFERENCES: {
        "relevance": "float",  # 0-1
        "citation_type": "string"  # direct, indirect
    }
}


def get_relation_description(relation_type: RelationType) -> str:
    """获取关系描述"""
    descriptions = {
        RelationType.HAS_AGENT: "项目包含Agent",
        RelationType.USES_SKILL: "Agent使用技能",
        RelationType.DEPENDS_ON: "Agent依赖关系",
        RelationType.CALLS: "Agent调用关系",
        RelationType.MADE_DECISION: "Agent做出决策",
        RelationType.DECISION_AFFECTS: "决策影响范围",
        RelationType.BASED_ON: "基于知识",
        RelationType.ALTERNATIVE_TO: "替代方案",
        RelationType.APPLIES_PATTERN: "应用模式",
        RelationType.PATTERN_USED_IN: "模式使用于",
        RelationType.SOLVES_PROBLEM: "解决问题",
        RelationType.REQUIRES_SKILL: "需要技能",
        RelationType.LEARNS_FROM: "从问题学习",
        RelationType.IMPROVES_SKILL: "提升技能",
        RelationType.REFERENCES: "参考引用",
        RelationType.EXTENDS: "扩展",
        RelationType.INHERITS: "继承",
        RelationType.RELATED_TO: "相关知识",
        RelationType.CAUSED_BY: "导致原因",
        RelationType.FOLLOWS: "后续决策",
        RelationType.PRECEDES: "前置任务",
        RelationType.BLOCKS: "阻塞",
        RelationType.DERIVED_FROM: "来源于",
        RelationType.APPLIES_TO: "适用于"
    }
    return descriptions.get(relation_type, "未知关系")