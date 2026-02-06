# Couple Quiz Frontend

Dokumentasi ini menjelaskan cara menjalankan frontend aplikasi Couple Quiz.

## Requirements
- Bun

## Install
```bash
cd frontend
bun install
```

## Development
```bash
bun run dev
```

## Build
```bash
bun run build
bun run preview
```

## Backend URL
Frontend memanggil backend dengan base URL `http://localhost:8000`.
Jika backend berjalan di host atau port lain, ubah di file:
- `frontend/src/views/Register.vue`
- `frontend/src/views/Question.vue`
- `frontend/src/views/Score.vue`

## Routes
- `/` Welcome
- `/register` Register pemain
- `/male/welcome` Intro pemain male
- `/female/welcome` Intro pemain female
- `/:player(male|female)/q/:no` Halaman soal 1..5
- `/:player(male|female)/score` Halaman skor pemain
- `/switching` Instruksi ganti pemain
- `/end` Halaman selesai

## Alur UI
1. Welcome -> Register
2. Register membuat sesi dan menyimpan data di localStorage
3. Male menjawab 5 soal -> score -> switching
4. Female menjawab 5 soal -> score -> end

## Local Storage
- `sessionId`, `maleName`, `femaleName`
- `questions_<sessionId>_male`, `questions_<sessionId>_female`
- `answers_<sessionId>_male`, `answers_<sessionId>_female`
