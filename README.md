# PHẦN 1: TỔNG QUAN DỰ ÁN (PROJECT REPORT)

# BÃ¡o CÃ¡o Dá»± Ãn: Hiá»‡n Äáº¡i HÃ³a Há»‡ Thá»‘ng QLSV (University Edition)

TÃ i liá»‡u nÃ y cung cáº¥p cÃ¡i nhÃ¬n tá»•ng quan vá» kiáº¿n trÃºc, cÃ´ng nghá»‡ vÃ  tiáº¿n Ä‘á»™ hiá»‡n táº¡i cá»§a dá»± Ã¡n dÃ nh cho thÃ nh viÃªn má»›i tham gia.

---

## 1. Tá»•ng Quan & Má»¥c TiÃªu
Dá»± Ã¡n Ä‘Æ°á»£c chuyá»ƒn Ä‘á»•i tá»« ná»n táº£ng Django Template (Monolithic) sang kiáº¿n trÃºc hiá»‡n Ä‘áº¡i **Decoupled API-First**:
- **Backend:** Django REST Framework (DRF) Ä‘Ã³ng vai trÃ² lÃ  API Server.
- **Frontend:** React (Vite) Ä‘Ã³ng vai trÃ² lÃ  Single Page Application (SPA).
- **Äá»‘i tÆ°á»£ng:** Há»‡ thá»‘ng Ä‘Æ°á»£c thiáº¿t káº¿ riÃªng cho quáº£n lÃ½ sinh viÃªn cáº¥p **Äáº¡i há»c**.

---

## 2. Tech Stack (CÃ´ng Nghá»‡ Sá»­ Dá»¥ng)

### Backend (Python/Django)
- **Framework:** Django 6.x + Django REST Framework.
- **Authentication:** JWT (SimpleJWT) - ÄÄƒng nháº­p nháº­n token.
- **Database:** PostgreSQL (Cloud - Neon.tech).
- **Excel Processing:** `openpyxl`.
- **Testing:** `pytest` + `pytest-django` + `model-bakery`.

### Frontend (JavaScript/React)
- **Build Tool:** Vite.
- **Styling:** Tailwind CSS + **shadcn/ui** (Bá»™ component hiá»‡n Ä‘áº¡i).
- **State Management:** Zustand (Auth/Settings).
- **Data Fetching:** TanStack Query v5 (React Query).
- **Icons:** Lucide React.

---

## 3. Cáº¥u TrÃºc ThÆ° Má»¥c (Directory Structure)

### `/backend`
- `accounts/`: Quáº£n lÃ½ User, vai trÃ² (Admin, Giáº£ng viÃªn, Sinh viÃªn) vÃ  Auth.
- `students/`: Quáº£n lÃ½ há»“ sÆ¡ sinh viÃªn, liÃªn há»‡ kháº©n cáº¥p vÃ  tÃ­nh nÄƒng Excel.
- `teachers/`: Quáº£n lÃ½ thÃ´ng tin Giáº£ng viÃªn vÃ  Khoa/Bá»™ mÃ´n.
- `academics/`: Chá»©a core logic vá» KhÃ³a (Grade), Lá»›p sinh hoáº¡t (Classroom), Há»c pháº§n (Course) vÃ  Äiá»ƒm sá»‘.

### `/frontend`
- `src/api/`: Cáº¥u hÃ¬nh `axiosClient` vÃ  cÃ¡c service API chung.
- `src/features/`: Chia theo module (students, teachers, academics). Má»—i module cÃ³ `api.js` vÃ  `hooks.js` (React Query).
- `src/components/ui/`: CÃ¡c component nguyÃªn tá»­ tá»« shadcn.
- `src/pages/`: CÃ¡c mÃ n hÃ¬nh chÃ­nh cá»§a á»©ng dá»¥ng.

---

## 4. Tiáº¿n Äá»™ Hiá»‡n Táº¡i (Káº¿t ThÃºc Phase 2)

### âœ… ÄÃ£ hoÃ n thÃ nh (100%):
1. **Refactor Äáº¡i há»c:** Chuyá»ƒn Ä‘á»•i toÃ n bá»™ thuáº­t ngá»¯ (Giáº£ng viÃªn, KhÃ³a, Lá»›p sinh hoáº¡t).
2. **Há»‡ thá»‘ng Sinh viÃªn:** CRUD Ä‘áº§y Ä‘á»§ + **Import/Export Excel**.
3. **Há»‡ thá»‘ng Giáº£ng viÃªn:** CRUD Ä‘áº§y Ä‘á»§.
4. **Academics Foundation:** ÄÃ£ cÃ³ giao diá»‡n danh sÃ¡ch cho KhÃ³a, Há»c pháº§n, Lá»›p sinh hoáº¡t.
5. **Testing:** ÄÃ£ cÃ³ bá»™ test backend vÃ  frontend á»•n Ä‘á»‹nh.
6. **Há»‡ thá»‘ng Äiá»ƒm danh (Attendance):** ÄÃ£ hoÃ n thiá»‡n API (Filtering, Bulk Update, Attendance Sheet).
7. **API PhÃ¢n cÃ´ng giáº£ng dáº¡y:** Backend API Ä‘Ã£ sáºµn sÃ ng vá»›i nested data (`classroom_name`, `course_name`, `teacher_name`) vÃ  há»— trá»£ filter (`?classroom=`, `?course=`, `?teacher=`).

### ðŸš§ Äang thá»±c hiá»‡n (Phase 3):
1. HoÃ n thiá»‡n Form ThÃªm/Sá»­a cho Lá»›p sinh hoáº¡t & Há»c pháº§n.
2. XÃ¢y dá»±ng giao diá»‡n Frontend (UI) cho module **PhÃ¢n cÃ´ng giáº£ng dáº¡y** dá»±a trÃªn API Ä‘Ã£ cÃ³.

---

## 5. HÆ°á»›ng Dáº«n CÃ i Äáº·t (Cho NgÆ°á»i Má»›i)

### BÆ°á»›c 1: Clone Repo & Backend Setup
```bash
git clone https://github.com/tungm1204-sudo/QLSV-DJANGO
cd QLSV-DJANGO/backend
# Táº¡o venv vÃ  cÃ i dependencies (náº¿u cÃ³ requirements.txt)
python manage.py migrate
python manage.py runserver
```

### BÆ°á»›c 2: Frontend Setup
```bash
cd ../frontend
npm install
npm run dev
```

### BÆ°á»›c 3: TÃ i khoáº£n Test
- **Trang Login:** `http://localhost:5173/login`
- **TÃ i khoáº£n Admin:** `admin` / `password123`

---

## 6. LÆ°u Ã Quan Trá»ng Cho Dev Má»›i
- **University Logic:** LuÃ´n sá»­ dá»¥ng thuáº­t ngá»¯ "Lá»›p sinh hoáº¡t" thay vÃ¬ "Lá»›p há»c" Ä‘á»ƒ trÃ¡nh nháº§m láº«n vá»›i "Lá»›p há»c pháº§n".
- **API First:** Má»i thao tÃ¡c frontend pháº£i thÃ´ng qua `axiosClient` trong `src/api/`.
- **UI Consistency:** Sá»­ dá»¥ng bá»™ component trong `src/components/ui/`.

## 7. TÃ i Liá»‡u API & Kiáº¿n Thá»©c Cá»‘t LÃµi (Knowledge Items)
Äá»ƒ trÃ¡nh viá»‡c cÃ¡c láº­p trÃ¬nh viÃªn vÃ  AI sau nÃ y pháº£i "Ä‘á»c láº¡i toÃ n bá»™ code", dá»± Ã¡n Ã¡p dá»¥ng há»‡ thá»‘ng ghi nhá»› vÃ  tÃ i liá»‡u hÃ³a:
- **TÃ i liá»‡u Walkthrough:** Báº¥t cá»© khi nÃ o hoÃ n thÃ nh má»™t tÃ­nh nÄƒng, má»™t báº£n bÃ¡o cÃ¡o `walkthrough.md` sáº½ Ä‘Æ°á»£c táº¡o ra Ä‘á»ƒ lÆ°u trá»¯ láº¡i cÃ¡c endpoints má»›i (nhÆ° Bulk Update Äiá»ƒm danh). Báº¡n cÃ³ thá»ƒ tÃ¬m tháº¥y trong lá»‹ch sá»­ thay Ä‘á»•i cá»§a mÃ¬nh.
- **BÃ¡o cÃ¡o nÃ y (`PROJECT_REPORT.md` vÃ  `ONBOARDING_REPORT.md`):** ÄÃ³ng vai trÃ² lÃ  trÃ­ nhá»› dÃ i háº¡n (Long-term memory) chá»©a tÃ³m táº¯t kiáº¿n trÃºc. CÃ¡c AI má»›i khi join vÃ o dá»± Ã¡n cÃ³ thá»ƒ Ä‘á»c file nÃ y Ä‘á»ƒ náº¯m ngay bá»‘i cáº£nh dá»± Ã¡n thay vÃ¬ tá»± scan source code.

---
> *TÃ i liá»‡u cáº­p nháº­t ngÃ y: 08/06/2026 bá»Ÿi Antigravity AI.*

## Cáº­p nháº­t cleanup
- Repo Ä‘Ã£ Ä‘Æ°á»£c dá»n sáº¡ch backend báº±ng cÃ¡ch loáº¡i bá» file local vÃ  artifact khÃ´ng cáº§n thiáº¿t.
- ThÆ° má»¥c `backend/core` hiá»‡n chá»‰ giá»¯ láº¡i cáº¥u trÃºc cáº§n thiáº¿t cho lá»‡nh quáº£n lÃ½: `management/commands/setup_groups.py`.
- `.gitignore` Ä‘Ã£ Ä‘Æ°á»£c má»Ÿ rá»™ng Ä‘á»ƒ bá» qua cÃ¡c file local `*.coverage` vÃ  `pytest_report.txt`.


---

# PHẦN 2: HƯỚNG DẪN ONBOARDING

# BÃ¡o CÃ¡o Onboarding Dá»± Ãn Chi Tiáº¿t (A-Z)

ChÃ o má»«ng báº¡n tham gia dá»± Ã¡n! DÆ°á»›i Ä‘Ã¢y lÃ  bÃ¡o cÃ¡o phÃ¢n tÃ­ch toÃ n diá»‡n vá» há»‡ thá»‘ng hiá»‡n táº¡i, giÃºp báº¡n nhanh chÃ³ng náº¯m báº¯t kiáº¿n trÃºc vÃ  tá»± tin Ä‘Ã³ng gÃ³p vÃ o dá»± Ã¡n.

---

## 1. Tá»•ng Quan Dá»± Ãn & Nghiá»‡p Vá»¥ (Business Logic)

> [!NOTE]
> **BÃ i toÃ¡n giáº£i quyáº¿t:** ÄÃ¢y lÃ  há»‡ thá»‘ng quáº£n lÃ½ sinh viÃªn dÃ nh riÃªng cho mÃ´i trÆ°á»ng **Äáº¡i há»c**. Dá»± Ã¡n Ä‘ang trong quÃ¡ trÃ¬nh chuyá»ƒn Ä‘á»•i (hiá»‡n Ä‘áº¡i hÃ³a) tá»« ná»n táº£ng web monolithic truyá»n thá»‘ng (Django Template) sang kiáº¿n trÃºc Decoupled API-First hiá»‡n Ä‘áº¡i.

- **Äá»‘i tÆ°á»£ng ngÆ°á»i dÃ¹ng hÆ°á»›ng Ä‘áº¿n:**
  - **Admin / GiÃ¡o vá»¥ (Academic Staff):** Quáº£n lÃ½ cáº¥u hÃ¬nh toÃ n há»‡ thá»‘ng, táº¡o dá»¯ liá»‡u gá»‘c (Khoa, KhÃ³a, MÃ´n há»c, Lá»›p), cáº¥u hÃ¬nh há»c ká»³ vÃ  phÃ¢n cÃ´ng giáº£ng dáº¡y.
  - **Giáº£ng viÃªn (Teacher):** Quáº£n lÃ½ thÃ´ng tin lá»›p sinh hoáº¡t/lá»›p há»c pháº§n Ä‘Æ°á»£c phÃ¢n cÃ´ng, thá»±c hiá»‡n Ä‘iá»ƒm danh vÃ  nháº­p Ä‘iá»ƒm sinh viÃªn.
  - **Sinh viÃªn (Student):** Tra cá»©u thÃ´ng tin cÃ¡ nhÃ¢n, xem Ä‘iá»ƒm sá»‘, thá»i khÃ³a biá»ƒu vÃ  lá»‹ch sá»­ Ä‘iá»ƒm danh.

- **TÃ³m táº¯t cÃ¡c chá»©c nÄƒng cá»‘t lÃµi (Core Features):**
  - **Há»‡ thá»‘ng TÃ i khoáº£n & PhÃ¢n quyá»n:** Quáº£n lÃ½ ngÆ°á»i dÃ¹ng táº­p trung vá»›i Role-based Access Control (Admin, GiÃ¡o vá»¥, Giáº£ng viÃªn, Sinh viÃªn).
  - **Quáº£n lÃ½ Há»“ sÆ¡ (Profiles):** Quáº£n lÃ½ chi tiáº¿t sinh viÃªn (kÃ¨m liÃªn há»‡ kháº©n cáº¥p/phá»¥ huynh) vÃ  giáº£ng viÃªn (kÃ¨m thÃ´ng tin khoa/bá»™ mÃ´n). Há»— trá»£ Import/Export Excel dá»¯ liá»‡u sinh viÃªn.
  - **Nghiá»‡p vá»¥ Há»c vá»¥ (Academics):** Quáº£n lÃ½ cáº¥u trÃºc Ä‘Ã o táº¡o bao gá»“m Há»c ká»³, KhÃ³a, Lá»›p sinh hoáº¡t, MÃ´n há»c, PhÃ¢n cÃ´ng giáº£ng dáº¡y, Äiá»ƒm danh vÃ  Quáº£n lÃ½ Äiá»ƒm sá»‘. (VÃ­ dá»¥ API Ä‘iá»ƒm danh: `bulk-update` vÃ  `attendance-sheet` Ä‘Ã£ hoÃ n thiá»‡n; API PhÃ¢n cÃ´ng giáº£ng dáº¡y `/api/assignments/` Ä‘Ã£ há»— trá»£ filter theo Lá»›p/MÃ´n/GV vÃ  tráº£ vá» tÃªn chi tiáº¿t Ä‘á»ƒ lÃ m UI).

---

## 2. Chi Tiáº¿t Báº£n Äá»“ CÃ´ng Nghá»‡ (Tech Stack Analysis)

Dá»± Ã¡n sá»­ dá»¥ng má»™t stack cÃ´ng nghá»‡ ráº¥t hiá»‡n Ä‘áº¡i, chia tÃ¡ch rÃµ rÃ ng giá»¯a Frontend vÃ  Backend.

| TÃªn CÃ´ng Nghá»‡/ThÆ° Viá»‡n | Vai trÃ²/TÃ¡c dá»¥ng cá»¥ thá»ƒ | ÄÃ¡nh giÃ¡ phiÃªn báº£n |
| :--- | :--- | :--- |
| **Django (v5.0+)** | Framework cá»‘t lÃµi á»Ÿ Backend, quáº£n lÃ½ ORM, Model, vÃ  logic nghiá»‡p vá»¥. | Má»›i, báº£o máº­t cao. |
| **Django REST Framework (DRF)** | XÃ¢y dá»±ng há»‡ thá»‘ng API (RESTful) giao tiáº¿p vá»›i Frontend. API-First thay vÃ¬ SSR. | Chuáº©n cÃ´ng nghiá»‡p, á»•n Ä‘á»‹nh. |
| **SimpleJWT** | XÃ¡c thá»±c ngÆ°á»i dÃ¹ng (Authentication) qua JSON Web Token (Access/Refresh token). | Lá»±a chá»n tá»‘t nháº¥t cho SPA. |
| **PostgreSQL (Neon Cloud)** | Database chÃ­nh trÃªn mÃ´i trÆ°á»ng production, lÆ°u trá»¯ dá»¯ liá»‡u quan há»‡. | Hiá»‡n Ä‘áº¡i, cloud-native. |
| **SQLite / pytest-django** | Database nháº¹ dÃ¹ng cho mÃ´i trÆ°á»ng dev/testing Ä‘á»ƒ test cháº¡y siÃªu tá»‘c. | PhÃ¹ há»£p cho CI vÃ  Dev local. |
| **openpyxl** | ThÆ° viá»‡n xá»­ lÃ½ nghiá»‡p vá»¥ Import/Export danh sÃ¡ch sinh viÃªn qua file Excel (`.xlsx`). | TiÃªu chuáº©n vÃ  á»•n Ä‘á»‹nh. |
| **React (v19) + Vite (v8)** | Frontend Single Page Application (SPA). Vite giÃºp build vÃ  reload cá»±c nhanh thay vÃ¬ CRA/Webpack. | Ráº¥t má»›i, hiá»‡u nÄƒng tá»‘i Ä‘a. |
| **Tailwind CSS (v4) + shadcn/ui** | Styling UI. Tailwind giÃºp style nhanh, `shadcn/ui` cung cáº¥p cÃ¡c component Ä‘áº¹p, cÃ³ thá»ƒ tÃ¹y biáº¿n source code. | Äang cá»±c ká»³ trending. |
| **TanStack Query (v5)** | React Query quáº£n lÃ½ server-state: tá»± Ä‘á»™ng fetch, cache, vÃ  Ä‘á»“ng bá»™ dá»¯ liá»‡u API. | PhiÃªn báº£n má»›i, tá»‘i Æ°u tá»‘t. |
| **Zustand (v5)** | Quáº£n lÃ½ global client-state gá»n nháº¹ (nhÆ° session user, auth token). | Nháº¹ vÃ  dá»… hiá»ƒu hÆ¡n Redux. |
| **React Hook Form + Zod** | Xá»­ lÃ½ tráº¡ng thÃ¡i Form vÃ  validate dá»¯ liá»‡u cháº·t cháº½ dá»±a trÃªn schema. | Combo tiÃªu chuáº©n hiá»‡n nay. |

---

## 3. Kiáº¿n TrÃºc Há»‡ Thá»‘ng & Luá»“ng Dá»¯ Liá»‡u (Architecture & Data Flow)

> [!TIP]
> **Kiáº¿n trÃºc:** Há»‡ thá»‘ng Ã¡p dá»¥ng mÃ´ hÃ¬nh **Decoupled Client-Server**. Backend thuáº§n tÃºy chá»‰ tráº£ vá» JSON qua API, vÃ  Frontend lÃ  má»™t SPA hoÃ n toÃ n Ä‘á»™c láº­p.

### Thiáº¿t káº¿ Database (Models)
CÃ¡c model Ä‘Æ°á»£c chia rÃ nh máº¡ch theo tá»«ng domain nghiá»‡p vá»¥:
- Báº£ng **`User`** (AbstractUser) Ä‘Ã³ng vai trÃ² trung tÃ¢m Ä‘á»ƒ Ä‘Äƒng nháº­p, Ä‘i kÃ¨m trÆ°á»ng `role`.
- Báº£ng **`StudentProfile`** vÃ  **`TeacherProfile`** liÃªn káº¿t `OneToOne` vá»›i `User` Ä‘á»ƒ má»Ÿ rá»™ng thÃ´ng tin.
- Module Há»c vá»¥ xoay quanh: **`Grade`** (KhÃ³a) -> **`Classroom`** (Lá»›p sinh hoáº¡t) -> chá»©a **`ClassroomStudent`** (M-N).
- Lá»›p há»c gáº¯n vá»›i **`Semester`** (Há»c ká»³) vÃ  cÃ³ phÃ¢n cÃ´ng **`CourseAssignment`** cho Giáº£ng viÃªn dáº¡y MÃ´n há»c (**`Course`**).

### Luá»“ng Dá»¯ Liá»‡u (Data Flow) - VÃ­ dá»¥ luá»“ng ÄÄƒng nháº­p:
1. **User Action:** NgÆ°á»i dÃ¹ng Ä‘iá»n Form Login á»Ÿ Frontend. `React Hook Form` káº¿t há»£p `Zod` validate email/password ngay táº¡i client.
2. **API Call:** HÃ m xá»­ lÃ½ gá»i API login thÃ´ng qua `axiosClient` (`POST /api/token/`).
3. **Backend Auth:** DRF nháº­n request, xÃ¡c thá»±c qua model `User`. Náº¿u Ä‘Ãºng, `SimpleJWT` sinh ra `access_token` vÃ  `refresh_token` tráº£ vá» JSON.
4. **Client State:** Frontend nháº­n token, lÆ°u vÃ o `Zustand` store (hoáº·c localStorage) Ä‘á»ƒ duy trÃ¬ phiÃªn.
5. **Next Request:** Khi Frontend muá»‘n láº¥y danh sÃ¡ch sinh viÃªn, `TanStack Query` gá»i API kÃ¨m Header `Authorization: Bearer <token>`. DRF nháº­n token, phÃ¢n quyá»n (Permissions), query Model qua ORM, Serializer chuyá»ƒn Ä‘á»•i thÃ nh JSON vÃ  tráº£ vá» cho React render báº£ng.

---

## 4. Cáº¥u TrÃºc ThÆ° Má»¥c & CÃ¡ch Tiáº¿p Cáº­n Code (Codebase Navigation)

### Backend (`/backend`) - Cáº¥u trÃºc Django App
- `qlsv/`: Chá»©a file cáº¥u hÃ¬nh gá»‘c `settings.py` (cáº¥u hÃ¬nh DB, App), `urls.py` (Ä‘á»‹nh tuyáº¿n root API). File `.env` lÆ°u key báº£o máº­t.
- `accounts/`, `students/`, `teachers/`, `academics/`: ÄÃ¢y lÃ  cÃ¡c Module (App). Trong má»—i App báº¡n sáº½ lÃ m viá»‡c vá»›i:
  - `models.py`: NÆ¡i Ä‘á»‹nh nghÄ©a cáº¥u trÃºc báº£ng CSDL (ORM).
  - `serializers.py`: NÆ¡i Ä‘á»‹nh nghÄ©a format JSON tráº£ vá» cho API.
  - `views.py` / `api.py`: NÆ¡i viáº¿t logic API (ViewSets), xá»­ lÃ½ lá»c dá»¯ liá»‡u, pháº§n quyá»n.
  - `urls.py`: NÆ¡i khai bÃ¡o Endpoint (Router).

### Frontend (`/frontend`) - Cáº¥u trÃºc React Feature-based
- `package.json`: Chá»©a script start (`npm run dev`) vÃ  thÆ° viá»‡n.
- `src/api/`: NÆ¡i chá»©a cáº¥u hÃ¬nh Axios (interceptors tá»± Ä‘á»™ng gáº¯n token vÃ o header).
- `src/components/ui/`: ThÆ° má»¥c chá»©a cÃ¡c component atomic cá»§a `shadcn`. (KhÃ´ng nÃªn sá»­a logic á»Ÿ Ä‘Ã¢y, chá»‰ Ä‘á»•i style náº¿u cáº§n).
- `src/features/`: **ÄÃ¢y lÃ  nÆ¡i báº¡n sáº½ code nhiá»u nháº¥t.** Logic Ä‘Æ°á»£c gom theo tÃ­nh nÄƒng (vd: `students`, `teachers`). Má»—i feature sáº½ cÃ³ `api.js` (gá»i endpoint) vÃ  `hooks.js` (TanStack Query hooks).
- `src/pages/`: CÃ¡c View ghÃ©p cÃ¡c component láº¡i vá»›i nhau Ä‘á»ƒ táº¡o thÃ nh giao diá»‡n nguyÃªn trang.

---

## 5. Lá»™ TrÃ¬nh Há»c Cáº¥p Tá»‘c Cho ThÃ nh ViÃªn Má»›i (Accelerated Learning Path)

Äá»ƒ nhanh chÃ³ng náº¯m báº¯t há»‡ thá»‘ng vÃ  commit code, báº¡n hÃ£y theo sÃ¡t lá»™ trÃ¬nh 4 bÆ°á»›c sau:

**BÆ°á»›c 1: Django ORM & DRF (Backend - 2 ngÃ y)**
- **Tá»« khÃ³a cáº§n há»c:** Django Models, QuerySet, ModelSerializer, ModelViewSet, DRF Permissions.
- *Thá»±c hÃ nh:* Äá»c hiá»ƒu file `academics/models.py`. Thá»­ táº¡o má»™t API má»›i Ä‘Æ¡n giáº£n (vÃ­ dá»¥ API Ä‘áº¿m sá»‘ lÆ°á»£ng lá»›p há»c).

**BÆ°á»›c 2: React Core & Tailwind CSS (Frontend UI - 2 ngÃ y)**
- **Tá»« khÃ³a cáº§n há»c:** Functional Component, `useState`, `useEffect`, Utility Classes cá»§a Tailwind.
- *Thá»±c hÃ nh:* Táº¡o má»™t Component tÄ©nh UI báº±ng Tailwind, thá»­ sá»­ dá»¥ng component Button, Input tá»« `shadcn/ui`.

**BÆ°á»›c 3: TanStack Query & Quáº£n lÃ½ Form (Frontend Logic - 2 ngÃ y)**
- **Tá»« khÃ³a cáº§n há»c:** `useQuery` (fetch data), `useMutation` (create/update data), React Hook Form, Zod schema validation.
- *Thá»±c hÃ nh:* Viáº¿t code gá»i API tá»« BÆ°á»›c 1 vÃ o Component BÆ°á»›c 2, Ä‘á»• dá»¯ liá»‡u ra giao diá»‡n. ThÃªm tÃ­nh nÄƒng Search Ä‘Æ¡n giáº£n.

**BÆ°á»›c 4: Authentication Flow (GhÃ©p ná»‘i há»‡ thá»‘ng - 1 ngÃ y)**
- **Tá»« khÃ³a cáº§n há»c:** JWT Lifecycle, Axios Interceptors, Zustand state management.
- *Thá»±c hÃ nh:* Äá»c hiá»ƒu luá»“ng Ä‘Ã­nh kÃ¨m JWT vÃ o request Header táº¡i file cáº¥u hÃ¬nh Axios cá»§a frontend.

---

## 6. ÄÃ¡nh GiÃ¡ Há»‡ Thá»‘ng & Gá»£i Ã HÆ°á»›ng Äi Tiáº¿p Theo (Next Steps)

> [!IMPORTANT]
> **Nháº­n xÃ©t tá»•ng quan:** Dá»± Ã¡n Ä‘ang cÃ³ ná»n táº£ng kiáº¿n trÃºc ráº¥t tá»‘t, tá»• chá»©c codebase sáº¡ch sáº½ vÃ  sá»­ dá»¥ng cÃ¡c cÃ´ng nghá»‡ hiá»‡n Ä‘áº¡i báº¯t ká»‹p xu hÆ°á»›ng. CÃ³ test coverage cÆ¡ báº£n á»Ÿ Backend.

### Ná»£ Ká»¹ Thuáº­t (Technical Debt) & Äiá»ƒm Cáº§n ChÃº Ã
1. **Hiá»‡u suáº¥t Database (N+1 Query Problem):** Do sá»­ dá»¥ng ORM vÃ  DRF Serializer, náº¿u khÃ´ng cáº©n tháº­n khi query cÃ¡c báº£ng liÃªn káº¿t (vÃ­ dá»¥ get danh sÃ¡ch `Classroom` kÃ¨m thÃ´ng tin `Teacher`), API sáº½ báº¯n ra hÃ ng chá»¥c query nhá». Báº¡n cáº§n luÃ´n kiá»ƒm tra vÃ  sá»­ dá»¥ng `select_related` / `prefetch_related` trong queryset cá»§a ViewSet.
2. **Authorization (PhÃ¢n quyá»n):** Cáº§n Ä‘áº£m báº£o cÃ¡c ViewSet á»Ÿ backend khÃ´ng chá»‰ cÃ³ `IsAuthenticated` mÃ  cáº§n custom permission classes (vd: Sinh viÃªn khÃ´ng Ä‘Æ°á»£c phÃ©p gá»i method `DELETE` lá»›p há»c).
3. **MÃ´i trÆ°á»ng DB:** Äang dÃ¹ng SQLite cho Test vÃ  PostgreSQL cho Prod. Äiá»u nÃ y cÃ³ thá»ƒ gÃ¢y lá»—i tiá»m áº©n (OperationalError) liÃªn quan Ä‘áº¿n phÃ¢n biá»‡t chá»¯ hoa/thÆ°á»ng (Case-insensitive) hoáº·c date-time format.

### Äá» Xuáº¥t Cáº£i Tiáº¿n (Recommendations cho Phase tá»›i)
- **Tá»‘i Æ°u hÃ³a (Optimization):** Ãp dá»¥ng Redis Caching cho cÃ¡c API danh má»¥c (Khoa, KhÃ³a, MÃ´n há»c) vÃ¬ cÃ¡c dá»¯ liá»‡u nÃ y Ã­t thay Ä‘á»•i.
- **Báº£o máº­t:** RÃ  soÃ¡t láº¡i viá»‡c xá»­ lÃ½ refresh token, cÃ¢n nháº¯c set `HttpOnly Cookies` thay vÃ¬ lÆ°u token trÃªn client (localStorage) Ä‘á»ƒ chá»‘ng táº¥n cÃ´ng XSS.
- **Tá»± Ä‘á»™ng hÃ³a (DevOps):** Thiáº¿t láº­p GitHub Actions Pipeline. Tá»± Ä‘á»™ng cháº¡y `pytest` vÃ  Frontend Linter (`eslint`) má»—i khi cÃ³ Pull Request, ngÄƒn cháº·n lá»—i tá»« sá»›m.
- **Nghiá»‡p vá»¥:** XÃ¢y dá»±ng UI Frontend cho module PhÃ¢n cÃ´ng giáº£ng dáº¡y (API Backend Ä‘Ã£ sáºµn sÃ ng). Trang bá»‹ tÃ­nh nÄƒng tÃ­nh Äiá»ƒm Trung BÃ¬nh (GPA) á»Ÿ module `ExamResult`.


---

# PHẦN 3: NHẬT KÝ PHÁT TRIỂN (CHANGELOG)

# BÃ¡o CÃ¡o Tá»•ng Há»£p XÃ¢y Dá»±ng QLSV-DJANGO (Fullstack Session)

> TÃ i liá»‡u nÃ y tÃ³m táº¯t toÃ n bá»™ tiáº¿n Ä‘á»™, kiáº¿n trÃºc vÃ  cÃ¡c module Frontend/Backend Ä‘Ã£ Ä‘Æ°á»£c xÃ¢y dá»±ng vÃ  hoÃ n thiá»‡n trong quÃ¡ trÃ¬nh phÃ¡t triá»ƒn há»‡ thá»‘ng Quáº£n lÃ½ Sinh viÃªn (QLSV-DJANGO).

---

## 1. Tá»”NG QUAN KIáº¾N TRÃšC

Há»‡ thá»‘ng Ä‘Æ°á»£c thiáº¿t káº¿ theo mÃ´ hÃ¬nh **Client - Server (SPA)**:
* **Backend**: Django REST Framework (DRF), quáº£n lÃ½ Database (PostgreSQL/Neon.tech), Auth JWT, cung cáº¥p RESTful APIs.
* **Frontend**: React.js (Vite), dÃ¹ng Tailwind CSS & shadcn/ui cho giao diá»‡n. Quáº£n lÃ½ state báº±ng Zustand (Auth) vÃ  TanStack React Query (Server-state/Caching).

---

## 2. NHá»®NG THAY Äá»”I Vá»€ BACKEND (DRF)

Äá»ƒ Ä‘Ã¡p á»©ng giao diá»‡n Ä‘a tÃ­nh nÄƒng cá»§a Frontend, Backend Ä‘Ã£ Ä‘Æ°á»£c má»Ÿ rá»™ng thÃªm cÃ¡c Custom Endpoint vÃ  Serializer Ä‘áº·c thÃ¹ Ä‘á»ƒ tá»‘i Æ°u hiá»‡u suáº¥t (thay vÃ¬ chá»‰ dÃ¹ng CRUD máº·c Ä‘á»‹nh).

### 2.1. API Quáº£n lÃ½ Ghi danh (Enrollment)
* ThÃªm `ClassroomStudentSerializer` Ä‘á»ƒ map trá»±c tiáº¿p thÃ´ng tin SV (tÃªn, mssv, email) thÃ´ng qua báº£ng trung gian.
* Táº¡o `ClassroomStudentViewSet` há»— trá»£ filter sinh viÃªn theo `classroom_id`.
* Route: `GET /POST /DELETE /api/academics/enrollments/`

### 2.2. API Dashboard & Thá»‘ng kÃª
* ThÃªm class `DashboardView` tá»•ng há»£p toÃ n bá»™ sá»‘ liá»‡u: Tá»•ng sá»‘ SV/GV, MÃ´n há»c, Tá»‰ lá»‡ Ä‘iá»ƒm danh 7 ngÃ y qua, Top lá»›p Ä‘Ã´ng sinh viÃªn.
* Route: `GET /api/academics/dashboard/`

### 2.3. API Nháº­p Äiá»ƒm & Káº¿t Quáº£ Há»c Táº­p (Exam Results)
* `GET /api/academics/exam-results/grade-sheet/`: Tráº£ vá» danh sÃ¡ch sinh viÃªn trong lá»›p kÃ¨m theo Ä‘iá»ƒm cÅ© (náº¿u cÃ³) táº¡o thÃ nh báº£ng Ä‘iá»ƒm trá»‘ng Ä‘á»ƒ GV nháº­p.
* `POST /api/academics/exam-results/bulk-update/`: Cho phÃ©p lÆ°u hÃ ng loáº¡t báº£ng Ä‘iá»ƒm cá»§a cáº£ lá»›p chá»‰ trong 1 request.
* `GET /api/academics/exam-results/student-gpa/`: TÃ­nh toÃ¡n TÃ­n chá»‰ tÃ­ch lÅ©y, GPA há»‡ 10 vÃ  GPA há»‡ 4 báº±ng Python (Backend).

---

## 3. NHá»®NG THAY Äá»”I Vá»€ FRONTEND (REACT)

Frontend ban Ä‘áº§u chá»‰ cÃ³ mÃ n hÃ¬nh Login vÃ  2 danh sÃ¡ch Ä‘Æ¡n giáº£n. Hiá»‡n táº¡i Ä‘Ã£ hoÃ n thiá»‡n thÃ nh má»™t **Portal Quáº£n lÃ½ ÄÃ o táº¡o** Ä‘áº§y Ä‘á»§ vá»›i **10 modules lá»›n**.

### 3.1. CÃ¡c Module Quáº£n lÃ½ Dá»¯ liá»‡u (CRUD)
Sá»­ dá»¥ng Dialog forms káº¿t há»£p `useMutation` Ä‘á»ƒ lÃ m ThÃªm/Sá»­a/XÃ³a mÆ°á»£t mÃ :
* **Há»c pháº§n (Courses)**: Quáº£n lÃ½ mÃ´n, sá»‘ tÃ­n chá»‰.
* **Lá»›p sinh hoáº¡t (Classrooms)**: Quáº£n lÃ½ lá»›p, khÃ³a, há»c ká»³, GV chá»§ nhiá»‡m.
* **PhÃ¢n cÃ´ng giáº£ng dáº¡y (Assignments)**: Quáº£n lÃ½ GV nÃ o dáº¡y mÃ´n nÃ o, lá»›p nÃ o (cÃ³ validate chá»‘ng trÃ¹ng láº·p).

### 3.2. Cáº¥u HÃ¬nh Há»‡ Thá»‘ng (Academics Config)
* XÃ¢y dá»±ng **Trang cáº¥u hÃ¬nh gá»™p 3 Tabs**: Há»c ká»³, KhÃ³a há»c, Loáº¡i ká»³ thi.
* Giao diá»‡n gá»n gÃ ng, giÃºp Admin thiáº¿t láº­p dá»¯ liá»‡u ná»n mÃ  khÃ´ng cáº§n vÃ o trang `/admin` gá»‘c cá»§a Django.

### 3.3. CÃ¡c TÃ­nh NÄƒng Nghiá»‡p Vá»¥ (Bulk Operations)
* **SV trong Lá»›p (Enrollments)**: Giao diá»‡n Split-pane (trÃ¡i chá»n lá»›p, pháº£i hiá»‡n SV). CÃ³ tÃ­nh nÄƒng tÃ¬m kiáº¿m vÃ  thÃªm SV vÃ o lá»›p. Ãp dá»¥ng **Optimistic Updates** giÃºp thao tÃ¡c ThÃªm/XÃ³a SV diá»…n ra vá»›i Ä‘á»™ trá»… 0ms.
* **Äiá»ƒm danh (Attendance)**: Nháº­p Ä‘iá»ƒm danh theo Lá»›p + NgÃ y. TÃ­ch há»£p radio buttons (CÃ³ máº·t/Muá»™n/Váº¯ng/PhÃ©p).
* **Nháº­p Ä‘iá»ƒm (Enter Grades)**: Giao diá»‡n dáº¡ng Spreadsheet (báº£ng tÃ­nh). Chá»n filter (Há»c ká»³, Lá»›p, MÃ´n, Loáº¡i ká»³ thi) Ä‘á»ƒ bung ra báº£ng nháº­p Ä‘iá»ƒm cho toÃ n lá»›p.

### 3.4. Cá»•ng ThÃ´ng Tin Sinh ViÃªn (Student Portal)
* **Káº¿t quáº£ há»c táº­p**: Hiá»ƒn thá»‹ 3 chá»‰ sá»‘ lá»›n (TÃ­n chá»‰, GPA 10, GPA 4) thÃ´ng qua Card UI, vÃ  báº£ng chi tiáº¿t Ä‘iá»ƒm tá»•ng káº¿t tá»«ng mÃ´n há»c.

### 3.5. Dashboard & Sidebar PhÃ¢n Quyá»n
* **Dashboard má»›i**: Hiá»ƒn thá»‹ Biá»ƒu Ä‘á»“ cá»™t Ä‘iá»ƒm danh 7 ngÃ y, Donut chart phÃ¢n bá»‘ Ä‘iá»ƒm danh, vÃ  Top lá»›p.
* **Sidebar Layout**: Render linh hoáº¡t tÃ¹y vÃ o `user.role` (Admin tháº¥y toÃ n bá»™, Giáº£ng viÃªn tháº¥y lá»›p/nháº­p Ä‘iá»ƒm, Sinh viÃªn chá»‰ tháº¥y GPA).

---

## 4. Tá»I Æ¯U HÃ“A & FIX BUG (HIGHLIGHTS)

1. **Hiá»‡u suáº¥t & Caching**: Sá»­ dá»¥ng triá»‡t Ä‘á»ƒ cÆ¡ cháº¿ invalidation cá»§a `React Query`. VÃ­ dá»¥: Vá»«a thÃªm MÃ´n há»c â†’ tá»± Ä‘á»™ng load láº¡i API list.
2. **Optimistic Updates (Giao diá»‡n tá»©c thÃ¬)**: Sá»­a váº¥n Ä‘á» máº¡ng cháº­m á»Ÿ trang *Sinh viÃªn trong lá»›p* báº±ng cÃ¡ch lá»«a UI cáº­p nháº­t trÆ°á»›c, gá»i API ngáº§m sau.
3. **Sá»­a lá»—i cáº¥u trÃºc Dá»¯ liá»‡u**: Kháº¯c phá»¥c lá»—i nháº§m láº«n giá»¯a truyá»n Object vs ID khi POST payload lÃªn Django.
4. **VÆ°á»£t rÃ o Cáº£n UI**: Tá»± code CSS flex/grid cÃ¡c biá»ƒu Ä‘á»“ cá»™t (Bar chart, Progress bar) trÃªn Dashboard mÃ  khÃ´ng cáº§n cÃ i thÃªm thÆ° viá»‡n Recharts hay Chart.js nháº±m giá»¯ project nháº¹.

---

## 5. Báº¢O Máº¬T & DEVOPS (Cáº¬P NHáº¬T Má»šI)

1. **Báº£o máº­t JWT Token**: Chuyá»ƒn Ä‘á»•i phÆ°Æ¡ng thá»©c lÆ°u trá»¯ `refresh_token` tá»« `localStorage` sang **HttpOnly Cookies**. TrÃ¬nh duyá»‡t sáº½ tá»± Ä‘á»™ng Ä‘Ã­nh kÃ¨m cookie nÃ y á»Ÿ má»—i request refresh token mÃ  khÃ´ng lÃ m lá»™ token ra Javascript, ngÄƒn cháº·n triá»‡t Ä‘á»ƒ táº¥n cÃ´ng XSS. Backend Ä‘Ã£ Ä‘Æ°á»£c custom láº¡i `CookieTokenRefreshView` vÃ  `LogoutView` Ä‘á»ƒ xá»­ lÃ½ cookie.
2. **PhÃ¢n quyá»n tuá»³ chá»‰nh (Custom Permissions)**: XÃ¢y dá»±ng cÃ¡c rules phÃ¢n quyá»n dá»±a trÃªn `Role` cá»§a user (Admin, Teacher, Student) trong file `accounts/permissions.py`. VÃ­ dá»¥ `IsAdminOrReadOnly` cho cÃ¡c API quáº£n lÃ½ KhÃ³a/Lá»›p, vÃ  `IsAdminOrTeacher` cho cÃ¡c API nháº­p Ä‘iá»ƒm/Ä‘iá»ƒm danh.
3. **Tá»‘i Æ°u Database**: ÄÃ£ rÃ  soÃ¡t cÃ¡c ViewSet trong module Academics Ä‘á»ƒ thiáº¿t láº­p `select_related` vÃ  `prefetch_related`, dá»n dáº¹p hoÃ n toÃ n váº¥n Ä‘á» N+1 query.
4. **CI/CD Pipeline**: TÃ­ch há»£p GitHub Actions Workflow (`ci.yml`) Ä‘á»ƒ tá»± Ä‘á»™ng cháº¡y kiá»ƒm thá»­ cho Frontend (npm run lint) vÃ  Backend (pytest) má»—i khi cÃ³ Push hoáº·c Pull Request.

---

## 6. HÆ¯á»šNG DáºªN DÃ€NH CHO NGÆ¯á»œI VÃ€O SAU

### Khá»Ÿi cháº¡y dá»± Ã¡n
```bash
# Terminal 1: Backend
cd backend
venv\Scripts\activate
python manage.py runserver

# Terminal 2: Frontend
cd frontend
npm run dev
```

### CÃ¡ch tiáº¿p cáº­n Codebase
* **Backend API**: Má»i logic phá»©c táº¡p Ä‘Æ°á»£c viáº¿t á»Ÿ `backend/academics/views.py` (sá»­ dá»¥ng `@action(detail=False)`).
* **Frontend Hooks**: CÃ¡c lá»‡nh gá»i API Ä‘Æ°á»£c gom háº¿t vÃ o `frontend/src/features/academics/hooks.js`. Náº¿u cáº§n gá»i API má»›i, hÃ£y Ä‘á»‹nh nghÄ©a hÃ m á»Ÿ file `api.js` sau Ä‘Ã³ bá»c nÃ³ qua 1 custom hook `useQuery/useMutation` táº¡i file nÃ y.

> **Tráº¡ng thÃ¡i Database (Neon.tech)**: VÃ¬ dÃ¹ng gÃ³i Free Tier, náº¿u tháº¥y Backend quÄƒng lá»—i `psycopg2.OperationalError` khÃ´ng thá»ƒ resolve DNS, nguyÃªn nhÃ¢n lÃ  DB Ä‘Ã£ bá»‹ Pause do khÃ´ng ai dÃ¹ng trong 5 phÃºt. Giáº£i phÃ¡p: VÃ o console.neon.tech Ä‘á»ƒ áº¥n nÃºt Resume.

