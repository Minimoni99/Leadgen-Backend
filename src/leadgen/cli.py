from pathlib import Path
import argparse

from .db import init_db
from .enrich import enrich_batch, get_enrichment_stats
from .ingest import import_leads
from .generate import generate_queries, write_queries, QUERY_FILE, CATEGORIES, CITIES


def main() -> None:
    parser = argparse.ArgumentParser(description="Leadgen CLI")
    subparsers = parser.add_subparsers(dest="command")

    parser_seed = subparsers.add_parser("seed", help="Generate seed queries")
    parser_seed.add_argument("--output", type=Path, default=QUERY_FILE)

    parser_init = subparsers.add_parser("init", help="Initialize database schema")
    parser_init.add_argument("--schema", type=Path, default=None)

    parser_import = subparsers.add_parser("import", help="Import scraper CSV into database")
    parser_import.add_argument("csv_path", type=Path)
    parser_import.add_argument("--source", default="scraper")

    parser_enrich = subparsers.add_parser("enrich", help="Enrich pending leads")
    parser_enrich.add_argument("--batch-size", type=int, default=100)

    parser_status = subparsers.add_parser("status", help="Show lead and enrichment counts")

    args = parser.parse_args()

    if args.command == "seed":
        queries = list(generate_queries(CATEGORIES, CITIES))
        write_queries(args.output, queries)
        print(f"Generated {len(queries)} queries to {args.output}")
    elif args.command == "init":
        init_db(args.schema)
    elif args.command == "import":
        count = import_leads(args.csv_path, source=args.source)
        print(f"Imported {count} leads from {args.csv_path}")
    elif args.command == "enrich":
        count = enrich_batch(batch_size=args.batch_size)
        print(f"Enriched {count} pending leads")
    elif args.command == "status":
        stats = get_enrichment_stats()
        print("Lead status:")
        print(f"  total leads:    {stats['total']}")
        print(f"  enriched leads: {stats['enriched']}")
        print(f"  pending leads:  {stats['pending']}")
    else:
        parser.print_help()
