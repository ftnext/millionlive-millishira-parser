import argparse
import json
import mimetypes

from google.api_core.client_options import ClientOptions
from google.cloud import documentai

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("ocr_target_file")
    parser.add_argument("response_json_file")
    parser.add_argument("--project_id", required=True)
    parser.add_argument("--location", choices=("us", "eu"), required=True)
    parser.add_argument("--processor_id", required=True)
    args = parser.parse_args()

    client = documentai.DocumentProcessorServiceClient(
        client_options=ClientOptions(
            api_endpoint=f"{args.location}-documentai.googleapis.com"
        )
    )
    name = client.processor_path(
        args.project_id, args.location, args.processor_id
    )

    with open(args.ocr_target_file, "rb") as image:
        image_content = image.read()
    mime_type, _ = mimetypes.guess_type(args.ocr_target_file)
    raw_document = documentai.RawDocument(
        content=image_content, mime_type=mime_type
    )

    request = documentai.ProcessRequest(name=name, raw_document=raw_document)

    result = client.process_document(request=request)
    document = result.document

    with open(args.response_json_file, "w") as f:
        json.dump(
            documentai.Document.to_dict(document),
            f,
            ensure_ascii=False,
            indent=2,
        )
