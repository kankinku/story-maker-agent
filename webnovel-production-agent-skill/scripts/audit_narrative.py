#!/usr/bin/env python3
"""Deterministic narrative-structure audit for the Web Novel Production Loop."""
from __future__ import annotations
import argparse, json, sys
from pathlib import Path
from typing import Any


def nonempty(v: Any) -> bool:
    return isinstance(v, str) and bool(v.strip())


def audit(project: dict[str, Any]) -> dict[str, Any]:
    errors: list[dict[str, str]] = []
    warnings: list[dict[str, str]] = []
    ne = project.get('narrative_engine', {})
    opening = ne.get('opening_contract', {})
    advantage = ne.get('protagonist_advantage', {})
    pov = ne.get('pov_policy', {})
    exposition = ne.get('exposition_policy', {})
    phases = ne.get('phase_map', [])
    foreshadows = ne.get('foreshadow_ledger', [])
    ladder = ne.get('scale_ladder', [])
    sustain = project.get('author_sustainability', {})
    episodes = project.get('plot', {}).get('episodes', [])

    for key in ['protagonist_identity','current_situation','immediate_goal','motive','obstacle','stakes','protagonist_imprint']:
        if not nonempty(opening.get(key)):
            errors.append({'code':'OPENING_CONTRACT_MISSING','path':f'narrative_engine.opening_contract.{key}','message':f'{key}가 필요합니다.'})
    if opening.get('opening_action_mode') == 'combat':
        if not nonempty(opening.get('combat_narrative_function')):
            errors.append({'code':'OPENING_COMBAT_ANCHOR','path':'narrative_engine.opening_contract.combat_narrative_function','message':'1화 전투의 서사 기능이 필요합니다.'})
        if not opening.get('reader_known_cards'):
            errors.append({'code':'OPENING_COMBAT_CARD','path':'narrative_engine.opening_contract.reader_known_cards','message':'독자가 미리 아는 카드가 없는 1화 전투입니다.'})

    for key in ['prior_profession','ability_synergy','unique_domain','exclusive_access','boundary','cost']:
        if not nonempty(advantage.get(key)):
            errors.append({'code':'ADVANTAGE_MISSING','path':f'narrative_engine.protagonist_advantage.{key}','message':f'{key}가 필요합니다.'})
    if len(advantage.get('transferable_expertise', [])) < 1:
        errors.append({'code':'EXPERTISE_EMPTY','path':'narrative_engine.protagonist_advantage.transferable_expertise','message':'전이 가능한 전문성이 필요합니다.'})
    if len(set(advantage.get('proof_episodes', []))) < 2:
        errors.append({'code':'ADVANTAGE_PROOF_THIN','path':'narrative_engine.protagonist_advantage.proof_episodes','message':'1~25화 안에 최소 2개의 증명 회차가 필요합니다.'})

    if not pov.get('switch_markers') or not nonempty(pov.get('anchor_method')):
        errors.append({'code':'POV_POLICY_MISSING','path':'narrative_engine.pov_policy','message':'POV 전환 앵커 정책이 필요합니다.'})
    if exposition.get('character_first') is not True:
        errors.append({'code':'EXPOSITION_CHARACTER_FIRST','path':'narrative_engine.exposition_policy.character_first','message':'정보 공개는 캐릭터 서사 우선이어야 합니다.'})

    phase_names={p.get('name') for p in phases}
    required={'imprint','growth','relationship','scale'}
    if not required.issubset(phase_names):
        errors.append({'code':'PHASE_MAP_INCOMPLETE','path':'narrative_engine.phase_map','message':f'누락 phase: {sorted(required-phase_names)}'})
    ladder_names={p.get('phase') for p in ladder}
    if not required.issubset(ladder_names):
        errors.append({'code':'SCALE_LADDER_INCOMPLETE','path':'narrative_engine.scale_ladder','message':f'누락 scale phase: {sorted(required-ladder_names)}'})

    for f in foreshadows:
        gap=f.get('payoff_episode',0)-f.get('seed_episode',0)
        if gap > 8 and (not f.get('reminder_required') or not nonempty(f.get('reminder_plan'))):
            errors.append({'code':'FORESHADOW_REMINDER_MISSING','path':f"narrative_engine.foreshadow_ledger.{f.get('id','?')}",'message':'8화를 넘는 복선에 reminder가 필요합니다.'})

    max_terms=exposition.get('max_new_terms_per_episode',3)
    allowed_pov={pov.get('primary'), *pov.get('allowed_variants', [])}
    proof_eps=set(advantage.get('proof_episodes', []))
    actual_proof=set()
    for ep in episodes:
        n=ep.get('number')
        if len(ep.get('new_terms', [])) > max_terms:
            errors.append({'code':'EXPOSITION_BUDGET_EXCEEDED','path':f'plot.episodes[{n}].new_terms','message':f'{n}화 신규 용어가 설명 예산을 초과했습니다.'})
        if ep.get('pov') not in allowed_pov and ep.get('pov') not in {'protagonist'}:
            if not nonempty(ep.get('pov_switch_marker')):
                errors.append({'code':'POV_ANCHOR_MISSING','path':f'plot.episodes[{n}].pov','message':f'{n}화 POV 전환 앵커가 없습니다.'})
        if nonempty(ep.get('profession_synergy')) or nonempty(ep.get('unique_domain_payoff')):
            actual_proof.add(n)
        if ep.get('stage_transition') and not ep.get('relationship_anchor_ids'):
            errors.append({'code':'RELATIONSHIP_ANCHOR_MISSING','path':f'plot.episodes[{n}].relationship_anchor_ids','message':f'{n}화 무대 이동에 관계 앵커가 없습니다.'})
        if ep.get('high_risk_event') != 'none' and ep.get('high_risk_event') is not None:
            warnings.append({'code':'HIGH_RISK_EVENT_REVIEW','path':f'plot.episodes[{n}].high_risk_event','message':'고위험 서사 장치는 사람 승인이 필요합니다.'})
    missing_proofs=proof_eps-actual_proof
    if missing_proofs:
        errors.append({'code':'ADVANTAGE_PROOF_NOT_PLANNED','path':'plot.episodes','message':f'직업/고유 영역 증명 회차가 계획에 반영되지 않았습니다: {sorted(missing_proofs)}'})

    bp=sustain.get('buffer_policy', {})
    if bp and not (bp.get('minimum_launch',0) <= bp.get('preferred',0) <= bp.get('deep_buffer',0)):
        errors.append({'code':'BUFFER_POLICY_ORDER','path':'author_sustainability.buffer_policy','message':'minimum_launch <= preferred <= deep_buffer 순서여야 합니다.'})
    if sustain.get('reaction_check_interval_days',0) < 1:
        errors.append({'code':'REACTION_SCHEDULE_MISSING','path':'author_sustainability.reaction_check_interval_days','message':'독자 반응 확인 주기가 필요합니다.'})
    if sustain.get('isolation_risk') in {'high','critical'}:
        warnings.append({'code':'AUTHOR_ISOLATION_RISK','path':'author_sustainability.isolation_risk','message':'연재 속도보다 회복과 최소 소통 계획을 우선하세요.'})

    status='FAIL' if errors else ('WARN' if warnings else 'PASS')
    return {'status':status,'errors':errors,'warnings':warnings,'metrics':{'phase_count':len(phases),'foreshadow_count':len(foreshadows),'scale_steps':len(ladder),'planned_advantage_proofs':len(actual_proof)}}


def main() -> int:
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('project',type=Path)
    args=ap.parse_args()
    try: project=json.loads(args.project.read_text(encoding='utf-8-sig'))
    except (OSError,json.JSONDecodeError) as exc:
        print(json.dumps({'status':'FAIL','errors':[{'code':'INPUT','message':str(exc)}]},ensure_ascii=False,indent=2)); return 2
    result=audit(project); print(json.dumps(result,ensure_ascii=False,indent=2)); return 0 if result['status'] in {'PASS','WARN'} else 1

if __name__=='__main__':
    sys.exit(main())
