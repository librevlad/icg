import uvicorn

def setup_parser(subparsers):
    p = subparsers.add_parser("serve", help="Start the ICG API server for Point clients")
    p.add_argument("--host", default="0.0.0.0", help="Host interface to bind to")
    p.add_argument("--port", type=int, default=8000, help="Port to listen on")

def execute(args) -> int:
    print(f"Starting Point Backend API on {args.host}:{args.port}...")
    uvicorn.run("api.server:app", host=args.host, port=args.port, reload=False)
    return 0
