# ICG (Internet Capability Graph) Kernel

ICG — это ядро операционной системы для распределенного интеллекта.

## Главная философия проекта

> **ICG не знает названий моделей.**

Ядро оперирует исключительно абстракциями **Capability** (что нужно сделать) и **Node** (кто это будет делать). 
Если завтра вместо `Gemini CLI` появится `Kimi CLI`, `OpenAI Codex CLI` или квантовый вычислитель, в коде ядра ICG не должно измениться **вообще ничего**.

### Архитектура
- **Capability:** Требование к вычислительному ресурсу (например, `reasoning`, `coding`, `execution`).
- **Contract:** Декларативное описание задачи, которое не зависит от промптов или языков. Контракт — это объект с предсказуемой структурой.
- **Node (Исполнитель):** Любая программа или API, способная выполнить контракт для запрошенной Capability. И `Gemini CLI`, и `Bash` — это равноправные Nodes.
- **Graph (Ядро):** Система маршрутизации, которая связывает требуемую Capability с лучшим доступным Node, опираясь на эмпирический опыт.

## Быстрый старт

ICG — это прежде всего **Kernel/Library**, а не CLI.

```python
from icg.core.graph import ICGGraph
from icg.contracts.contract import Contract
from icg.workspace.workspace import Workspace
from icg.nodes.bash import BashNode

# Инициализация ядра
workspace = Workspace("./my_project")
kernel = ICGGraph(workspace)

# Регистрация исполнителей
bash_node = BashNode()
kernel.register_node(bash_node, ["execution"])

# Создание контракта
contract = Contract(
    id="task-1",
    task_description="List files",
    requires=["execution"],
    inputs={"command": "ls -la"}
)

# Запрос выполнения способности
result = kernel.request("execution", contract)
```

## Память и Обучение
Каждый запуск контракта на любом узле оставляет след в базе данных SQLite (History & Metrics). 
В будущем это позволит графу самостоятельно обучаться маршрутизировать задачи, используя подходы Reinforcement Learning (RL).
