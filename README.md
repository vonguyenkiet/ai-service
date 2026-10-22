# SupportFlow AI Service

Code base cho AI inference service của **SupportFlow AI IT Service Desk**.

Base này được thiết kế từ contract và code backend hiện tại, không biến AI thành một backend
nghiệp vụ thứ hai.

## Trách nhiệm

AI service:

- chạy ticket classification;
- giữ provider/model adapters tách khỏi API;
- tạo nền cho embedding;
- cung cấp evaluation baseline;
- không kết nối Service Desk database;
- không thay đổi ticket, priority, permission hoặc workflow.

Backend ASP.NET Core vẫn sở hữu business state, authorization, HITL, persistence và audit.

## Kiến trúc

```text
FastAPI
  |
  v
Application use cases
  |
  v
Ports <---- Adapters
  |          |-- NoOp
  |          `-- Rule baseline
  v
Domain
```

Xem `docs/architecture.md`.

## Trạng thái capability

| Capability | Trạng thái |
|---|---|
| Classification contract v1 | Có |
| FastAPI classification endpoint | Có |
| Service Bearer auth | Có |
| NoOp provider / controlled 503 | Có |
| Rule-based baseline | Có |
| Real ML/Transformer model | Chưa chọn |
| Embedding port/use case | Scaffold |
| External embedding endpoint | Chưa expose vì backend chưa có canonical contract |
| RAG | Chưa đưa vào MVP |
| Evaluation baseline | Có |

## Chạy local

```bash
python -m venv .venv
# Windows:
.venv\Scripts\activate
# Linux/macOS:
source .venv/bin/activate

python -m pip install -e ".[dev]"
cp .env.example .env
# Sinh token riêng, sao chép kết quả vào SUPPORTFLOW_AI_SERVICE_TOKEN trong .env:
python -c "import secrets; print(secrets.token_urlsafe(48))"
uvicorn supportflow_ai.main:create_app --factory --reload --host 127.0.0.1 --port 8000
```

PowerShell có thể dùng:

```powershell
Copy-Item .env.example .env
```

Endpoint:

```text
POST /v1/ticket-classifications
GET  /health/live
GET  /health/ready
```

Ví dụ request:

```json
{
  "requestId": "00000000-0000-0000-0000-000000000001",
  "ticketId": "00000000-0000-0000-0000-000000000002",
  "ticketRevision": 1,
  "inputHash": "e737e044b7ef976a6f2f2e97f1f2aaee633a2205cc16d051316bf2139d5dc02c",
  "title": "VPN issue",
  "description": "Cisco AnyConnect cannot connect"
}
```

Header:

```text
Authorization: Bearer <SUPPORTFLOW_AI_SERVICE_TOKEN>
```

Rule baseline trả category với `score: null`; nó không giả lập xác suất.

## Kiểm thử

```bash
ruff check .
pytest
python scripts/validate_ai_contract.py
python -m evaluation.run_classification
```

`evaluation/sample-classification.jsonl` chỉ là smoke data, không phải gold set.

## Provider mới

Để thêm model thật:

1. triển khai `TicketClassifier` trong `src/supportflow_ai/adapters/classifiers/`;
2. giữ provider output trong domain `ClassificationPrediction`;
3. đăng ký provider trong `bootstrap.py`;
4. thêm contract/integration tests;
5. benchmark cùng gold set trước khi chọn làm mặc định.

Không gọi SDK model trực tiếp từ FastAPI route.

## Security

- Không truyền end-user JWT sang AI service.
- Không cấp DB credential nghiệp vụ cho AI service.
- Không log title/description.
- Không trả action đặc quyền.
- Mặc định xác thực bật và **không có token mặc định**. Nếu không cung cấp token hợp lệ,
service sẽ từ chối khởi động. Chỉ môi trường development/test mới có thể tắt auth một cách
rõ ràng để chạy thử; staging/production không cho phép. Giới hạn request-body 64 KiB.

Production phải bật service Bearer với secret ngoài Git; đặt service trên private network,
không mở public port. Chưa có distributed rate-limit/advanced credential rotation/mTLS.
