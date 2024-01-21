# millionlive-millishira-parser
#ミリアニムビナナ異文化交流 最高！

## Usage

前提：Google CloudのDocument AIでProcessorを作っている

```sh
% python documentai_ocr.py \
    --project_id <GCPプロジェクトのID> \
    --location us \
    --processor_id <ProcessorのID> \
    <path to PDF or image> \
    data/ocr_raw/spam.json
```

```sh
% python parse_response.py data/ocr_raw/spam.json data/parsed_docs/spam.jsonl
```

エミリーちゃんの評を抜き出し

```sh
% jq -c 'select(.upper_left.y >= 1350)' data/parsed_docs/spam.jsonl | jq -c 'select(.bottom_right.x <= 450)' | jq -c 'select(.upper_left.x >= 330)' | jq -r '.text | gsub("\n"; "")'
```
