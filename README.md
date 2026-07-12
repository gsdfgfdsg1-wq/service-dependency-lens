# service-dependency-lens

A dependency-free CLI for analyzing service call graphs and estimating operational change impact.

## Quick start

```bash
python lens.py edges.json --changed checkout
```

Edges are JSON objects with `source` and `target`. The tool reports all services, downstream blast radius for a changed service, dependency cycles, and shared dependencies with multiple callers.

## Test

```bash
python -m unittest discover -v
```

## License

MIT.
