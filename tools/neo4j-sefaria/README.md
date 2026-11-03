# Neo4j / Sefaria — small research utility snapshot

Original: https://github.com/MeiRR17/Neo4j (main). This folder consolidates the two Cypher files and three acquisition/validation/helper scripts, without copying data.

The original Docker Compose and README are deliberately **not** copied because they include a static authentication value, machine-specific Windows paths and insecure demo deployment settings. Use a modern Neo4j deployment with credentials from your own secret store and restrict network exposure. The PowerShell scripts are for Windows and may need adjustment; the Python ingestion script requires dependencies and rights review. Do not treat this source snapshot as a validated production service.
