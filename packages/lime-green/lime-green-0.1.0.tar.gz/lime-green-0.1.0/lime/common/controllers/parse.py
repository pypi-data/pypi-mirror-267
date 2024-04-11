import os
import json
import yaml
from typing import (
    List,
)
from pydantic import (
    BaseModel
)
from lime.common.models.internal import (
    MdSheetSection,
    MdQuestionSection,
    MdDocument,
    QuestionSchema,
    SheetSchema,
)

ENDCHAR_MD_TOKENS = ['|EVAL-ENDCHAR|', '<EVAL-ENDCHAR>']

def strip_end_token(
        text : str,
        endchar_tokens : List[str] = ENDCHAR_MD_TOKENS,
) -> str:
    endchar_ind =  max([text.find(tok) for tok in endchar_tokens])
    if endchar_ind != -1:
        return text[:endchar_ind]
    return text

def parse(
    text: list, 
    d_md: dict, 
    check_name: bool = False
) -> list:

    parsed_markers = []
    for i, line in enumerate(text):
        for obj, md_header in d_md.items():
            marker = "#" * md_header + " "
            if line.startswith(marker):
                data = line.replace(marker, "").strip()
                if check_name and (data.lower() != obj): continue
                parsed_markers.append((i, obj, data))

    parsed_markers.append((len(text) + 1, None, None)) # include last line

    doc_markers = [
        {
            'start': parsed_markers[i][0] + 1, 
            'end': parsed_markers[i+1][0], 
            'obj_type': parsed_markers[i][1],
            'obj_name': parsed_markers[i][2],
        }
        for i in range(len(parsed_markers) - 1)
    ]

    return doc_markers


def extract_sections(
    text: list,
    parsed_markers: list,
    compress: bool = False,
) -> list:

    sections = []
    for section in parsed_markers:
        section_text = text[section['start']: section['end']]
        if compress:
            section_text = "".join(section_text)
        sections.append({
            'type': section['obj_type'],
            'name': section['obj_name'],
            'text': section_text
        })
    return sections


def extract_meta_kv(
    text: str,
) -> dict:
    d_meta = {}
    for line in text.split('\n'):
        try:
            
            ind = line.find(':')
            if ind == -1: 
                continue
            
            k = line[:ind]
            v = line[ind+1:]
            
            # remove the markdown bullet point if present
            if k.startswith(('-', ' -')):
                k = k[k.find('-')+1:]
                k = k.strip()

            # sanitize and format as snake case
            k = k.strip().lower().replace('  ', ' ')
            k = k.strip().lower().replace(' ', '_')
            k = k.strip().lower().replace('-', '_')

            # TODO - does the key name need to be [fuzzy] matched to a schema?
            # TODO - does this value need to be broken to tags
            # TODO - does this value need to be checked as enum

            v = v.strip()
            
            d_meta[k] = v

        except Exception as e: 
            pass

    return d_meta




def parse_markdown(
    text: str, 
    md_schema: dict
) -> MdDocument:
    
    # parse and extract major sections
    d_md = {obj: md_schema[obj]['md_header'] for obj in md_schema}

    parsed_markers = parse(text, d_md, check_name=False)

    major_sections = extract_sections(text, parsed_markers)

    # parse and extract sub-sections
    output = MdDocument(header=None, questions=[])
    d_sheet_meta = None
    sheet_question = ''
    
    for section in major_sections:
        
        section_type = section['type']
        
        d_md = {subsection_name: md_schema[section_type]['children']['md_header']
                for subsection_name in md_schema[section_type]['children']['options']
        }
        
        parsed_markers = parse(section['text'], d_md, check_name=True)
        
        sub_sections = extract_sections(section['text'], parsed_markers, compress=True)
    
        # apply sub-section specific parsing
        for sub_section in sub_sections:
            
            if sub_section.get('type') == 'meta':
                
                if section_type == 'sheet':
                    d_sheet_meta = extract_meta_kv(sub_section['text'])
                    sub_section['data'] = d_sheet_meta
                    
                elif section_type == 'question':
                    d_meta = extract_meta_kv(sub_section['text'])
                    if d_sheet_meta is not None:
                        tmp = d_sheet_meta.copy()
                        tmp.update(d_meta)
                        d_meta = tmp
                    sub_section['data'] = d_meta
                
            if sub_section.get('type') == 'question':

                if section_type == 'sheet':
                    sheet_question = strip_end_token(sub_section['text'])
                    sub_section['clean'] = strip_end_token(sub_section['text'])
                    
                elif section_type == 'question':
                    sub_section['text_sys'] = sheet_question
                    sub_section['text_usr'] = strip_end_token(sub_section['text'])
                    sub_section['text'] = (
                        sheet_question + strip_end_token(sub_section['text'])
                    )
                    
            if sub_section.get('type') == 'answer':
                sub_section['answer_clean'] = (
                    strip_end_token(sub_section['text'])
                )

        if section_type == 'sheet':
            output.header = MdSheetSection(
                type = section_type,
                name = section['name'],
                sub_sections = sub_sections
            )
        elif section_type == 'question':
            output.questions.append(
                MdQuestionSection(
                    type = section_type,
                    name = section['name'],
                    sub_sections = sub_sections
                )
            )
        else:
            raise ValueError(f'Unknown section type: {section_type}')

    return output


def extract_gen_params(meta_data: dict) -> dict:
    params = {
        'temperature': float,
        'max_tokens': int,
        'seed': int,
    }
    gen_params = {}
    for k, f in params.items():
        if k in meta_data:
            try: gen_params[k] = f(meta_data[k])
            except: pass
    return gen_params

def parse_wrapper(
    fn: str,
    md_schema_fn: str,
) -> MdDocument:

    with open(fn, 'r') as f:
        text = f.readlines()

    with open(md_schema_fn, 'r') as f:
        md_schema = yaml.safe_load(f)

    return parse_markdown(text, md_schema)


def parse_to_obj(
    fn: str,
    md_schema_fn: str = None,
) -> SheetSchema:
    
    if md_schema_fn is None:
        md_schema_fn = os.path.join(
            os.path.dirname(__file__), 
            '../../data/md-schema.yaml'
        )

    md_doc = parse_wrapper(fn, md_schema_fn)

    sheet_obj = SheetSchema.from_mddoc(md_doc)

    sheet_obj.sheet_fn = os.path.basename(fn)

    return sheet_obj


if __name__ == '__main__':
    md_doc = parse_wrapper(
        '../../../../datasets/tmp/one/input-common-sense-2.md',
        '../../data/md-schema.yaml'
    )
    
    sheet = SheetSchema.from_mddoc(md_doc)    
    print(sheet.model_dump_json(indent=2))
    # print(z.questions[0].model_dump())
    # x = z.to_json()
    # print(json.dumps(sheet_obj, indent=2))
    
