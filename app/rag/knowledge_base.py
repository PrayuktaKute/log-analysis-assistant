"""Load the historical-incident knowledge base used to seed the FAISS
vector store for RAG retrieval.

The knowledge base is a plain JSON file (default: `incidents.json` under
`settings.knowledge_base_dir`) -- editable/replaceable per deployment, not
hardcoded to any one dataset. A missing file degrades to an empty
knowledge base (logged) rather than raising, since retrieval over zero
incidents is a valid (if unhelpful) state, not an error.
"""

import json
from pathlib import Path

from loguru import logger

from app.config import settings
from app.models.schemas import HistoricalIncident

DEFAULT_KNOWLEDGE_BASE_FILE = "incidents.json"


class KnowledgeBaseLoader:
    """Loads HistoricalIncident records from a JSON file."""

    def __init__(self, knowledge_base_dir: Path = settings.knowledge_base_dir):
        self.knowledge_base_dir = Path(knowledge_base_dir)

    def load(self, filename: str = DEFAULT_KNOWLEDGE_BASE_FILE) -> list[HistoricalIncident]:
        path = self.knowledge_base_dir / filename
        if not path.exists():
            logger.warning("Knowledge base file not found at {} -- returning an empty knowledge base", path)
            return []

        raw = json.loads(path.read_text(encoding="utf-8"))
        incidents = [HistoricalIncident(**item) for item in raw]
        logger.info("Loaded {} historical incident(s) from {}", len(incidents), path)
        return incidents
