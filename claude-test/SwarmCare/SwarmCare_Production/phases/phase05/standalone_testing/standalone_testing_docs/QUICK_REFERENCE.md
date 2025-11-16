# Quick Reference - Phase 05: Knowledge Graph

**Port:** 8005 | **Updated:** 2025-11-08

---

## Instant Start

```bash
cd deployment
./run.sh
# Access: http://localhost:8005
```

---

## Essential Commands

### Start Application
```bash
cd deployment && ./run.sh
```

### Stop Application
```bash
lsof -ti:8005 | xargs kill -9
```

### Health Check
```bash
curl http://localhost:8005/api/health | python3 -m json.tool
```

### View Logs
```bash
tail -f ../../../logs/phase05.log
```

---

## URLs

| Endpoint | URL |
|----------|-----|
| **UI** | http://localhost:8005 |
| **API Docs** | http://localhost:8005/docs |
| **Health** | http://localhost:8005/api/health |
| **OpenAPI** | http://localhost:8005/openapi.json |

---

## File Locations

```
Requirements:   standalone_testing/requirements/
Deployment:     standalone_testing/deployment/
Test Data:      standalone_testing/test_data/
Documentation:  standalone_testing/standalone_testing_docs/
Generated:      standalone_testing/deployment/generated_files/
```

---

## Quick Troubleshooting

| Issue | Solution |
|-------|----------|
| Port in use | `lsof -ti:8005 \| xargs kill -9` |
| FastAPI missing | `pip3 install --break-system-packages fastapi uvicorn` |
| Docker down | `docker-compose up -d neo4j redis` |
| Cannot access UI | Check `curl localhost:8005/api/health` |

---

## Dependencies Install

```bash
pip3 install --break-system-packages \
    fastapi>=0.109.0 \
    uvicorn>=0.27.0 \
    python-multipart \
    pydantic>=2.0.0 \
    python-dotenv>=1.0.0
```

---

## Testing Workflow

1. **Review Requirements** → `cd requirements && cat BRD.md`
2. **Start App** → `cd deployment && ./run.sh`
3. **Open Browser** → http://localhost:8005
4. **Test Features** → Use UI to test functionality
5. **Check Results** → `cd generated_files && ls -la`

---

**Phase 05 - Knowledge Graph**
**Ready for Testing**
