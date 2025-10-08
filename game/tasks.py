import logging
from celery import shared_task
from django.db import transaction
from .models import Game, Submission

from celery import shared_task
from django.utils import timezone
from .models import Game

log = logging.getLogger(__name__)

def validate_word(word: str, lang: str, board_seed: str) -> tuple[bool, str | None, float]:
    # TODO: reemplazar por tu servicio real (categorias/lexicon)
    if len(word) < 3:
        return False, "too_short", 0.0
    return True, None, 0.5  # rarity fake

def score_word(word: str, rarity: float) -> int:
    # regla simple: largo * (1 + rarity)
    return int(len(word) * (1 + rarity))

@shared_task(name="game.validate_and_score_word")
def validate_and_score_word(game_id: int, submission_id: int):
    try:
        with transaction.atomic():
            sub = Submission.objects.select_for_update().get(id=submission_id, game_id=game_id)
            g = Game.objects.select_for_update().get(id=game_id)
            ok, reason, rarity = validate_word(sub.word, sub.lang, g.board_seed)
            if not ok:
                sub.accepted = False
                sub.delta = 0
                sub.save(update_fields=["accepted", "delta"])
                log.info("word.validated", extra={"game_id": g.id, "word": sub.word, "valid": False, "reason": reason})
                return

            delta = score_word(sub.word, rarity)
            sub.accepted = True
            sub.delta = delta
            sub.save(update_fields=["accepted", "delta"])

            g.total_score = (g.total_score or 0) + delta
            g.save(update_fields=["total_score"])

            log.info("score.updated", extra={"game_id": g.id, "delta": delta, "total": g.total_score})
    except Exception as e:
        log.exception("validate_and_score_word failed", extra={"game_id": game_id, "submission_id": submission_id})
        raise



@shared_task
def expire_games():
    Game.objects.filter(status=Game.Status.RUNNING, finished_at__isnull=True)\
        .filter(created_at__lt=timezone.now() - timezone.timedelta(minutes=3))\
        .update(status=Game.Status.FINISHED, finished_at=timezone.now())