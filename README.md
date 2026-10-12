# chill_education

JA: AI が答えを教えず「問い」で導くことで、学生が自分で考えながら学べる AI 学習支援 Web アプリ。
VI: Ứng dụng web hỗ trợ học tập bằng AI: AI không đưa ra đáp án mà dẫn dắt bằng "câu hỏi", giúp sinh viên tự suy nghĩ khi học.

---

## 概要 / Tổng quan

JA: gPBL（Global Project Based Learning）で、ベトナムの学生と日本の学生の合同チームが開発したアプリです。
開発テーマは「**AI が当たり前になった時代に、学生たちが自分で考え、主体的に学び、成長を感じることができる Web アプリ**」。

一般的な AI 学習ツールは質問すると答えを返すため、考えずに答えだけを写しがちです。
このアプリの AI チューターは最終的な答えを出さず、ヒント・誘導質問・小さな問いへの分解で学習者を導きます。
学んだ内容はツリー構造の知識ベースに蓄積され、間隔反復で「そろそろ復習すべきもの」を知らせます。

プロダクト名は未定です。リポジトリ名の `chill_education` は、gPBL でのチーム名「chill」と、
開発テーマ（学生の主体的な学び）を表す「education」を合わせたものです。

VI: Ứng dụng do nhóm chung sinh viên Việt Nam và Nhật Bản phát triển trong chương trình gPBL (Global Project Based Learning).
Chủ đề phát triển: "**Một ứng dụng web giúp sinh viên tự suy nghĩ, chủ động học tập và cảm nhận được sự trưởng thành trong thời đại AI đã trở nên phổ biến**".

Các công cụ học tập AI thông thường trả lời ngay khi được hỏi, nên người học dễ chép đáp án mà không suy nghĩ.
Gia sư AI của ứng dụng này không đưa ra đáp án cuối cùng, mà dẫn dắt bằng gợi ý, câu hỏi định hướng và chia nhỏ vấn đề.
Nội dung đã học được lưu vào cơ sở tri thức dạng cây, và nhắc "nên ôn lại" theo phương pháp lặp lại ngắt quãng.

Tên sản phẩm chưa được quyết định. Tên repo `chill_education` ghép từ tên nhóm "chill" trong gPBL
và "education" thể hiện chủ đề phát triển (việc học chủ động của sinh viên).

---

## 主な機能 / Tính năng chính

### ヒントチャット / Chat gợi ý（`/hint-chat`）

- JA: AI は答えを直接出さず、ヒントと問いで段階的に導く（システムプロンプトで徹底）
  VI: AI không đưa đáp án trực tiếp mà dẫn dắt từng bước bằng gợi ý và câu hỏi (đảm bảo bằng system prompt)
- JA: 会話の各発言を AI が「幹（学習の大きなステップ）」か「枝（掘り下げの質問）」かに分類し、思考ツリーとして自動整理
  VI: AI phân loại từng phát ngôn thành "thân" (bước học lớn) hay "nhánh" (câu hỏi đào sâu) và tự sắp xếp thành cây tư duy
- JA: どの過去の発言に続く質問かを AI が推定し、確信度が低いときはユーザーに確認する
  VI: AI đoán câu hỏi nối tiếp phát ngôn nào trước đó; khi độ tin cậy thấp thì hỏi lại người dùng
- JA: チャットが終わると、会話を要約して学習ツリーに「知識ノード」として保存
  VI: Khi kết thúc chat, nội dung được tóm tắt và lưu vào cây học tập dưới dạng "node tri thức"

### 学習ツリー / Cây học tập（`/learning-tree`）

- JA: 学んだ内容を「トピック（フォルダのような階層）× 知識ノード」で管理・可視化
  VI: Quản lý và trực quan hóa nội dung đã học theo "topic (phân cấp như thư mục) × node tri thức"
- JA: トピック配下の検索と検索履歴、曖昧な説明からキーワード候補を出す AI 検索アシスト
  VI: Tìm kiếm trong topic kèm lịch sử, và trợ lý tìm kiếm AI gợi ý từ khóa từ mô tả mơ hồ
- JA: 復習を重ねるほど色が濃くなる「定着度」で、どこが定着済みかを一目で確認できる
  VI: "Mức độ ghi nhớ" đậm dần theo số lần ôn, giúp nhìn qua là biết phần nào đã nhớ chắc

### 復習リマインド / Nhắc ôn tập

- JA: 間隔反復アルゴリズム SM-2 で次回の復習日を計算し、期限を過ぎたノードを一覧表示
  VI: Tính ngày ôn tiếp theo bằng thuật toán lặp lại ngắt quãng SM-2 và liệt kê các node đã quá hạn
- JA: 理解度は自己申告させず、「予定日にノードを開いて復習を完了したか」という行動で判断する
  VI: Không bắt tự đánh giá mức hiểu, mà đánh giá bằng hành động "có mở node và hoàn thành ôn đúng ngày không"

---

## 技術構成 / Công nghệ

| 領域 / Phần | 技術 / Công nghệ |
|---|---|
| Frontend | React 18 + TypeScript + Vite（SPA）、TanStack Query、React Router、React Flow（`@xyflow/react`）、Tailwind CSS |
| Backend | Django 5 + Django REST Framework（セッション認証 / xác thực session） |
| DB | SQLite（ローカル / local）、PostgreSQL（本番 / production） |
| AI | プロバイダ抽象化層 / lớp trừu tượng provider: `fake`（API キー不要 / không cần API key）・Gemini・Claude |
| Hosting | Vercel（Frontend）、Render（Backend） |
| CI | GitHub Actions（ruff・型チェック / kiểm kiểu・ビルド / build） |

```
[ブラウザ / Trình duyệt]
   │  React SPA（Vercel）
   │  /api/*  セッション Cookie + CSRF / Cookie session + CSRF
   ▼
[Django REST Framework]（Render）
   ├── accounts  認証 / xác thực
   ├── chat      ヒントチャット・思考ツリー / chat gợi ý, cây tư duy
   ├── topics    学習ツリー・検索 / cây học tập, tìm kiếm
   ├── reviews   SM-2 による復習 / ôn tập theo SM-2
   └── ai        LLM 抽象化 / trừu tượng LLM ──▶ Gemini / Claude / fake
```

JA: バックエンドは `views → services → models` の一方向依存に統一し、業務ロジックは `services.py` に置きます。
すべてのデータはユーザー単位で絞り込み、他人のデータには触れられないようにしています。
5 人のチームで同じ形のコードを書けるよう、実装パターンを [`CONVENTIONS.md`](./CONVENTIONS.md) にまとめています。

VI: Backend thống nhất phụ thuộc một chiều `views → services → models`, logic nghiệp vụ đặt ở `services.py`.
Mọi dữ liệu đều lọc theo người dùng để không chạm được dữ liệu của người khác.
Để nhóm 5 người viết code cùng một kiểu, các pattern hiện thực được tổng hợp trong [`CONVENTIONS.md`](./CONVENTIONS.md).

---

## ディレクトリ構成 / Cấu trúc

```
.
├── CONVENTIONS.md          # 開発規約（最重要）/ Quy ước (quan trọng nhất)
├── .env.example            # 環境変数の雛形 / Mẫu biến môi trường
├── .github/                # CI・PR テンプレート / CI, mẫu PR
├── backend/
│   ├── config/             # 設定(base/local/production)・urls / cấu hình, urls
│   ├── apps/
│   │   ├── common/         # 基底モデル・共通例外・権限・レート制限・seed / model gốc, ngoại lệ, quyền, rate limit, seed
│   │   ├── accounts/       # カスタム User・認証 API / User tùy biến, API xác thực
│   │   ├── ai/             # LLM 抽象化 / trừu tượng LLM: fake / gemini / claude
│   │   ├── chat/           # ヒントチャット / chat gợi ý
│   │   ├── topics/         # 学習ツリー / cây học tập
│   │   └── reviews/        # 間隔復習 / ôn tập ngắt quãng
│   └── requirements/       # base / local / gemini / production
└── frontend/
    └── src/
        ├── app/            # Provider・router・認証ガード / auth guard
        ├── pages/          # 画面の組み立て / ghép màn hình
        ├── features/       # auth / hintChat / learningTree / reviews
        └── shared/         # API クライアント・UI・型 / API client, UI, kiểu
```

---

## 開発環境の構築 / Cài đặt môi trường phát triển

前提 / Yêu cầu: **Python 3.13**, **Node 20+**

### 1. リポジトリ直下 / Ở gốc repo

```bash
cp .env.example .env      # 中身は空でOK（fake AI で動く）/ để trống cũng được (chạy fake AI)
```

### 2. バックエンド / Backend

```bash
cd backend
python -m venv .venv && source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements/local.txt
python manage.py migrate
python manage.py seed        # デモユーザーとサンプルの学習ツリーを投入 / nạp user demo và cây học tập mẫu
python manage.py runserver   # http://localhost:8000
```

### 3. フロントエンド / Frontend（別ターミナル / terminal khác）

```bash
cd frontend
npm install
npm run dev                  # http://localhost:5173
```

### 4. ログイン / Đăng nhập

JA: http://localhost:5173 を開き、`demo` / `demo12345` でログインするか、新規登録します。
`/api` は Vite が `:8000` にプロキシするので、Cookie と CSRF が同一オリジンとして動きます。

VI: Mở http://localhost:5173, đăng nhập bằng `demo` / `demo12345` hoặc đăng ký mới.
Vite proxy `/api` sang `:8000` nên Cookie và CSRF chạy như cùng origin.

### AI プロバイダ / Nhà cung cấp AI

JA: 既定は `AI_PROVIDER=fake` で、API キーなしで開発できます。実際の LLM を使うときは `.env` に設定します。
キーが未設定のまま `gemini` / `claude` を選んでも、自動で fake に切り替わります。

VI: Mặc định `AI_PROVIDER=fake`, không cần API key vẫn phát triển được. Khi dùng LLM thật thì đặt trong `.env`.
Nếu chọn `gemini` / `claude` mà chưa có key, hệ thống tự chuyển về fake.

| `AI_PROVIDER` | 必要な設定 / Cần đặt | 追加のインストール / Cài thêm |
|---|---|---|
| `fake` | なし / không | なし / không |
| `gemini` | `GEMINI_API_KEY` | `pip install -r requirements/gemini.txt` ※ |
| `claude` | `ANTHROPIC_API_KEY` | なし（`local.txt` に含まれる）/ không (đã có trong `local.txt`) |

JA: ※ Gemini の SDK は Windows ARM64 など一部の環境でビルドに失敗するため、`local.txt` から分けています。
VI: ※ SDK của Gemini bị lỗi build trên một số môi trường như Windows ARM64, nên được tách khỏi `local.txt`.

### 動作確認 / Kiểm tra

```bash
cd backend && python manage.py test apps                 # テスト / test
cd backend && ruff check . && ruff format --check .      # lint
cd frontend && npm run typecheck && npm run build        # 型チェック・ビルド / kiểm kiểu, build
```

---

## 関連ドキュメント / Tài liệu liên quan

| ファイル / File | 内容 / Nội dung |
|---|---|
| [`CONVENTIONS.md`](./CONVENTIONS.md) | 開発規約・実装パターン・Git 運用 / Quy ước, pattern hiện thực, quy trình Git |
| [`FOLDER_GUIDE.ja.md`](./FOLDER_GUIDE.ja.md) / [`FOLDER_GUIDE.vi.md`](./FOLDER_GUIDE.vi.md) | フォルダの役割 / Vai trò từng thư mục |
| [`DESIGN_SYSTEM.md`](./DESIGN_SYSTEM.md) | UI のデザインルール / Quy tắc thiết kế UI |
| [`APP_OVERVIEW_FOR_SLIDES.md`](./APP_OVERVIEW_FOR_SLIDES.md) | 機能の詳しい説明 / Mô tả chi tiết tính năng |
