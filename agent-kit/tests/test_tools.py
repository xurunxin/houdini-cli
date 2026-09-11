from __future__ import annotations
import contextlib
import importlib.util
import io
import json
from pathlib import Path
import tempfile
import unittest
ROOT=Path(__file__).resolve().parents[1];H=ROOT/'skills/houdini-agent'

def module(name,path):
    spec=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m
Q=module('query',H/'tools/query.py');P=module('pack',H/'tools/make_tool_args.py')
I=module('inspect_result',H/'tools/inspect_result.py');SEQ=module('sequence',H/'tools/validate_sequence.py')
A=module('acceptance',H/'tools/check_acceptance.py')
SMOKE=module('smoke',H/'examples/hom/build_sop_smoke.py')
class SearchTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):cls.docs,cls.sources=Q.load_index()
    def test_chinese_cloth(self):self.assertEqual(Q.search('布料穿透',self.docs)[0]['skill'],'houdini-vellum')
    def test_pyro(self):self.assertEqual(Q.search('烟不显示',self.docs)[0]['skill'],'houdini-pyro')
    def test_usd(self):self.assertEqual(Q.search('USD材质不生效',self.docs)[0]['skill'],'houdini-solaris')
    def test_timeout(self):self.assertEqual(Q.search('工具超时',self.docs)[0]['topic'],'cli-contract')
    def test_retrieval_limit(self):self.assertLessEqual(len(Q.search('houdini',self.docs,2)),2)
    def test_empty(self):self.assertEqual(Q.search(' ',self.docs),[])
    def test_unrelated(self):self.assertEqual(Q.search('zzzzzzzzzzzz',self.docs),[])
    def test_kind(self):self.assertTrue(all(d['kind']=='topic' for d in Q.search('vellum',self.docs,3,'topic')))
    def test_budget_json(self):
        payload={'results':[Q.compact(d,self.sources) for d in Q.search('geometry',self.docs,10)],'truncated':False}
        text=Q.bounded_payload(payload,1024);self.assertLessEqual(len(text),1024);json.loads(text)
    def test_path_resolves(self):
        for d in Q.search('mpm',self.docs,10):self.assertTrue((H/d['path']).is_file())
class PackageTests(unittest.TestCase):
    def schema(self,required=None):return {'ok':True,'tool':{'name':'execute_houdini_code','inputSchema':{'type':'object','properties':{'code':{'type':'string'},'label':{'type':'string'}},'required':required or ['code'],'additionalProperties':False}}}
    def test_no_execution(self):
        tool,args,mode=P.build_args(self.schema(),'raise RuntimeError("must not run")','code')
        self.assertEqual(tool,'execute_houdini_code');self.assertIn('compile(',args['code'])
    def test_wrapper_config(self):
        source='print(HOUDINI_AGENT_CONFIG["name"]); assert __name__ == "__main__"'
        _,args,_=P.build_args(self.schema(),source,'code',{'name':'中文 path'})
        out=io.StringIO()
        with contextlib.redirect_stdout(out):exec(args['code'],{})
        self.assertIn('中文 path',out.getvalue())
    def test_missing_code_field(self):
        with self.assertRaises(ValueError):P.build_args(self.schema(),'pass','python')
    def test_extra_required(self):
        with self.assertRaises(ValueError):P.build_args(self.schema(['code','label']),'pass','code')
    def test_extra_unknown(self):
        with self.assertRaises(ValueError):P.build_args(self.schema(),'pass','code',extra={'wrong':1})
    def test_no_code_override(self):
        with self.assertRaises(ValueError):P.build_args(self.schema(),'pass','code',extra={'code':'pass'})
    def test_config_type(self):
        with self.assertRaises(ValueError):P.build_args(self.schema(),'pass','code',config=[])
    def test_syntax_only(self):
        with self.assertRaises(SyntaxError):P.build_args(self.schema(),'this is ! python','code')
    def test_failed_snapshot(self):
        s=self.schema();s['ok']=False
        with self.assertRaises(ValueError):P.build_args(s,'pass','code')
class ResultTests(unittest.TestCase):
    def wrap(self,v):return {'ok':True,'result':{'content':[{'type':'text','text':json.dumps(v)}]}}
    def test_outer_ok_not_proof(self):self.assertEqual(I.inspect({'ok':True})['status'],'unknown')
    def test_mcp_error(self):self.assertEqual(I.inspect({'ok':True,'result':{'isError':True}})['status'],'failed')
    def test_business_error(self):self.assertEqual(I.inspect(self.wrap({'status':'error','message':'bad'}))['status'],'failed')
    def test_business_success(self):self.assertEqual(I.inspect(self.wrap({'status':'success','result':{'nodes':[]}}))['status'],'reported_success')
    def test_partial_failure(self):self.assertEqual(I.inspect(self.wrap({'status':'success','result':{'failed':['bad parm']}}))['status'],'failed')
    def test_vex_validation(self):self.assertEqual(I.inspect(self.wrap({'status':'success','result':{'validation':{'errors':['compile error']}}}))['status'],'failed')
    def test_free_text_unknown(self):self.assertEqual(I.inspect({'ok':True,'result':{'content':[{'type':'text','text':'Code executed successfully.'}]}})['status'],'unknown')
    def test_marker(self):
        v={'ok':True,'result':{'content':[{'type':'text','text':'Code executed successfully.\\n--- Stdout ---\\nHOUDINI_AGENT_RESULT={"ok":true,"counts":{"points":8}}'}]}}
        self.assertEqual(I.inspect(v)['status'],'reported_success');self.assertFalse(I.inspect(v)['artifact_verified'])
    def test_marker_failure(self):
        v={'ok':True,'result':{'content':[{'type':'text','text':'HOUDINI_AGENT_RESULT={"ok":false,"error":"permission required"}'}]}}
        self.assertEqual(I.inspect(v)['status'],'failed')
    def test_prose_error_wins_over_stdout_success_marker(self):
        v={'ok':True,'result':{'content':[{'type':'text','text':'Error (houdini): failed after stdout HOUDINI_AGENT_RESULT={"ok":true}'}]}}
        self.assertEqual(I.inspect(v)['status'],'failed')
    def test_multiple_markers_are_not_success(self):
        v={'ok':True,'result':{'content':[{'type':'text','text':'HOUDINI_AGENT_RESULT={"ok":true}\nHOUDINI_AGENT_RESULT={"ok":false}'}]}}
        self.assertEqual(I.inspect(v)['status'],'unknown')
    def test_pinned_prose_error(self):
        v={'ok':True,'result':{'content':[{'type':'text','text':'Error (houdini): Bad input'}]}}
        self.assertEqual(I.inspect(v)['status'],'failed')
    def test_nontext_unknown(self):self.assertEqual(I.inspect({'ok':True,'result':{'content':[{'type':'image','data':'...'}]}})['status'],'unknown')
    def test_batch_unknown_item_cannot_borrow_success(self):
        for unknown in ({}, {'isError':False}, {'status':'pending'}):
            payload={'ok':True,'results':[self.wrap({'ok':True}),self.wrap(unknown)]}
            with self.subTest(unknown=unknown):self.assertEqual(I.inspect(payload)['status'],'unknown')
    def test_all_batch_items_report_success(self):
        payload={'ok':True,'results':[self.wrap({'ok':True}),self.wrap({'status':'success'})]}
        self.assertEqual(I.inspect(payload)['status'],'reported_success')
    def test_unknown_mcp_representation_cannot_borrow_success(self):
        payload=self.wrap({'ok':True})
        payload['result']['structuredContent']={}
        self.assertEqual(I.inspect(payload)['status'],'unknown')
    def test_empty_or_malformed_result_arrays_are_unknown(self):
        for field in ('content','results'):
            for value in ([], {}, None):
                with self.subTest(field=field,value=value):
                    self.assertEqual(I.inspect({'ok':True,'result':{'status':'success',field:value}})['status'],'unknown')
    def test_pending_child_is_not_completed(self):
        self.assertEqual(I.inspect(self.wrap({'status':'success','result':{'status':'pending'}}))['status'],'unknown')
    def test_bare_mcp_error_is_failed(self):
        self.assertEqual(I.inspect({'isError':True})['status'],'failed')
class SequenceTests(unittest.TestCase):
    def test_complete(self):
        with tempfile.TemporaryDirectory() as td:
            root=Path(td)
            for f in (1,2,3):(root/f'x.{f:04d}.exr').write_bytes(b'not-an-image')
            r=SEQ.check(root,'x.{frame:04d}.exr',1,3);self.assertTrue(r['ok']);self.assertFalse(r['decoded'])
    def test_missing_and_empty(self):
        with tempfile.TemporaryDirectory() as td:
            root=Path(td);(root/'1').write_bytes(b'')
            r=SEQ.check(root,'{frame}',1,2);self.assertEqual(r['missing_frames'],[2]);self.assertEqual(r['undersize_frames'],[1])
    def test_reject_escape(self):
        with tempfile.TemporaryDirectory() as td:
            with self.assertRaises(ValueError):SEQ.check(Path(td),'../{frame}',1,2)
    def test_reject_fields(self):
        with tempfile.TemporaryDirectory() as td:
            for pattern in ('a.exr','{frame.__class__}','{other}','{frame}{frame}'):
                with self.subTest(pattern=pattern),self.assertRaises(ValueError):SEQ.check(Path(td),pattern,1,2)
    def test_invalid_range(self):
        with tempfile.TemporaryDirectory() as td:
            with self.assertRaises(ValueError):SEQ.check(Path(td),'{frame}',2,1)
class SafetyGuardTests(unittest.TestCase):
    def test_default_no_writes(self):
        with self.assertRaises(ValueError):SMOKE.validate_config({})
    def test_task_no_path_escape(self):
        with self.assertRaises(ValueError):SMOKE.validate_config({'allow_write':True,'allow_cook':True,'task':'../scene'})
    def test_nan_rejected(self):
        with self.assertRaises(ValueError):SMOKE.validate_config({'allow_write':True,'allow_cook':True,'task':'test','size':[1,float('nan'),1]})
    def test_valid_config(self):self.assertEqual(SMOKE.validate_config({'allow_write':True,'allow_cook':True,'task':'test'})[0],'test')
    def test_cook_permission_before_hou_import(self):
        for name in ('geometry_report.py','usd_report.py'):
            m=module('guard_'+name,H/'examples/hom'/name)
            with self.subTest(name=name),self.assertRaises(ValueError):m.run({})
class AcceptanceTests(unittest.TestCase):
    def report(self,status,evidence=None):return {'task':'test','checks':[{'layer':'technical','criterion':'file check','status':status,'evidence':evidence or []}]}
    def test_unknown(self):
        with tempfile.TemporaryDirectory() as td:self.assertEqual(A.check(self.report('unknown'),Path(td))['status'],'unknown')
    def test_malformed_status_is_invalid(self):
        with tempfile.TemporaryDirectory() as td:
            for state in ([], {}, None, True):
                with self.subTest(state=state):self.assertEqual(A.check(self.report(state),Path(td))['status'],'invalid')
    def test_pass_needs_evidence(self):
        with tempfile.TemporaryDirectory() as td:self.assertEqual(A.check(self.report('pass'),Path(td))['status'],'invalid')
    def test_evidence_presence_not_semantics(self):
        with tempfile.TemporaryDirectory() as td:
            root=Path(td);(root/'log.txt').write_text('test')
            r=A.check(self.report('pass',[{'path':'log.txt','observed':'log exists'}]),root)
            self.assertEqual(r['status'],'reported_pass');self.assertFalse(r['semantic_verified'])
if __name__=='__main__':unittest.main()
