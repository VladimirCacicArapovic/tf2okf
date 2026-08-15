from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

@dataclass
class Variable:
    name: str
    type: str | None = None
    description: str | None = None
    default: Any = None
    sensitive: bool = False
    file: str | None = None

@dataclass
class Output:
    name: str
    description: str | None = None
    value: str | None = None
    sensitive: bool = False
    file: str | None = None

@dataclass
class Resource:
    kind: str  # resource | data
    type: str
    name: str
    file: str
    attributes: dict[str, str] = field(default_factory=dict)
    references: set[str] = field(default_factory=set)

    @property
    def address(self) -> str:
        return f"data.{self.type}.{self.name}" if self.kind == "data" else f"{self.type}.{self.name}"

@dataclass
class Module:
    name: str
    source: str | None
    file: str
    attributes: dict[str, str] = field(default_factory=dict)
    references: set[str] = field(default_factory=set)

    @property
    def address(self) -> str:
        return f"module.{self.name}"

@dataclass
class Provider:
    name: str
    source: str | None = None
    version: str | None = None

@dataclass
class TerraformModel:
    root: Path
    resources: list[Resource] = field(default_factory=list)
    modules: list[Module] = field(default_factory=list)
    variables: list[Variable] = field(default_factory=list)
    outputs: list[Output] = field(default_factory=list)
    providers: list[Provider] = field(default_factory=list)
    source_files: list[str] = field(default_factory=list)
    terraform_docs_markdown: str | None = None
