import argparse
import json
from operator import itemgetter

import jsonlines


def get_upper_left(vertices):
    """
    >>> get_upper_left([{"x":150,"y":347},{"x":1094,"y":340},{"x":1094,"y":392},{"x":150,"y":399}])
    {'x': 150, 'y': 347}
    >>> get_upper_left([{"x":150,"y":347},{"x":1094,"y":340},{"x":1094,"y":392},{"x":149,"y":399}])
    {'x': 150, 'y': 347}
    """
    # xの値が1番目と2番目に小さい座標2つのうち、yも小さい方を返す
    candidate1, candidate2 = sorted(vertices, key=itemgetter("x"))[:2]
    if candidate1["y"] <= candidate2["y"]:
        return candidate1
    else:
        return candidate2


def get_bottom_right(vertices):
    """
    >>> get_bottom_right([{"x":150,"y":347},{"x":1094,"y":340},{"x":1094,"y":392},{"x":150,"y":399}])
    {'x': 1094, 'y': 392}
    >>> get_bottom_right([{"x":150,"y":347},{"x":1094,"y":340},{"x":1094,"y":392},{"x":150,"y":392}])
    {'x': 1094, 'y': 392}
    """
    # yの値が1番目と2番目に大きい座標2つのうち、xも大きい方を返す
    candidate1, candidate2 = sorted(
        vertices, key=itemgetter("y"), reverse=True
    )[:2]
    if candidate1["x"] <= candidate2["x"]:
        return candidate2
    else:
        return candidate1


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("ocr_result_json")
    parser.add_argument("parse_result_jsonl")
    args = parser.parse_args()

    with open(args.ocr_result_json) as f:
        document = json.load(f)

    text = document["text"]
    paragraphs = []
    for page in document["pages"]:
        for paragraph_number, paragraph in enumerate(page["paragraphs"]):
            layout = paragraph["layout"]
            text_segments = layout["text_anchor"]["text_segments"]
            assert len(text_segments) == 1
            text_segment = text_segments[0]
            start_index = int(text_segment["start_index"])
            end_index = int(text_segment["end_index"])

            bounding_vertices = layout["bounding_poly"]["vertices"]
            assert len(bounding_vertices) == 4
            upper_left = get_upper_left(bounding_vertices)
            bottom_right = get_bottom_right(bounding_vertices)

            paragraphs.append(
                {
                    "page": page["page_number"],
                    "number": paragraph_number,
                    "text": text[start_index:end_index],
                    "upper_left": upper_left,
                    "bottom_right": bottom_right,
                }
            )

    with jsonlines.open(args.parse_result_jsonl, "w") as writer:
        writer.write_all(paragraphs)
