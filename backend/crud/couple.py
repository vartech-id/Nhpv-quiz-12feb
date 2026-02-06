from sqlalchemy.orm import Session
from sqlalchemy import select, func

from models.couple_session import CoupleSession
from models.question import Question
from models.session_question import SessionQuestion

from datetime import datetime
from models.couple_result import CoupleResult
from models.player_result import PlayerResult


def create_couple_session(db: Session, male_name: str, female_name: str) -> CoupleSession:
    cs = CoupleSession(male_name=male_name, female_name=female_name, status="created")
    db.add(cs)
    db.commit()
    db.refresh(cs)
    return cs


def get_couple_session(db: Session, couple_session_id: int) -> CoupleSession | None:
    return db.get(CoupleSession, couple_session_id)


def _seed_questions_if_empty(db: Session) -> None:
    count = db.scalar(select(func.count(Question.id)))
    if count and count > 0:
        return

    # Format: (question_text, option_a, option_b, correct_answer)
    male_seed = [
        ('"Aku Kangen" Artinya...', "Dia pura-pura aja", "Dia beneran kangen dan ingin dimanja sama kamu", "B"),
        ('"Tidur Yuk!" Artinya...', "Dia sebenernya bosen ngobrol dan pengen aktivitas lain", "Dia ngajak tidur beneran", "A"),
        ('"Gapapa kok aman aja" Artinya...', "Dia lagi capek / stress", "Dia beneran gak kenapa-kenapa", "A"),
        ('"Terserah" Artinya...', "Dia santai dan setuju apa aja", "Dia kecewa tapi males debat", "B"),
        ('"Bebas" Artinya...', "Dia ngasih kamu ruang buat milih", "Dia berharap kamu peka dan milih yang dia mau", "B"),
        ('"Aku lagi males" Artinya...', "Dia cuma lelah", "Dia butuh ditemenin tapi gak enak bilang", "B"),
        ('"Yaudah" Artinya...', "Dia menerima dengan ikhlas", "Dia kesel tapi menahan diri", "B"),
    ]

    female_seed = [
        ('"Aku Kangen" Artinya...', "Dia pura-pura aja", "Dia beneran kangen dan ingin dimanja sama kamu", "B"),
        ('"Tidur Yuk!" Artinya...', "Dia sebenernya bosen ngobrol dan pengen aktivitas lain", "Dia ngajak tidur beneran", "A"),
        ('"Gapapa kok aman aja" Artinya...', "Dia lagi capek / stress", "Dia beneran gak kenapa-kenapa", "A"),
        ('"Terserah" Artinya...', "Dia santai dan setuju apa aja", "Dia kecewa tapi males debat", "B"),
        ('"Bebas" Artinya...', "Dia ngasih kamu ruang buat milih", "Dia berharap kamu peka dan milih yang dia mau", "B"),
        ('"Aku lagi males" Artinya...', "Dia cuma lelah", "Dia butuh ditemenin tapi gak enak bilang", "B"),
        ('"Yaudah" Artinya...', "Dia menerima dengan ikhlas", "Dia kesel tapi menahan diri", "B"),
    ]

    # Insert male
    for qtext, a, b, correct in male_seed:
        db.add(
            Question(
                question_text=qtext,
                option_a=a,
                option_b=b,
                correct_answer=correct,
                target="male",
            )
        )

    # Insert female
    for qtext, a, b, correct in female_seed:
        db.add(
            Question(
                question_text=qtext,
                option_a=a,
                option_b=b,
                correct_answer=correct,
                target="female",
            )
        )

    db.commit()


def get_or_assign_questions(db: Session, couple_session_id: int, player: str, n: int = 5) -> list[Question]:
    _seed_questions_if_empty(db)

    existing = db.scalars(
        select(SessionQuestion)
        .where(
            SessionQuestion.couple_session_id == couple_session_id,
            SessionQuestion.player == player
        )
        .order_by(SessionQuestion.order_index.asc())
    ).all()

    # Kalau sudah ada 5, kembalikan urutannya sesuai assignment
    if len(existing) == n:
        q_ids = [x.question_id for x in existing]
        questions = db.scalars(select(Question).where(Question.id.in_(q_ids))).all()
        q_map = {q.id: q for q in questions}
        return [q_map[qid] for qid in q_ids]

    # kalau ada partial (misal 1-4), bersihin dulu
    if existing:
        for row in existing:
            db.delete(row)
        db.commit()

    # Assign new set (random) sesuai target
    candidates = db.scalars(
        select(Question)
        .where(Question.target == player)
        .order_by(func.random())
        .limit(n)
    ).all()

    if len(candidates) < n:
        raise ValueError(f"Not enough questions for target={player}. Need at least {n}.")

    # Simpan assignment (lock) 5 soal untuk session+player
    for idx, q in enumerate(candidates, start=1):
        db.add(
            SessionQuestion(
                couple_session_id=couple_session_id,
                player=player,
                order_index=idx,
                question_id=q.id,
            )
        )

    db.commit()
    return candidates


def _get_assigned_question_ids(db: Session, couple_session_id: int, player: str) -> list[int]:
    rows = db.scalars(
        select(SessionQuestion)
        .where(SessionQuestion.couple_session_id == couple_session_id, SessionQuestion.player == player)
        .order_by(SessionQuestion.order_index.asc())
    ).all()
    return [r.question_id for r in rows]


def _compute_score(db: Session, answers: list[dict], allowed_question_ids: set[int]) -> int:
    # answers: [{"question_id":..., "answer":"A"}...]
    # validate ids
    for a in answers:
        if a["question_id"] not in allowed_question_ids:
            raise ValueError("Answer contains question_id not assigned to this session/player")

    q_ids = [a["question_id"] for a in answers]
    questions = db.scalars(select(Question).where(Question.id.in_(q_ids))).all()
    q_map = {q.id: q for q in questions}

    score = 0
    for a in answers:
        ans = (a["answer"] or "").strip().upper()
        if ans not in ("A", "B"):
            raise ValueError("Answer must be 'A' or 'B'")
        if q_map[a["question_id"]].correct_answer.upper() == ans:
            score += 1
    return score


def submit_player_answers(db: Session, couple_session_id: int, player: str, answers: list[dict]) -> int:
    # Prevent double submit
    existing_res = db.scalar(
        select(PlayerResult).where(
            PlayerResult.couple_session_id == couple_session_id,
            PlayerResult.player == player
        )
    )
    if existing_res:
        raise ValueError("Player already submitted")

    assigned_ids = _get_assigned_question_ids(db, couple_session_id, player)
    if len(assigned_ids) != 5:
        raise ValueError("Questions not assigned yet. Call GET questions first.")

    if len(answers) != 5:
        raise ValueError("Must submit exactly 5 answers")

    # Optional strict: ensure same set count (ignores order)
    allowed_set = set(assigned_ids)
    score = _compute_score(db, answers, allowed_set)

    db.add(PlayerResult(couple_session_id=couple_session_id, player=player, score=score))
    db.commit()
    return score


def get_player_score(db: Session, couple_session_id: int, player: str) -> int | None:
    res = db.scalar(
        select(PlayerResult).where(
            PlayerResult.couple_session_id == couple_session_id,
            PlayerResult.player == player
        )
    )
    return res.score if res else None

def upsert_couple_result(db, cs):
    now = datetime.utcnow()
    if cs.completed_at is None:
        cs.completed_at = now

    existing = db.scalar(select(CoupleResult).where(CoupleResult.couple_session_id == cs.id))
    if existing:
        existing.male_name = cs.male_name
        existing.female_name = cs.female_name
        existing.male_score = cs.male_score or 0
        existing.female_score = cs.female_score or 0
        existing.total_players = 2
        existing.created_at = cs.created_at
        existing.completed_at = cs.completed_at
        db.commit()
        return existing

    r = CoupleResult(
        couple_session_id=cs.id,
        male_name=cs.male_name,
        female_name=cs.female_name,
        male_score=cs.male_score or 0,
        female_score=cs.female_score or 0,
        total_players=2,
        created_at=cs.created_at,
        completed_at=cs.completed_at,
    )
    db.add(r)
    db.commit()
    return r

def compute_score(db, answers: list[dict]) -> int:
    q_ids = [a["question_id"] for a in answers]
    q_list = db.scalars(select(Question).where(Question.id.in_(q_ids))).all()
    q_map = {q.id: q for q in q_list}

    score = 0
    for a in answers:
        q = q_map.get(a["question_id"])
        if q and a["answer"] == q.correct_answer:
            score += 1
    return score


