from typing import Optional

from spotlight.core.common.base import Base
from spotlight.core.common.enum import RuleSeverity, RuleType


class DataRuleRequest(Base):
    display_name: str
    severity: RuleSeverity
    type: RuleType
    predicate: Optional[str]


class DataRuleResponse(Base):
    id: str
    display_name: str
    severity: RuleSeverity
    type: RuleType
    predicate: Optional[str]
    created_by: Optional[str]
    created_at: Optional[int]
    updated_by: Optional[str]
    updated_at: Optional[int]
