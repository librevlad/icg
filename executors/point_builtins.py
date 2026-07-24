"""
Point-oriented executors — built-in capabilities that don't require external APIs.
These handle common Object transformations that Point clients need.
"""
import json
import re
import hashlib
import base64
import time
from typing import List
from executors.base import Executor
from contracts.contract import Contract
from workspace.workspace import Workspace
from core.types import ExecutionResult


class TextAnalyzerExecutor(Executor):
    """Extracts structured entities from text: phones, emails, URLs, dates."""

    def capabilities(self) -> List[str]:
        return ["entity_extraction", "text_analysis"]

    def run(self, contract: Contract, workspace: Workspace) -> ExecutionResult:
        start = time.time()
        text = str(contract.inputs.get("object_data", contract.task_description))

        entities = {
            "phones": re.findall(r'[\+]?[\d\-\(\)\s]{7,15}', text),
            "emails": re.findall(r'[\w\.\-]+@[\w\.\-]+\.\w+', text),
            "urls": re.findall(r'https?://[^\s<>"\']+', text),
            "numbers": re.findall(r'\b\d+\.?\d*\b', text),
        }

        # Clean up phone matches
        entities["phones"] = [p.strip() for p in entities["phones"] if len(p.strip()) >= 7]

        result = json.dumps(entities, ensure_ascii=False, indent=2)
        return ExecutionResult(success=True, stdout=result, duration=time.time() - start)


class TransformExecutor(Executor):
    """Transforms text between formats: uppercase, lowercase, reverse, word count, char count, base64."""

    def capabilities(self) -> List[str]:
        return ["transform", "format"]

    def run(self, contract: Contract, workspace: Workspace) -> ExecutionResult:
        start = time.time()
        text = str(contract.inputs.get("object_data", ""))
        params = contract.inputs.get("parameters", {})
        operation = params.get("operation", "stats")

        ops = {
            "uppercase": lambda t: t.upper(),
            "lowercase": lambda t: t.lower(),
            "reverse": lambda t: t[::-1],
            "base64_encode": lambda t: base64.b64encode(t.encode()).decode(),
            "base64_decode": lambda t: base64.b64decode(t.encode()).decode(),
            "stats": lambda t: json.dumps({
                "characters": len(t),
                "words": len(t.split()),
                "lines": len(t.splitlines()),
                "sentences": len(re.split(r'[.!?]+', t)),
                "md5": hashlib.md5(t.encode()).hexdigest(),
            }, indent=2),
        }

        fn = ops.get(operation, ops["stats"])
        try:
            result = fn(text)
            return ExecutionResult(success=True, stdout=result, duration=time.time() - start)
        except Exception as e:
            return ExecutionResult(success=False, stderr=str(e), duration=time.time() - start)


class SummarizeExecutor(Executor):
    """Simple extractive summarization — picks the most important sentences."""

    def capabilities(self) -> List[str]:
        return ["summarize"]

    def run(self, contract: Contract, workspace: Workspace) -> ExecutionResult:
        start = time.time()
        text = str(contract.inputs.get("object_data", contract.task_description))

        sentences = re.split(r'(?<=[.!?])\s+', text)
        if len(sentences) <= 3:
            return ExecutionResult(success=True, stdout=text, duration=time.time() - start)

        # Score sentences by word count and position (longer + earlier = more important)
        scored = []
        for i, s in enumerate(sentences):
            word_count = len(s.split())
            position_score = 1.0 / (i + 1)
            scored.append((position_score * word_count, s))

        scored.sort(key=lambda x: x[0], reverse=True)
        top = scored[:max(3, len(sentences) // 3)]
        # Re-order by original position
        top_sentences = [s for _, s in sorted(top, key=lambda x: sentences.index(x[1]))]

        return ExecutionResult(
            success=True,
            stdout=" ".join(top_sentences),
            duration=time.time() - start,
        )
