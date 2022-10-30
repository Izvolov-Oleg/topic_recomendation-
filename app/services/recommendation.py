from loguru import logger
import numpy as np
from typing import List

from app.models.user import UserPreferences
from app.db.database import database
from app.utils import timer
from app.data import (
    scenario_skills,
    topic2skill,
    TOP_K, TOP_V
)


def get_candidate_topics(embedding: List[float]) -> List[str]:
    scores = np.array(embedding).dot(np.array(database).T)
    top_indices = np.argsort(scores)[::-1]
    similarity_vector = np.sum(np.array([database[top_idx] for top_idx in top_indices[:TOP_V]]), 0)
    candidate_topics_idx = np.argsort(similarity_vector)[::-1][:TOP_K]
    candidate_topics = [scenario_skills[idx] for idx in candidate_topics_idx]
    return candidate_topics


def handler(user_prefer: UserPreferences) -> List[List[str]]:
    with timer('topic_recommendation'):
        logger.info(f'Request data - {user_prefer.dict()}')

        candidate_topics_batch = []

        for active_skills, cobot_topics in zip(user_prefer.active_skills,
                                               user_prefer.cobot_topics):
            try:
                skills_dict = {skill: 0 for skill in scenario_skills}

                for skill in active_skills:
                    if skill in scenario_skills:
                        skills_dict[skill] += 1

                for topic in cobot_topics:
                    if topic in topic2skill.keys():
                        skill = topic2skill[topic]
                        skills_dict[skill] += 1

                total_skill = sum(skills_dict.values())
                embedding = [skills_dict[skill] / total_skill if total_skill > 0 else 0 for skill in scenario_skills]
                used_topics = [skill for skill in scenario_skills if skills_dict[skill] > 0]
                candidate_topics = get_candidate_topics(embedding)

                candidate_topics = [skill for skill in candidate_topics if skill not in used_topics]

                if "game_cooperative_skill" in candidate_topics:
                    candidate_topics += ["dff_gaming_skill"]

                candidate_topics_batch.append(candidate_topics)
            except Exception as exc:
                logger.exception(exc)
                candidate_topics_batch.append([])

        logger.info(candidate_topics_batch)
        return candidate_topics_batch
