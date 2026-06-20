#!/usr/bin/env python3
"""Run deterministic schema and narrative regression cases."""
from __future__ import annotations
import argparse, importlib.util, json, sys
from pathlib import Path
from typing import Any

ROOT=Path(__file__).resolve().parents[1]

def load(path: Path, name: str, func: str):
    spec=importlib.util.spec_from_file_location(name,path)
    if spec is None or spec.loader is None: raise RuntimeError(f'Could not load {path}')
    module=importlib.util.module_from_spec(spec); spec.loader.exec_module(module); return getattr(module,func)

def combine(v:dict[str,Any],a:dict[str,Any])->dict[str,Any]:
    rank={'PASS':0,'WARN':1,'FAIL':2}; status=max([v['status'],a['status']],key=lambda s:rank[s])
    return {'status':status,'errors':v.get('errors',[])+a.get('errors',[]),'warnings':v.get('warnings',[])+a.get('warnings',[]),'metrics':{'validator':v.get('metrics',{}),'narrative':a.get('metrics',{})}}

def main()->int:
    ap=argparse.ArgumentParser(description=__doc__); ap.add_argument('cases',type=Path); args=ap.parse_args()
    doc=json.loads(args.cases.read_text(encoding='utf-8'))
    validate=load(ROOT/'scripts'/'validate_project.py','validate_project','validate_project')
    audit=load(ROOT/'scripts'/'audit_narrative.py','audit_narrative','audit')
    results=[]; failed=0
    for case in doc['cases']:
        fixture=(args.cases.parent/case['input_fixture']).resolve(); project=json.loads(fixture.read_text(encoding='utf-8'))
        actual=combine(validate(project),audit(project)); codes={e['code'] for e in actual['errors']}; warnings={w['code'] for w in actual['warnings']}
        expected_codes=set(case.get('expected_error_codes',[])); forbidden_codes=set(case.get('forbidden_error_codes',[]))
        passed=actual['status']==case['expected_status'] and expected_codes.issubset(codes) and not (forbidden_codes & codes)
        if not passed: failed+=1
        results.append({'case_id':case['case_id'],'name':case['name'],'expected':case['expected_status'],'actual':actual['status'],'passed':passed,'error_codes':sorted(codes),'warning_codes':sorted(warnings)})
    summary={'total':len(results),'passed':len(results)-failed,'failed':failed,'results':results}; print(json.dumps(summary,ensure_ascii=False,indent=2)); return 1 if failed else 0
if __name__=='__main__': sys.exit(main())
