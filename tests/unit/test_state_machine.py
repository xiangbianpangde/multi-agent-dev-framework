"""
状态机单元测试
"""
import pytest
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent.parent.parent / "tools" / "templates"))

from core.state_machine import (
    StateMachine, TaskState, InvalidTransitionError,
    is_valid_transition, get_transition_path
)


class TestStateMachine:
    """状态机测试"""
    
    def test_initial_state(self):
        """测试初始状态"""
        sm = StateMachine()
        assert sm.current_state == TaskState.DRAFT
    
    def test_valid_transition(self):
        """测试合法转换"""
        sm = StateMachine()
        assert sm.can_transition_to(TaskState.PLANNING) is True
        assert sm.can_transition_to(TaskState.DONE) is False
    
    def test_transition_success(self):
        """测试转换成功"""
        sm = StateMachine()
        sm.transition(TaskState.PLANNING, "开始规划")
        assert sm.current_state == TaskState.PLANNING
    
    def test_invalid_transition(self):
        """测试非法转换"""
        sm = StateMachine()
        with pytest.raises(InvalidTransitionError):
            sm.transition(TaskState.DONE)
    
    def test_full_workflow(self):
        """测试完整工作流"""
        sm = StateMachine()
        
        # 正常流程
        sm.transition(TaskState.PLANNING)
        sm.transition(TaskState.REVIEW)
        sm.transition(TaskState.DISPATCHED)
        sm.transition(TaskState.EXECUTING)
        sm.transition(TaskState.CHECKING)
        sm.transition(TaskState.ACCEPTED)
        sm.transition(TaskState.DONE)
        
        assert sm.is_terminal() is True
    
    def test_rejected_flow(self):
        """测试封驳流程"""
        sm = StateMachine()
        
        sm.transition(TaskState.PLANNING)
        sm.transition(TaskState.REVIEW)
        sm.transition(TaskState.REJECTED, "审核不通过")
        
        assert sm.current_state == TaskState.REJECTED
        assert sm.is_terminal() is False
        
        # 返回重做
        sm.transition(TaskState.PLANNING)
        assert sm.current_state == TaskState.PLANNING
    
    def test_history(self):
        """测试历史记录"""
        sm = StateMachine()
        sm.transition(TaskState.PLANNING, "开始")
        
        history = sm.get_history()
        assert len(history) == 2  # 初始 + 1次转换
        assert history[1]["state"] == "planning"
        assert history[1]["reason"] == "开始"
    
    def test_is_active(self):
        """测试活跃状态"""
        sm = StateMachine()
        assert sm.is_active() is False
        
        sm.transition(TaskState.PLANNING)
        assert sm.is_active() is True
    
    def test_force_transition(self):
        """测试强制转换"""
        sm = StateMachine()
        sm.force_transition(TaskState.DONE, "强制完成")
        assert sm.current_state == TaskState.DONE


class TestStateTransitionHelpers:
    """状态转换辅助函数测试"""
    
    def test_is_valid_transition(self):
        """测试转换验证"""
        assert is_valid_transition(TaskState.DRAFT, TaskState.PLANNING) is True
        assert is_valid_transition(TaskState.DRAFT, TaskState.DONE) is False
    
    def test_get_transition_path_direct(self):
        """测试直接转换路径"""
        path = get_transition_path(TaskState.DRAFT, TaskState.PLANNING)
        assert path == [TaskState.DRAFT, TaskState.PLANNING]
    
    def test_get_transition_path_same(self):
        """测试相同状态"""
        path = get_transition_path(TaskState.DRAFT, TaskState.DRAFT)
        assert path == [TaskState.DRAFT]
    
    def test_get_transition_path_multi_step(self):
        """测试多步路径"""
        path = get_transition_path(TaskState.DRAFT, TaskState.DISPATCHED)
        assert TaskState.DRAFT in path
        assert TaskState.DISPATCHED in path
        assert len(path) > 2