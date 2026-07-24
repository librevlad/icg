import json
import yaml
from .contract import Contract
from core.types import ContractStatus

class ContractSerializer:
    @staticmethod
    def to_dict(contract: Contract) -> dict:
        return {
            "id": contract.id,
            "task_description": contract.task_description,
            "requires": contract.requires,
            "constraints": contract.constraints,
            "inputs": contract.inputs,
            "outputs": contract.outputs,
            "acceptance_criteria": contract.acceptance_criteria,
            "workspace": contract.workspace,
            "status": contract.status.value,
            "created_at": contract.created_at
        }

    @staticmethod
    def from_dict(data: dict) -> Contract:
        contract = Contract(
            id=data["id"],
            task_description=data["task_description"],
            requires=data.get("requires", [])
        )
        contract.constraints = data.get("constraints", {})
        contract.inputs = data.get("inputs", {})
        contract.outputs = data.get("outputs", {})
        contract.acceptance_criteria = data.get("acceptance_criteria", [])
        contract.workspace = data.get("workspace", "")
        if "status" in data:
            contract.status = ContractStatus(data["status"])
        if "created_at" in data:
            contract.created_at = data["created_at"]
        return contract

    @staticmethod
    def from_json(json_str: str) -> Contract:
        return ContractSerializer.from_dict(json.loads(json_str))

    @staticmethod
    def to_json(contract: Contract) -> str:
        return json.dumps(ContractSerializer.to_dict(contract))
        
    @staticmethod
    def from_yaml(yaml_str: str) -> Contract:
        return ContractSerializer.from_dict(yaml.safe_load(yaml_str))
        
    @staticmethod
    def to_yaml(contract: Contract) -> str:
        return yaml.dump(ContractSerializer.to_dict(contract))
