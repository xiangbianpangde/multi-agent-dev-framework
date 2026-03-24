"""
知识图谱核心实现

提供Neo4j知识图谱的完整操作接口
"""
from typing import List, Optional, Dict, Any
from datetime import datetime
import logging
import json

from .nodes import (
    BaseNode, ProjectNode, AgentNode, SkillNode,
    DecisionNode, PatternNode, ProblemNode, KnowledgeNode
)
from .relations import RelationType, get_relation_description

logger = logging.getLogger(__name__)


class KnowledgeGraph:
    """
    知识图谱管理器
    
    使用Neo4j存储和查询知识图谱
    """
    
    def __init__(self, uri: str = "bolt://localhost:7687",
                 user: str = "neo4j",
                 password: str = "password"):
        """
        初始化知识图谱
        
        Args:
            uri: Neo4j连接URI
            user: 用户名
            password: 密码
        """
        self.uri = uri
        self.user = user
        self.password = password
        self._driver = None
    
    def connect(self):
        """建立连接"""
        try:
            from neo4j import GraphDatabase
            self._driver = GraphDatabase.driver(
                self.uri,
                auth=(self.user, self.password)
            )
            logger.info(f"知识图谱连接成功: {self.uri}")
        except ImportError:
            logger.warning("Neo4j驱动未安装，使用内存存储模式")
            self._driver = None
        except Exception as e:
            logger.error(f"知识图谱连接失败: {e}")
            self._driver = None
    
    def close(self):
        """关闭连接"""
        if self._driver:
            self._driver.close()
    
    # ========== 节点操作 ==========
    
    def create_node(self, node: BaseNode) -> bool:
        """
        创建节点
        
        Args:
            node: 节点对象
            
        Returns:
            是否创建成功
        """
        if not self._driver:
            logger.warning("Neo4j未连接，跳过节点创建")
            return False
        
        label = node.__class__.__name__.replace("Node", "")
        props = node.to_dict()
        
        with self._driver.session() as session:
            try:
                session.run(
                    f"CREATE (n:{label} $props)",
                    props=props
                )
                logger.debug(f"节点创建成功: {label}/{node.id}")
                return True
            except Exception as e:
                logger.error(f"节点创建失败: {e}")
                return False
    
    def get_node(self, label: str, node_id: str) -> Optional[Dict]:
        """
        获取节点
        
        Args:
            label: 节点标签
            node_id: 节点ID
            
        Returns:
            节点属性字典
        """
        if not self._driver:
            return None
        
        with self._driver.session() as session:
            result = session.run(
                f"MATCH (n:{label} {{id: $id}}) RETURN n",
                id=node_id
            )
            record = result.single()
            if record:
                return dict(record["n"])
            return None
    
    def update_node(self, label: str, node_id: str, 
                    properties: Dict[str, Any]) -> bool:
        """
        更新节点属性
        
        Args:
            label: 节点标签
            node_id: 节点ID
            properties: 要更新的属性
            
        Returns:
            是否更新成功
        """
        if not self._driver:
            return False
        
        properties["updated_at"] = datetime.now().isoformat()
        
        with self._driver.session() as session:
            try:
                session.run(
                    f"MATCH (n:{label} {{id: $id}}) SET n += $props",
                    id=node_id,
                    props=properties
                )
                return True
            except Exception as e:
                logger.error(f"节点更新失败: {e}")
                return False
    
    def delete_node(self, label: str, node_id: str) -> bool:
        """
        删除节点
        
        Args:
            label: 节点标签
            node_id: 节点ID
            
        Returns:
            是否删除成功
        """
        if not self._driver:
            return False
        
        with self._driver.session() as session:
            try:
                session.run(
                    f"MATCH (n:{label} {{id: $id}}) DETACH DELETE n",
                    id=node_id
                )
                return True
            except Exception as e:
                logger.error(f"节点删除失败: {e}")
                return False
    
    # ========== 关系操作 ==========
    
    def create_relation(self, from_label: str, from_id: str,
                        to_label: str, to_id: str,
                        relation_type: RelationType,
                        properties: Dict = None) -> bool:
        """
        创建关系
        
        Args:
            from_label: 起点节点标签
            from_id: 起点节点ID
            to_label: 终点节点标签
            to_id: 终点节点ID
            relation_type: 关系类型
            properties: 关系属性
            
        Returns:
            是否创建成功
        """
        if not self._driver:
            return False
        
        props = properties or {}
        
        with self._driver.session() as session:
            try:
                session.run(
                    f"""
                    MATCH (a:{from_label} {{id: $from_id}})
                    MATCH (b:{to_label} {{id: $to_id}})
                    CREATE (a)-[r:{relation_type.value} $props]->(b)
                    """,
                    from_id=from_id,
                    to_id=to_id,
                    props=props
                )
                logger.debug(f"关系创建成功: {from_id} -[{relation_type.value}]-> {to_id}")
                return True
            except Exception as e:
                logger.error(f"关系创建失败: {e}")
                return False
    
    def delete_relation(self, from_id: str, to_id: str,
                        relation_type: RelationType = None) -> bool:
        """
        删除关系
        
        Args:
            from_id: 起点节点ID
            to_id: 终点节点ID
            relation_type: 关系类型（可选，不指定则删除所有关系）
            
        Returns:
            是否删除成功
        """
        if not self._driver:
            return False
        
        with self._driver.session() as session:
            try:
                if relation_type:
                    session.run(
                        f"""
                        MATCH (a {{id: $from_id}})-[r:{relation_type.value}]->(b {{id: $to_id}})
                        DELETE r
                        """,
                        from_id=from_id,
                        to_id=to_id
                    )
                else:
                    session.run(
                        """
                        MATCH (a {id: $from_id})-[r]->(b {id: $to_id})
                        DELETE r
                        """,
                        from_id=from_id,
                        to_id=to_id
                    )
                return True
            except Exception as e:
                logger.error(f"关系删除失败: {e}")
                return False
    
    # ========== 项目相关 ==========
    
    def create_project(self, project: ProjectNode) -> bool:
        """创建项目节点"""
        return self.create_node(project)
    
    def add_agent_to_project(self, project_id: str, agent_id: str,
                              role: str = "primary") -> bool:
        """
        添加Agent到项目
        
        Args:
            project_id: 项目ID
            agent_id: Agent ID
            role: 角色（primary/secondary）
        """
        return self.create_relation(
            "Project", project_id,
            "Agent", agent_id,
            RelationType.HAS_AGENT,
            {"role": role, "added_at": datetime.now().isoformat()}
        )
    
    def get_project_agents(self, project_id: str) -> List[Dict]:
        """获取项目的所有Agent"""
        if not self._driver:
            return []
        
        with self._driver.session() as session:
            result = session.run(
                """
                MATCH (p:Project {id: $project_id})-[:HAS_AGENT]->(a:Agent)
                RETURN a
                """,
                project_id=project_id
            )
            return [dict(record["a"]) for record in result]
    
    # ========== Agent相关 ==========
    
    def create_agent(self, agent: AgentNode) -> bool:
        """创建Agent节点"""
        return self.create_node(agent)
    
    def add_skill_to_agent(self, agent_id: str, skill_id: str,
                           proficiency: float = 1.0) -> bool:
        """
        为Agent添加技能
        
        Args:
            agent_id: Agent ID
            skill_id: 技能ID
            proficiency: 熟练度 0-1
        """
        return self.create_relation(
            "Agent", agent_id,
            "Skill", skill_id,
            RelationType.USES_SKILL,
            {"proficiency": proficiency, "last_used": datetime.now().isoformat()}
        )
    
    def get_agent_skills(self, agent_id: str) -> List[Dict]:
        """获取Agent的所有技能"""
        if not self._driver:
            return []
        
        with self._driver.session() as session:
            result = session.run(
                """
                MATCH (a:Agent {id: $agent_id})-[:USES_SKILL]->(s:Skill)
                RETURN s
                """,
                agent_id=agent_id
            )
            return [dict(record["s"]) for record in result]
    
    def get_agent_dependencies(self, agent_id: str) -> List[Dict]:
        """获取Agent依赖的其他Agent"""
        if not self._driver:
            return []
        
        with self._driver.session() as session:
            result = session.run(
                """
                MATCH (a:Agent {id: $agent_id})-[:DEPENDS_ON]->(dep:Agent)
                RETURN dep
                """,
                agent_id=agent_id
            )
            return [dict(record["dep"]) for record in result]
    
    # ========== 决策相关 ==========
    
    def record_decision(self, decision: DecisionNode,
                        affected_nodes: List[tuple] = None) -> bool:
        """
        记录决策
        
        Args:
            decision: 决策节点
            affected_nodes: 受影响的节点列表 [(label, id), ...]
        """
        # 创建决策节点
        if not self.create_node(decision):
            return False
        
        # 创建Agent到决策的关系
        if decision.made_by:
            self.create_relation(
                "Agent", decision.made_by,
                "Decision", decision.id,
                RelationType.MADE_DECISION,
                {"timestamp": datetime.now().isoformat()}
            )
        
        # 创建决策影响关系
        if affected_nodes:
            for label, node_id in affected_nodes:
                self.create_relation(
                    "Decision", decision.id,
                    label, node_id,
                    RelationType.DECISION_AFFECTS
                )
        
        return True
    
    def get_project_decisions(self, project_id: str) -> List[Dict]:
        """获取项目的所有决策"""
        if not self._driver:
            return []
        
        with self._driver.session() as session:
            result = session.run(
                """
                MATCH (d:Decision {project_id: $project_id})
                RETURN d
                ORDER BY d.created_at DESC
                """,
                project_id=project_id
            )
            return [dict(record["d"]) for record in result]
    
    # ========== 模式相关 ==========
    
    def suggest_patterns(self, scenario: str, top_k: int = 5) -> List[Dict]:
        """
        推荐适用模式
        
        Args:
            scenario: 场景描述
            top_k: 返回数量
            
        Returns:
            推荐的模式列表
        """
        if not self._driver:
            return []
        
        with self._driver.session() as session:
            # 简单的关键词匹配
            keywords = scenario.lower().split()
            result = session.run(
                """
                MATCH (p:Pattern)
                WHERE ANY(keyword IN $keywords WHERE 
                    toLower(p.description) CONTAINS keyword OR
                    ANY(scene IN p.applicable_scenarios WHERE toLower(scene) CONTAINS keyword))
                RETURN p
                ORDER BY p.success_rate DESC, p.usage_count DESC
                LIMIT $top_k
                """,
                keywords=keywords,
                top_k=top_k
            )
            return [dict(record["p"]) for record in result]
    
    def record_pattern_usage(self, pattern_id: str, project_id: str,
                              success: bool = True) -> bool:
        """
        记录模式使用
        
        Args:
            pattern_id: 模式ID
            project_id: 项目ID
            success: 是否成功
        """
        # 创建项目-模式关系
        self.create_relation(
            "Project", project_id,
            "Pattern", pattern_id,
            RelationType.APPLIES_PATTERN,
            {"applied_at": datetime.now().isoformat(), "success": success}
        )
        
        # 更新模式统计
        if self._driver:
            with self._driver.session() as session:
                session.run(
                    """
                    MATCH (p:Pattern {id: $pattern_id})
                    SET p.usage_count = p.usage_count + 1,
                        p.success_rate = CASE 
                            WHEN $success THEN (p.success_rate * p.usage_count + 1) / (p.usage_count + 1)
                            ELSE p.success_rate * p.usage_count / (p.usage_count + 1)
                        END
                    """,
                    pattern_id=pattern_id,
                    success=success
                )
        
        return True
    
    # ========== 问题相关 ==========
    
    def record_problem(self, problem: ProblemNode,
                       solution: str = None) -> bool:
        """
        记录问题
        
        Args:
            problem: 问题节点
            solution: 解决方案
        """
        if solution:
            problem.solution = solution
            problem.status = "solved"
        
        return self.create_node(problem)
    
    def find_similar_problems(self, description: str, top_k: int = 5) -> List[Dict]:
        """
        查找相似问题
        
        Args:
            description: 问题描述
            top_k: 返回数量
            
        Returns:
            相似问题列表
        """
        if not self._driver:
            return []
        
        keywords = description.lower().split()
        
        with self._driver.session() as session:
            result = session.run(
                """
                MATCH (p:Problem)
                WHERE ANY(keyword IN $keywords WHERE 
                    toLower(p.title) CONTAINS keyword OR
                    toLower(p.description) CONTAINS keyword)
                RETURN p
                ORDER BY p.created_at DESC
                LIMIT $top_k
                """,
                keywords=keywords,
                top_k=top_k
            )
            return [dict(record["p"]) for record in result]
    
    # ========== 知识检索 ==========
    
    def search_knowledge(self, query: str, category: str = None,
                         top_k: int = 10) -> List[Dict]:
        """
        搜索知识
        
        Args:
            query: 查询内容
            category: 知识类别
            top_k: 返回数量
            
        Returns:
            匹配的知识列表
        """
        if not self._driver:
            return []
        
        keywords = query.lower().split()
        
        with self._driver.session() as session:
            if category:
                result = session.run(
                    """
                    MATCH (k:Knowledge {category: $category})
                    WHERE ANY(keyword IN $keywords WHERE 
                        toLower(k.title) CONTAINS keyword OR
                        toLower(k.content) CONTAINS keyword OR
                        ANY(tag IN k.tags WHERE toLower(tag) CONTAINS keyword))
                    RETURN k
                    ORDER BY k.confidence DESC
                    LIMIT $top_k
                    """,
                    keywords=keywords,
                    category=category,
                    top_k=top_k
                )
            else:
                result = session.run(
                    """
                    MATCH (k:Knowledge)
                    WHERE ANY(keyword IN $keywords WHERE 
                        toLower(k.title) CONTAINS keyword OR
                        toLower(k.content) CONTAINS keyword OR
                        ANY(tag IN k.tags WHERE toLower(tag) CONTAINS keyword))
                    RETURN k
                    ORDER BY k.confidence DESC
                    LIMIT $top_k
                    """,
                    keywords=keywords,
                    top_k=top_k
                )
            
            return [dict(record["k"]) for record in result]
    
    def get_related_knowledge(self, node_label: str, 
                               node_id: str) -> List[Dict]:
        """
        获取节点相关的知识
        
        Args:
            node_label: 节点标签
            node_id: 节点ID
            
        Returns:
            相关知识列表
        """
        if not self._driver:
            return []
        
        with self._driver.session() as session:
            result = session.run(
                f"""
                MATCH (n:{node_label} {{id: $node_id}})-[*1..2]-(k:Knowledge)
                RETURN DISTINCT k
                ORDER BY k.confidence DESC
                LIMIT 10
                """,
                node_id=node_id
            )
            return [dict(record["k"]) for record in result]
    
    # ========== 统计与分析 ==========
    
    def get_statistics(self) -> Dict[str, Any]:
        """获取图谱统计信息"""
        if not self._driver:
            return {"status": "disconnected"}
        
        with self._driver.session() as session:
            stats = {}
            
            # 节点统计
            for label in ["Project", "Agent", "Skill", "Decision", 
                         "Pattern", "Problem", "Knowledge"]:
                result = session.run(f"MATCH (n:{label}) RETURN count(n) as count")
                stats[f"{label.lower()}_count"] = result.single()["count"]
            
            # 关系统计
            result = session.run("MATCH ()-[r]->() RETURN count(r) as count")
            stats["relation_count"] = result.single()["count"]
            
            return stats
    
    def export_graph(self) -> Dict[str, Any]:
        """导出完整图谱"""
        if not self._driver:
            return {"nodes": [], "relations": []}
        
        with self._driver.session() as session:
            # 导出节点
            nodes_result = session.run("MATCH (n) RETURN n")
            nodes = []
            for record in nodes_result:
                node = dict(record["n"])
                node["_labels"] = list(record["n"].labels)
                nodes.append(node)
            
            # 导出关系
            relations_result = session.run(
                "MATCH (a)-[r]->(b) RETURN a.id as from_id, type(r) as type, b.id as to_id"
            )
            relations = [dict(record) for record in relations_result]
            
            return {"nodes": nodes, "relations": relations}