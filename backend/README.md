# Couple Quiz Backend

Dokumentasi ini menjelaskan struktur, cara menjalankan, dan API untuk backend kuis pasangan.

**Overview**
Backend ini menggunakan FastAPI dan SQLAlchemy. Fungsinya adalah membuat sesi kuis untuk pasangan, membagikan pertanyaan, menerima jawaban, menghitung skor, dan menyediakan report Excel.

**Tech Stack**
- FastAPI
- SQLAlchemy
- SQLite
- OpenPyXL (export Excel)

**Struktur**
| Path | Deskripsi |
| --- | --- |
| `backend/main.py` | Entry point FastAPI dan definisi endpoint. |
| `backend/db/base.py` | Deklarasi `Base` SQLAlchemy. |
| `backend/db/session.py` | Konfigurasi engine, session lokal, dan dependency `get_db`. |
| `backend/models/question.py` | Model pertanyaan. |
| `backend/models/couple_session.py` | Model sesi pasangan. |
| `backend/models/session_question.py` | Relasi sesi ke pertanyaan. |
| `backend/models/player_result.py` | Hasil jawaban dan skor per pemain. |
| `backend/models/couple_result.py` | Snapshot hasil akhir untuk report. |
| `backend/schemas/couple.py` | Skema request/response terkait sesi. |
| `backend/schemas/question.py` | Skema pertanyaan untuk API. |
| `backend/crud/couple.py` | Logika bisnis sesi, penugasan pertanyaan, dan skor. |
| `backend/quiz_booth_a.db` | File database SQLite (dibuat saat pertama kali jalan). |

**Setup**
1. Pastikan Python >= 3.12.
2. Buat virtual environment.
3. Install dependencies (minimal):

```bash
pip install fastapi uvicorn sqlalchemy openpyxl
```

**Menjalankan Server**
Jalankan dari folder `backend`:

```bash
uvicorn main:app --reload
```

**Konfigurasi Database**
- Default: SQLite
- Lokasi: `backend/quiz_booth_a.db`
- Konfigurasi ada di `backend/db/session.py` pada `DATABASE_URL`.

**CORS**
- CORS dibuka untuk semua origin di `backend/main.py`.

**API**
`POST /couple-sessions`
Request body:

```json
{
  "male_name": "Andi",
  "female_name": "Bunga"
}
```

Response:

```json
{
  "id": 1,
  "current_player": "male"
}
```

`GET /couple-sessions/{couple_session_id}/questions?player=male|female`
Response (5 pertanyaan):

```json
{
  "questions": [
    {
      "id": 1,
      "question_text": "...",
      "option_a": "...",
      "option_b": "...",
      "correct_answer": "A"
    }
  ]
}
```

Aturan alur:
- `player=male` hanya valid saat status `created` atau `male_done`.
- `player=female` hanya valid saat status `male_done`.

`POST /couple-sessions/{couple_session_id}/submit`
Request body:

```json
{
  "player": "male",
  "answers": [
    { "question_id": 1, "answer": "A" }
  ]
}
```

Response saat `player=male`:

```json
{
  "player": "male",
  "score": 3,
  "next_player": "female"
}
```

Response saat `player=female` (final):

```json
{
  "male_score": 3,
  "female_score": 4,
  "status": "done"
}
```

`GET /couple-sessions/{couple_session_id}`
Response:

```json
{
  "id": 1,
  "male_name": "Andi",
  "female_name": "Bunga",
  "status": "male_done",
  "male_score": 3,
  "female_score": null,
  "created_at": "2026-02-06T15:40:00",
  "completed_at": null
}
```

`GET /reports/couple-results.xlsx`
- Download report Excel.
- Kolom: `result_id`, `couple_session_id`, `male_name`, `female_name`, `male_score`, `female_score`, `total_players`, `created_at`, `completed_at`.

**Alur Kuis**
1. Buat sesi dengan `POST /couple-sessions`.
2. Pemain male mengambil pertanyaan dan submit jawaban.
3. Pemain female mengambil pertanyaan dan submit jawaban.
4. Cek skor dan status lewat `GET /couple-sessions/{id}`.
5. (Opsional) Download report dengan `GET /reports/couple-results.xlsx`.

**Status Sesi**
- `created`: sesi baru, male belum submit.
- `male_done`: male sudah submit, female boleh mulai.
- `done`: female selesai, skor final tersedia.

**Error Umum**
- `404 Session not found` jika ID sesi tidak ada.
- `400` untuk invalid `player` atau alur tidak sesuai status.

**Catatan Pengembangan**
- `Base.metadata.create_all(bind=engine)` dipanggil saat startup. Pastikan semua model di-import setidaknya sekali sebelum baris ini (sudah terjadi via `main.py` dan `crud/couple.py`).
- Pertanyaan akan di-seed otomatis jika tabel `questions` kosong saat pertama kali `GET /questions` dipanggil.
