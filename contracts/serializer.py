import json
import yaml
from typing import Dict, Any
from .contract import Contract

class ContractSerializer:
    """
    Handles serialization and deserialization of Contracts.
    Decouples the Contract object from its storage format (YAML, JSON, etc).
    """

    @staticmethod
    def from_dict(data: Dict[str, Any]) -> Contract:
        return Contract(
            id=data.get("id", "unknown"),
            task_description=data.get("task", ""),
            requires=data.get("requires", []),
            constraints=data.get("constraints", []),
            inputs=data.get("inputs", {}),
            outputs=data.get("outputs", {}),
            acceptance_criteria=data.get("acceptance", [])
        )

    @staticmethod
    def to_dict(contract: Contract) -> Dict[str, Any]:
        return {
            "id": contract.id,
            "task": contract.task_description,
            "requires": contract.requires,
            "constraints": contract.constraints,
            "inputs": contract.inputs,
            "outputs": contract.outputs,
            "acceptance": contract.acceptance_criteria
        }

    @staticmethod
    def from_yaml(yaml_content: str) -> Contract:
        data = yaml.safe_load(yaml_content)
        return ContractSerializer.from_dict(data)

    @staticmethod
    def to_yaml(contract: Contract) -> str:
        return yaml.dump(ContractSerializer.to_dict(contract), sort_keys=False)
