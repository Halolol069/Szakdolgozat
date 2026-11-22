from collections import Counter

from Model.database import Modell


def build_model_labels(models):
    name_counts = Counter(m.name for m in models)
    labels = []
    label_map = {}
    for m in models:
        if name_counts[m.name] > 1:
            label = f"{m.name} ({m.generation}. generáció, #{m.id})"
        else:
            label = m.name
        labels.append(label)
        label_map[label] = m.id
    return labels, label_map

def resolve_model_id(session, label, label_map=None):
    if label_map and label in label_map:
        return label_map[label]
    matches = session.query(Modell.id).filter(Modell.name == label).limit(2).all()
    if len(matches) == 1:
        return matches[0][0]
    return None