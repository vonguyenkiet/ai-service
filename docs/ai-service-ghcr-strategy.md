# AI Service GHCR Publishing Strategy — Round 3

Tài liệu ghi nhận chiến lược phát hành container image GHCR và đối soát của AI Service cho Round 3.

## 1. Thông tin nhánh và Commit

- Baseline branch: `ai-service` (`66d5cefd846b40d6e2c0e793c589037dfa36e042`)
- Round 2 branch: `devops/cicd-github-actions` (`28f85014c391355b4791b9e1a65a1c215b41bac7`)
- Round 3 corrective branch: `devops/cicd-round3-ai-service`
- Pull Request Round 2: [PR #4](https://github.com/supportflow-ai/ai-service/pull/4) (Base: `ai-service`, Head: `vonguyenkiet:devops/cicd-github-actions`)

## 2. Kết quả kiểm thử và Workflow Run

- Workflow Run: [Run 41115433754](https://github.com/supportflow-ai/ai-service/actions/runs/41115433754) (Success)
- Quality Job: Lint (Ruff 0 vi phạm), Pytest (34 passed), Contract validation (Pass), Baseline evaluation (Accuracy 1.0, MacroF1 1.0).
- Docker Job: Build non-root runtime image `servicedesk-ai-service:ci` thành công.

## 3. Chiến lược phát hành GHCR Trusted Upstream

- Do quy tắc bảo mật không cho phép Fork PR tiếp cận write token hoặc đẩy vào namespace của tổ chức `supportflow-ai`, job `publish` trên PR chạy fork được bỏ qua an toàn.
- Image mục tiêu: `ghcr.io/supportflow-ai/servicedesk-ai-service`
- Tag mục tiêu: `sha-28f85014c391355b4791b9e1a65a1c215b41bac7`
- Trạng thái hiện tại trong Release Manifest: `pending` (Digest: `null`).
- Quy trình kích hoạt: Ngay sau khi PR #4 được Lead Architect phê duyệt và merge vào nhánh chính thức `ai-service`, workflow upstream sẽ tự động xuất bản image chính thức lên GHCR.
