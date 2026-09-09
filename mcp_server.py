"""MCP Server for Count-Min Sketch Skill."""
import json
import sys
from client import CountMinSketch

def main():
    cms = CountMinSketch()
    for line in sys.stdin:
        if not line.strip():
            continue
        try:
            req = json.loads(line)
            req_id = req.get("id")
            method = req.get("method")
            params = req.get("params", {})

            if method == "tools/list":
                res = {
                    "jsonrpc": "2.0",
                    "id": req_id,
                    "result": {
                        "tools": [
                            {
                                "name": "update_sketch",
                                "description": "Add occurrences of item to sketch",
                                "inputSchema": {
                                    "type": "object",
                                    "properties": {
                                        "item": {"type": "string"},
                                        "count": {"type": "integer"}
                                    },
                                    "required": ["item"]
                                }
                            },
                            {
                                "name": "query_sketch",
                                "description": "Estimate frequency of item",
                                "inputSchema": {
                                    "type": "object",
                                    "properties": {"item": {"type": "string"}},
                                    "required": ["item"]
                                }
                            }
                        ]
                    }
                }
            elif method == "tools/call":
                name = params.get("name")
                args = params.get("arguments", {})
                if name == "update_sketch":
                    cms.update(args["item"], args.get("count", 1))
                    out = {"status": "updated"}
                else:
                    freq = cms.estimate(args["item"])
                    out = {"estimated_frequency": freq}
                res = {
                    "jsonrpc": "2.0",
                    "id": req_id,
                    "result": {"content": [{"type": "text", "text": json.dumps(out)}]}
                }
            else:
                res = {"jsonrpc": "2.0", "id": req_id, "error": {"code": -32601, "message": "Method not found"}}
            print(json.dumps(res), flush=True)
        except Exception as e:
            err = {"jsonrpc": "2.0", "id": None, "error": {"code": -32000, "message": str(e)}}
            print(json.dumps(err), flush=True)

if __name__ == "__main__":
    main()
