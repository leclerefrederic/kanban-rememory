from pathlib import Path
import ast,subprocess,shutil,tempfile,hashlib,json,sys
R=Path(sys.argv[1]).resolve() if len(sys.argv)>1 else Path(__file__).resolve().parents[3];base=Path(tempfile.mkdtemp(prefix='kr-card141-adoption-',dir='/private/tmp'));out=[]
def run(root,*args,expected=0):
 p=subprocess.run([sys.executable,*args],cwd=root,capture_output=True,text=True);assert p.returncode==expected,(args,p.returncode,p.stdout,p.stderr);return p.stdout+p.stderr
def digest(root):
 return {str(p.relative_to(root)):hashlib.sha256(p.read_bytes()).hexdigest() for p in root.rglob('*') if p.is_file() and '.git' not in p.parts and '__pycache__' not in p.parts}
def copy(root,relative):
 src=R/relative;dst=root/relative;dst.parent.mkdir(parents=True,exist_ok=True)
 if src.is_dir():shutil.copytree(src,dst,dirs_exist_ok=True,ignore=shutil.ignore_patterns('__pycache__'))
 else:shutil.copy2(src,dst)
module=ast.parse((R/'agents/tools/test-kanban-board.py').read_text());names=next(ast.literal_eval(n.value) for n in module.body if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='INSTALL_FILES' for t in n.targets))
for flavor in ['fresh','existing']:
 root=base/flavor;root.mkdir();subprocess.run(['git','init','-q',str(root)],check=True)
 if flavor=='existing':
  (root/'AGENTS.md').write_text('Project policy: deployment requires explicit authorization.\n');(root/'CLAUDE.md').write_text('Keep custom instructions.\n');(root/'app.py').write_text('print("existing product")\n');(root/'.claude').mkdir();(root/'.claude/settings.json').write_text(json.dumps({'model':'custom-model','hooks':{'Stop':[{'hooks':[{'type':'command','command':'echo keep'}]}]}}));(root/'.agents/skills/personal').mkdir(parents=True);(root/'.agents/skills/personal/SKILL.md').write_text('Personal skill\n')
 for p in names:copy(root,p)
 copy(root,'agents/tools/kanban')
 with (root/'AGENTS.md').open('a') as f:f.write('Default: [KR Orchestrator](agents/roles/orchestrator.md). Explicit and delegated roles take precedence. Read [shared rules](agents/guidelines/working-rules.md).\n')
 with (root/'CLAUDE.md').open('a') as f:f.write('@AGENTS.md\n')
 run(root,'agents/tools/manage-kanban-board.py','init','--template','standard','--wip-limit','1','--timezone','Europe/Paris');assert not (root/'project/kanban').exists()
 run(root,'agents/tools/manage-kanban-board.py','init','--template','standard','--wip-limit','1','--timezone','Europe/Paris','--apply');run(root,'agents/tools/manage-kanban-board.py','validate');before=digest(root);run(root,'agents/tools/manage-kanban-board.py','init','--template','standard','--wip-limit','1','--timezone','Europe/Paris','--apply');assert digest(root)==before
 out.append({'case':flavor+' core','result':'passed','fixture':str(root),'evidence':'approved preview/apply, links/show policy and idempotence'})
 run(root,'agents/tools/manage-kanban-board.py','show')
 if flavor=='existing':
  assert 'deployment requires' in (root/'AGENTS.md').read_text() and 'Keep custom' in (root/'CLAUDE.md').read_text()
  for p in ['agents/skills','agents/tools/sync-skills.py','agents/hosts/claude/agents','agents/tools/role-limit-hook.py','agents/tools/install-claude-role-hook.py','agents/tools/guard-batch-work.py','agents/tools/check-batch-publication.py','agents/tools/git-hooks','agents/tools/configure-telegram.py','agents/tools/notify-telegram.py','agents/tools/test-telegram-setup.py']:copy(root,p)
  run(root,'agents/tools/sync-skills.py');run(root,'agents/tools/sync-skills.py','--check');run(root,'agents/tools/install-claude-role-hook.py');run(root,'agents/tools/install-claude-role-hook.py','--apply');before=digest(root);run(root,'agents/tools/sync-skills.py');run(root,'agents/tools/install-claude-role-hook.py','--apply');assert digest(root)==before
  assert (root/'app.py').read_text()=='print("existing product")\n';assert (root/'.agents/skills/personal/SKILL.md').read_text()=='Personal skill\n';settings=json.loads((root/'.claude/settings.json').read_text());assert settings['model']=='custom-model' and settings['hooks']['Stop']
  for name in ['draft','ready','approved','resources/active','resources/archived']:(root/'project/specs'/name).mkdir(parents=True,exist_ok=True)
  (root/'project/batches').mkdir();run(root,'agents/tools/manage-kanban-board.py','validate')
  out.append({'case':'add selected modules and rerun','result':'passed','fixture':str(root),'evidence':'both skill hosts; Claude hook; Batch dirs; product, existing instructions, personal skill and settings preserved'})
  missing=root/'agents/hosts/claude/agents/writer.md';saved=missing.read_bytes();missing.unlink();before=digest(root);message=run(root,'agents/tools/install-claude-role-hook.py','--apply',expected=1);assert 'Nothing was changed' in message and digest(root)==before;missing.write_bytes(saved);run(root,'agents/tools/install-claude-role-hook.py','--apply')
  out.append({'case':'missing prerequisite and recovery','result':'passed','fixture':str(root),'evidence':'missing canonical adapter refuses before changes, restoration recovers'})
  run(root,'agents/tools/test-telegram-setup.py');out.append({'case':'commands and simulated Telegram','result':'passed','fixture':str(root),'evidence':'copied documented verification script runs 22 tests; no real Telegram message'})
# Frozen records/resources and role access headers must be unchanged.
changed=subprocess.check_output(['git','diff','--name-only','308b747c82dbe290bbd14a53d791be90c2949646'],cwd=R,text=True).splitlines();protected=('project/kanban/completion/','project/kanban/cancellation/','project/batches/','project/specs/approved/','project/specs/resources/')
assert not any(p.startswith(protected) for p in changed)
for old,new in [('development-agent','developer'),('specification-agent','writer'),('tester','tester')]:
 original=subprocess.check_output(['git','show','308b747:agents/roles/'+old+'.md'],cwd=R,text=True);current=(R/'agents/roles'/f'{new}.md').read_text()
 for key in ['read:','write:','git:']:
  a=[s for s in original.splitlines() if s.startswith(key)];b=[s for s in current.splitlines() if s.startswith(key)];assert a==b,(new,key,a,b)
out.append({'case':'frozen content and role ACLs','result':'passed','evidence':'no protected path changes; read/write/git frontmatter identical across renamed roles'})
Path('/private/tmp/card141-adoption-result.json').write_text(json.dumps({'candidate_base':subprocess.check_output(['git','rev-parse','HEAD'],cwd=R,text=True).strip(),'fixture_root':str(base),'cases':out},indent=2)+'\n');print(json.dumps(out,indent=2))
